"""One local monitoring session per window; main GUI remains usable."""
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from chflab.monitor import SaveMonitor
from chflab.screen import capture_game, pixel_change
from chflab.zstd_runtime import resolve_zstd


class MonitorWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title('CHF — monitoring des sauvegardes')
        self.geometry('980x650')
        self.monitor = None
        self.timer = None
        self.worker = ThreadPoolExecutor(max_workers=1)
        self.future = None
        self.screen_before = None
        self.last_frame = None
        self.path = tk.StringVar(value=(parent.female if parent.active == 'female' else parent.male).get())
        self.control = tk.StringVar()
        self.build = tk.StringVar(value=parent.version.get())
        self.folder_mode = tk.BooleanVar(value=False)
        self.capture = tk.BooleanVar(value=False)
        self.status = tk.StringVar(value='Choisir le baseline enregistré, nommer le contrôle, puis démarrer.')
        self.screen_status = tk.StringVar(value='Capture locale désactivée')
        self.columnconfigure(1, weight=1)
        for row, label, variable in ((0, 'Fichier de départ', self.path), (1, 'Contrôle testé', self.control), (2, 'Build du jeu', self.build)):
            ttk.Label(self, text=label).grid(row=row, column=0, sticky='w', padx=8, pady=5)
            ttk.Entry(self, textvariable=variable).grid(row=row, column=1, sticky='ew')
        ttk.Button(self, text='Parcourir', command=self.browse).grid(row=0, column=2, padx=8)
        ttk.Checkbutton(self, text='Détecter aussi les nouveaux CHF du même dossier (Sauvegarder sous)', variable=self.folder_mode).grid(row=3, column=0, columnspan=3, sticky='w', padx=8)
        ttk.Checkbutton(self, text='Capture locale de Star Citizen au premier plan, environ 1 image/s', variable=self.capture).grid(row=4, column=0, columnspan=3, sticky='w', padx=8)
        actions = ttk.Frame(self)
        actions.grid(row=5, column=0, columnspan=3, sticky='w', padx=8, pady=8)
        ttk.Button(actions, text='Démarrer / nouveau contrôle', command=self.start).pack(side='left', padx=4)
        ttk.Button(actions, text='Arrêter', command=self.stop).pack(side='left', padx=4)
        ttk.Label(self, textvariable=self.status, wraplength=930).grid(row=6, column=0, columnspan=3, sticky='w', padx=8)
        ttk.Label(self, textvariable=self.screen_status, wraplength=930).grid(row=7, column=0, columnspan=3, sticky='w', padx=8)
        self.results = tk.Text(self, wrap='word')
        self.results.grid(row=8, column=0, columnspan=3, sticky='nsew', padx=8, pady=8)
        self.rowconfigure(8, weight=1)
        ttk.Label(self, text='Un geste puis une sauvegarde. Association candidate uniquement ; effet visuel à confirmer.\nLe nom du contrôle est figé au démarrage. Nouveau contrôle : sélectionner le dernier CHF puis redémarrer.', wraplength=930).grid(row=9, column=0, columnspan=3, sticky='w', padx=8, pady=5)
        self.protocol('WM_DELETE_WINDOW', self.close)

    def browse(self):
        selected = filedialog.askopenfilename(filetypes=[('CHF', '*.chf')], parent=self)
        if selected:
            self.path.set(selected)

    def start(self):
        self.stop()
        try:
            dll = resolve_zstd(self.master.dll.get() or None)
            if self.capture.get():
                try:
                    import PIL  # Dependency check only; no native capture until polling.
                except ImportError as error:
                    raise ValueError('Installer requirements-monitor.txt ou lancer sans capture') from error
            self.monitor = SaveMonitor(self.path.get(), dll,
                Path(__file__).resolve().parents[1] / 'outputs' / 'monitor',
                self.control.get(), self.build.get(), self.folder_mode.get())
            self.screen_before = self.last_frame = None
            self.capture_enabled = self.capture.get()
            self.status.set(f"Surveillance : {self.monitor.control} — session {self.monitor.session}")
            self._tick()
        except (OSError, ValueError) as error:
            self.stop()
            messagebox.showerror('Monitoring', str(error), parent=self)

    def _tick(self):
        if not self.monitor or (not self.monitor.active and self.future is None):
            return
        try:
            if self.future is None:
                self.future = self.worker.submit(self.sample, self.monitor, self.capture_enabled)
            if not self.future.done():
                self.timer = self.after(200, self._tick)
                return
            sampled_monitor, frame, screen_error, events = self.future.result()
            self.future = None
            if sampled_monitor is not self.monitor:
                self.timer = self.after(200, self._tick)
                return
            if screen_error:
                self.screen_status.set(f'Capture indisponible : {screen_error}')
            if frame is not None:
                metric = pixel_change(self.last_frame, frame) if self.last_frame is not None else None
                self.screen_status.set(f'Capture locale active — variation globale {metric if metric is not None else "—"} % (inclut interface, animation et éclairage)')
                self.last_frame = frame
                if self.screen_before is None:
                    self.screen_before = frame
            for event in events:
                if 'sequence' in event:
                    capture_record = {'status': 'unavailable', 'visual_validation': 'not confirmed'}
                    if frame is not None:
                        seq = event['sequence']
                        after_name = f'{seq:04d}-screen-after.png'
                        frame.save(self.monitor.session / after_name)
                        before_name = None
                        if self.screen_before is not None and self.screen_before is not frame:
                            before_name = f'{seq:04d}-screen-before.png'
                            self.screen_before.save(self.monitor.session / before_name)
                        capture_record.update({'status': 'captured after file detection', 'before': before_name,
                            'after': after_name, 'max_size': [1920, 1080],
                            'whole_window_pixel_change_percent': pixel_change(self.screen_before, frame) if before_name else None,
                            'timing': 'first successful session capture or previous saved capture; not synchronized to slider gesture'})
                        self.screen_before = frame
                    else:
                        self.screen_before = None
                    self.monitor._write_json(f"{event['sequence']:04d}-screen.json", capture_record)
                    self.path.set(event['observed_file'])
                self.results.insert('end', json.dumps(event, ensure_ascii=False, indent=2) + '\n\n')
                self.results.see('end')
            if self.monitor.error:
                self.status.set(f'Attente : {self.monitor.error}')
            elif events:
                self.status.set(f"{events[-1]['status']} — contrôle {self.monitor.control} — historique : {self.monitor.session}")
            if self.monitor.active:
                self.timer = self.after(1000, self._tick)
            else:
                self.status.set('Surveillance en pause : plusieurs fichiers ou référence incompatible. Choisir le baseline voulu puis redémarrer.')
        except (OSError, ValueError, RuntimeError) as error:
            self.stop()
            self.status.set(f'Surveillance arrêtée : {error}')

    @staticmethod
    def sample(monitor, capture_enabled):
        # Native window capture can be slow; this worker never touches Tk widgets.
        frame, error = None, None
        if capture_enabled and monitor.active:
            try:
                frame = capture_game()
            except (OSError, ValueError, RuntimeError) as failure:
                error = str(failure)
        return monitor, frame, error, monitor.poll()

    def stop(self):
        if self.timer is not None:
            self.after_cancel(self.timer)
            self.timer = None
        if self.monitor:
            self.monitor.stop()
        self.status.set('Surveillance arrêtée')
        self.screen_status.set('Capture arrêtée')

    def close(self):
        self.stop()
        self.worker.shutdown(wait=False, cancel_futures=True)
        self.destroy()
