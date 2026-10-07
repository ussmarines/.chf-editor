"""Local, conservative Star Citizen CHF experiment CLI (v7/v8)."""
import argparse
import ctypes
import hashlib
import json
import math
from pathlib import Path
import struct
import tempfile

from chflab.inspector import FACE_PARTS, crc32c, decompress, inspect, structural_diff
from chflab.zstd_runtime import resolve_zstd


def digest(data):
    return hashlib.sha256(data).hexdigest()


def zstd_compress(payload, dll_path, level=1):
    lib = ctypes.CDLL(str(dll_path))
    lib.ZSTD_compressBound.argtypes = (ctypes.c_size_t,)
    lib.ZSTD_compressBound.restype = ctypes.c_size_t
    lib.ZSTD_compress.argtypes = (ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_int)
    lib.ZSTD_compress.restype = ctypes.c_size_t
    lib.ZSTD_isError.argtypes = (ctypes.c_size_t,)
    lib.ZSTD_isError.restype = ctypes.c_uint
    capacity = lib.ZSTD_compressBound(len(payload))
    out = ctypes.create_string_buffer(capacity)
    source = ctypes.create_string_buffer(payload)
    size = lib.ZSTD_compress(out, capacity, source, len(payload), level)
    if lib.ZSTD_isError(size):
        raise ValueError("Zstandard compression failed")
    return out.raw[:size]


def inspect_file(path, dll):
    return inspect(path, dll, True)


def publish_candidate(source, output, dll, before, raw, payload, wanted, change, game_version, control):
    compressed_size = struct.unpack_from("<I", raw, 8)[0]
    old_end = 16 + compressed_size
    compressed = None
    for level in (1, 3, 6, 9, 12, 15, 19, 22):
        attempt = zstd_compress(bytes(payload), dll, level)
        end = 16 + len(attempt)
        if end <= 4096 and (end <= old_end or not any(raw[old_end:end])):
            compressed = attempt
            break
    if compressed is None:
        raise ValueError("compressed stream exceeds container or overlaps opaque bytes")
    new_end = 16 + len(compressed)
    candidate = bytearray(raw)
    candidate[16:new_end] = compressed
    if new_end < old_end:
        candidate[new_end:old_end] = bytes(old_end - new_end)
    struct.pack_into("<II", candidate, 8, len(compressed), len(payload))
    struct.pack_into("<I", candidate, 4, crc32c(candidate[16:]))
    if candidate[:4] != raw[:4] or candidate[-8:] != raw[-8:]:
        raise ValueError("opaque header or trailer changed")
    manifest_path = output.with_suffix(".experiment.json")
    if output.exists() or manifest_path.exists():
        raise ValueError("output or experiment manifest already exists")
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent) as temporary:
        staged = Path(temporary) / "candidate.chf"
        staged.write_bytes(candidate)
        after = inspect_file(staged, dll)
        changes = structural_diff(before, after)
        logical = [c for c in changes if c["path"] != "compressed_size"]
        expected_paths = [wanted] if isinstance(wanted, str) else wanted
        if sorted(entry["path"] for entry in logical) != sorted(expected_paths):
            raise ValueError(f"unexpected logical diff: {logical}")
        reread = inspect_file(staged, dll)
        if reread["sha256"] != digest(bytes(candidate)) or structural_diff(before, reread) != changes:
            raise ValueError("independent output reread failed")
    manifest = {
        "schema": 1, "source": str(source), "source_sha256": before["sha256"],
        "output": str(output), "output_sha256": reread["sha256"],
        "game_version": game_version, "control": control, "change": change,
        "structured_diff": changes, "structural_validation": "PASS",
        "game_load": "not tested", "game_save": "not tested",
        "screenshots": [], "visual_verdict": "not tested",
    }
    manifest_data = json.dumps(manifest, ensure_ascii=False, indent=2).encode("utf-8")
    created_output = False
    created_manifest = False
    try:
        with output.open("xb") as file:
            created_output = True
            file.write(candidate)
        published = inspect_file(output, dll)
        if published["sha256"] != reread["sha256"] or structural_diff(before, published) != changes:
            raise ValueError("independent output reread failed")
        with manifest_path.open("xb") as file:
            created_manifest = True
            file.write(manifest_data)
    except (OSError, ValueError):
        if created_manifest:
            manifest_path.unlink()
        if created_output:
            output.unlink()
        raise
    return manifest


def variant(source, output, dll, part, slot, value, balance_slot, game_version, control,
            expected_source_sha256=None):
    source = source.resolve()
    output = output.resolve()
    if source == output or output.exists():
        raise ValueError("output must be a new path distinct from the source")
    if not 0 <= value <= 65535 or not 0 <= slot < 4 or not 0 <= balance_slot < 4 or slot == balance_slot:
        raise ValueError("value must be 0..65535; slot and balance slot must differ and be 0..3")
    before = inspect_file(source, dll)
    if expected_source_sha256 and before["sha256"].lower() != expected_source_sha256.lower():
        raise ValueError("source SHA-256 changed")
    raw = source.read_bytes()
    if digest(raw) != before["sha256"]:
        raise ValueError("source changed during inspection")
    compressed_size, payload_size = struct.unpack_from("<II", raw, 8)
    payload = bytearray(decompress(raw[16:16 + compressed_size], payload_size, dll))
    parts = before["dna"]["parts"]
    if part not in FACE_PARTS[:parts]:
        raise ValueError("part is not present in this CHF version")
    # The DNA starts after two versions, two GUIDs and its u64 length.
    dna_start = 8 + 32 + 8
    blend_offset = dna_start + 24 + 4 * (slot * parts + FACE_PARTS.index(part))
    balance_offset = dna_start + 24 + 4 * (balance_slot * parts + FACE_PARTS.index(part))
    old_value, head_id = struct.unpack_from("<HH", payload, blend_offset)
    old_balance, balance_head_id = struct.unpack_from("<HH", payload, balance_offset)
    if old_value == value:
        raise ValueError("requested value equals the source value")
    expected_head = before["face_parts"][part][slot][1]
    expected_balance_head = before["face_parts"][part][balance_slot][1]
    if head_id != expected_head or balance_head_id != expected_balance_head:
        raise ValueError("DNA offset disagrees with structural parser")
    new_balance = old_balance - (value - old_value)
    if not 0 <= new_balance <= 65535:
        raise ValueError("balance slot cannot absorb the requested weight change")
    struct.pack_into("<H", payload, blend_offset, value)
    struct.pack_into("<H", payload, balance_offset, new_balance)
    return publish_candidate(
        source, output, dll, before, raw, payload,
        [f"face_parts.{part}[{selected}][0]" for selected in (slot, balance_slot)],
        {"kind": "dna_balanced_weights", "part": part, "slot": slot,
         "balance_slot": balance_slot, "head_id_opaque": head_id,
         "balance_head_id_opaque": balance_head_id,
         "before": old_value, "after": value,
         "balance_before": old_balance, "balance_after": new_balance,
         "region_weight_sum": sum(weight for weight, _ in before["face_parts"][part])},
        game_version, control)


def variant_param(source, output, dll, expected_source_sha256, material_index,
                  submaterial_index, kind, param_index, name_hash, value,
                  channel, game_version, control):
    source = source.resolve()
    output = output.resolve()
    if source == output or output.exists():
        raise ValueError("output must be a new path distinct from the source")
    before = inspect_file(source, dll)
    if before["sha256"].lower() != expected_source_sha256.lower():
        raise ValueError("source SHA-256 changed")
    try:
        item = before["material_definitions"][material_index]["submaterials"][submaterial_index]
        field = "floats" if kind == "float" else "colors"
        entry = item[field][param_index]
    except (IndexError, KeyError) as error:
        raise ValueError("material, submaterial or parameter index is absent") from error
    if min(material_index, submaterial_index, param_index) < 0:
        raise ValueError("negative indices are not allowed")
    if entry["name_hash"].lower() != name_hash.lower():
        raise ValueError("selected parameter hash does not match")
    raw = source.read_bytes()
    if digest(raw) != before["sha256"]:
        raise ValueError("source changed during inspection")
    compressed_size, payload_size = struct.unpack_from("<II", raw, 8)
    payload = bytearray(decompress(raw[16:16 + compressed_size], payload_size, dll))
    offset = entry["payload_offset"]
    base_path = (f"material_definitions[{material_index}].submaterials[{submaterial_index}]"
                 f".{field}[{param_index}]")
    if kind == "float":
        if channel is not None:
            raise ValueError("channel is only valid for RGBA colors")
        old = entry["value"]
        requested = float(value)
        if not math.isfinite(old) or not math.isfinite(requested):
            raise ValueError("non-finite floats are not allowed")
        encoded = struct.pack("<f", requested)
        after_value = struct.unpack("<f", encoded)[0]
        if not math.isfinite(after_value) or after_value == old:
            raise ValueError("float is unrepresentable or unchanged")
        if struct.unpack_from("<f", payload, offset)[0] != old:
            raise ValueError("float payload offset disagrees with parser")
        payload[offset:offset + 4] = encoded
        wanted = base_path + ".value"
    else:
        if channel not in ("R", "G", "B", "A"):
            raise ValueError("color requires --channel R, G, B or A")
        component = "RGBA".index(channel)
        after_value = int(value)
        if not 0 <= after_value <= 255:
            raise ValueError("RGBA component must be 0..255")
        old = entry["rgba"][component]
        if after_value == old:
            raise ValueError("color component is unchanged")
        if list(payload[offset:offset + 4]) != entry["rgba"]:
            raise ValueError("color payload offset disagrees with parser")
        payload[offset + component] = after_value
        wanted = base_path + f".rgba[{component}]"
    change = {"kind": kind, "material_index": material_index,
              "submaterial_index": submaterial_index, "param_index": param_index,
              "name_hash": name_hash.lower(), "before": old, "after": after_value}
    if kind == "color":
        change["channel"] = channel
    return publish_candidate(source, output, dll, before, raw, payload, wanted,
                             change, game_version, control)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--zstd-dll", type=Path,
                        help="native library path; defaults to CHF_ZSTD_DLL or a detected Python library")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("inspect", "diff"):
        p = commands.add_parser(name)
        p.add_argument("files", nargs=1 if name == "inspect" else 2, type=Path)
    p = commands.add_parser("variant")
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--part", required=True, choices=FACE_PARTS)
    p.add_argument("--slot", required=True, type=int)
    p.add_argument("--balance-slot", required=True, type=int,
                   help="second slot to adjust by the opposite amount, preserving the region total")
    p.add_argument("--value", required=True, type=int)
    p.add_argument("--game-version", required=True)
    p.add_argument("--control", required=True, help="UI action or raw DNA slot under test")
    p = commands.add_parser("variant-param", help="change one raw f32 or RGBA component")
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    p.add_argument("--expected-source-sha256", required=True)
    p.add_argument("--material-index", required=True, type=int)
    p.add_argument("--submaterial-index", required=True, type=int)
    p.add_argument("--kind", required=True, choices=("float", "color"))
    p.add_argument("--param-index", required=True, type=int)
    p.add_argument("--name-hash", required=True)
    p.add_argument("--value", required=True)
    p.add_argument("--channel", choices=("R", "G", "B", "A"))
    p.add_argument("--game-version", required=True)
    p.add_argument("--control", required=True)
    args = parser.parse_args()
    try:
        args.zstd_dll = resolve_zstd(args.zstd_dll)
        if args.command == "inspect":
            result = inspect_file(args.files[0], args.zstd_dll)
        elif args.command == "diff":
            left, right = (inspect_file(p, args.zstd_dll) for p in args.files)
            result = {"source_sha256": left["sha256"], "output_sha256": right["sha256"],
                      "changes": structural_diff(left, right)}
        elif args.command == "variant":
            result = variant(args.source, args.output, args.zstd_dll, args.part, args.slot,
                             args.value, args.balance_slot, args.game_version, args.control)
        else:
            result = variant_param(args.source, args.output, args.zstd_dll,
                                   args.expected_source_sha256, args.material_index,
                                   args.submaterial_index, args.kind, args.param_index,
                                   args.name_hash, args.value, args.channel,
                                   args.game_version, args.control)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (OSError, ValueError, OverflowError, struct.error) as error:
        parser.exit(1, f"CHF rejected: {error}\n")


if __name__ == "__main__":
    main()
