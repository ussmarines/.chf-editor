"""Read-only save monitoring; observations never promote the public catalog."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import struct
import time
from uuid import uuid4

from chflab.inspector import inspect, structural_diff

NAMES = json.loads(Path(__file__).with_name('known_names.json').read_text(encoding='utf-8'))


def read_container(path):
    with Path(path).open('rb') as handle:
        raw = handle.read(4097)
    if len(raw) != 4096:
        raise ValueError('Incomplete or unsupported CHF size; waiting for a valid 4096-byte save')
    return raw


def classify(before, after):
    changes = structural_diff(before, after)
    logical = [c for c in changes if c['path'] != 'compressed_size']
    groups = set()
    for change in logical:
        path = change['path']
        match = re.match(r'face_parts\.([^\[]+)', path)
        if match:
            groups.add('DNA/' + match[1])
            continue
        match = re.fullmatch(r'material_definitions\[(\d+)\]\.submaterials\[(\d+)\]\.(floats|colors)\[(\d+)\]\.(value|rgba\[\d+\])', path)
        if match:
            mi, si, field, pi, _ = match.groups()
            entry = before['material_definitions'][int(mi)]['submaterials'][int(si)][field][int(pi)]
            name = NAMES.get(entry['name_hash'], entry['name_hash'])
            change['source_name'] = name
            groups.add(f'Material/{mi}/{si}/{name}')
        else:
            groups.add('Other/' + path.split('.')[0])
    compatible = all(before[key] == after[key] for key in ('version', 'body_guid', 'voice_guid'))
    if not compatible:
        status = 'incompatible_reference'
    elif not logical:
        status = 'no_logical_change'
    elif len(groups) == 1 and not next(iter(groups)).startswith('Other/'):
        status = 'candidate_association'
    else:
        status = 'ambiguous_group'
    return {'status': status, 'categories': sorted(groups), 'changes': changes,
            'mapping_validation': 'not confirmed', 'visual_effect': 'not observed',
            'game_load': 'not observed', 'game_save': 'valid file write observed; producer not verified'}


class SaveMonitor:
    """Poll bounded local files, debounce contents, archive immutable parsed copies."""
    def __init__(self, baseline, dll, output_root, control, build, folder_mode=False,
                 stable_seconds=1.0):
        self.baseline = Path(baseline).resolve()
        self.dll = dll
        self.control, self.build = control.strip(), build.strip()
        if not self.control or not self.build:
            raise ValueError('Provide the control tested and game build before starting')
        self.folder_mode = folder_mode
        self.stable_seconds = stable_seconds
        self.active = True
        self.pending = {}
        self.error = ''
        self.session = Path(output_root).resolve() / ('session-' + uuid4().hex)
        if self.session.is_relative_to(self.baseline.parent):
            raise ValueError('Store monitoring sessions outside the watched directory')
        self.session.mkdir(parents=True, exist_ok=False)
        self.sequence = 0
        self.previous_path, self.previous = self._snapshot(read_container(self.baseline))
        self.known = self._scan()
        # A concurrent baseline write must be noticed on the first poll.
        self.known[self.baseline] = self.previous['sha256']
        self._write_json('session.json', {'schema': 1, 'control': self.control,
            'game_build': self.build, 'baseline_path': str(self.baseline),
            'baseline_sha256': self.previous['sha256'], 'folder_mode': folder_mode,
            'started_utc': datetime.now(timezone.utc).isoformat(),
            'screen_analysis': 'not available', 'catalog_promotion': 'manual review required'})

    def _write_json(self, name, data):
        with (self.session / name).open('x', encoding='utf-8') as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)

    def _paths(self):
        if not self.folder_mode:
            return [self.baseline] if self.baseline.exists() else []
        paths = []
        for path in self.baseline.parent.iterdir():
            if path.suffix.lower() == '.chf' and path.is_file():
                paths.append(path)
                if len(paths) > 256:
                    raise ValueError('More than 256 CHF files; use same-file mode or a smaller folder')
        return paths

    def _scan(self):
        found = {}
        for path in self._paths():
            try:
                found[path] = hashlib.sha256(read_container(path)).hexdigest()
            except (OSError, ValueError) as error:
                self.error = str(error)
        return found

    def _snapshot(self, raw, sequence=None):
        sequence = self.sequence if sequence is None else sequence
        path = self.session / f'{sequence:04d}.chf'
        with path.open('xb') as handle:
            handle.write(raw)
        try:
            record = inspect(path, self.dll, True)
            if record['sha256'] != hashlib.sha256(raw).hexdigest():
                raise ValueError('Snapshot digest disagrees with parser')
        except (OSError, ValueError, struct.error):
            path.unlink()
            raise
        return path, record

    def stop(self):
        self.active = False

    def poll(self, now=None):
        if not self.active:
            return []
        now = time.monotonic() if now is None else now
        self.error = ''
        current = self._scan()
        changed = {path: sha for path, sha in current.items() if self.known.get(path) != sha}
        self.pending = {p: value for p, value in self.pending.items() if p in changed}
        for path, sha in changed.items():
            if path not in self.pending or self.pending[path][0] != sha:
                self.pending[path] = (sha, now)
        if len(changed) > 1:
            self.active = False
            event = {'status': 'multiple_files_changed', 'files': [str(p) for p in changed],
                     'mapping_validation': 'not confirmed', 'instruction': 'Select the intended latest baseline and restart'}
            self._write_json('paused.json', event)
            return [event]
        if not changed:
            if not self.folder_mode and not current:
                self.error = 'Watched file absent; waiting for its next save'
            return []
        path, sha = next(iter(changed.items()))
        if now - self.pending[path][1] < self.stable_seconds:
            return []
        try:
            raw = read_container(path)
            if hashlib.sha256(raw).hexdigest() != sha:
                return []
            # Saving an identical copy under a new name carries no new gesture evidence.
            if sha == self.previous['sha256']:
                self.known[path] = sha
                self.pending.pop(path, None)
                return []
            snapshot, record = self._snapshot(raw, self.sequence + 1)
        except (OSError, ValueError, struct.error) as error:
            self.error = str(error)
            return []
        self.sequence += 1
        event = classify(self.previous, record)
        event.update({'schema': 1, 'sequence': self.sequence, 'control_reported_by_user': self.control,
            'game_build_reported_by_user': self.build, 'time_utc': datetime.now(timezone.utc).isoformat(),
            'observed_file': str(path), 'before_snapshot': self.previous_path.name,
            'after_snapshot': snapshot.name, 'before_sha256': self.previous['sha256'],
            'after_sha256': record['sha256'], 'structural_validation': 'PASS',
            'screen_analysis': 'not available'})
        self._write_json(f'{self.sequence:04d}.json', event)
        self.known[path] = sha
        self.pending.pop(path, None)
        if event['status'] == 'incompatible_reference':
            self.stop()
        else:
            self.previous_path, self.previous = snapshot, record
        return [event]
