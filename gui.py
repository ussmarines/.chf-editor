"""Desktop interface for local CHF inspection and guarded experiments."""
import json
import struct
from copy import deepcopy
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from chf import inspect_file, structural_diff, variant, variant_param
from chflab.evidence import evidence_report

KNOWN_NAMES = json.loads((Path(__file__).parent / "chflab" / "known_names.json").read_text(encoding="utf-8"))
KNOWN_GUIDS = json.loads((Path(__file__).parent / "chflab" / "known_guids.json").read_text(encoding="utf-8"))


def cig_display(raw_hex):
    b = bytes.fromhex(raw_hex)
    return (b[4:8][::-1].hex() + "-" + b[2:4][::-1].hex() + "-" + b[0:2][::-1].hex()
            + "-" + b[14:16][::-1].hex() + "-" + b[8:14][::-1].hex())


def annotate_hashes(value):
    """Add source-backed display names while retaining every raw hash."""
    result = deepcopy(value)
    def walk(node):
        if isinstance(node, dict):
            for key in ("name_hash", "attachment_hash", "port_hash"):
                if key in node and node[key] in KNOWN_NAMES:
                    node[key + "_name"] = KNOWN_NAMES[node[key]]
            for key, catalog in (("item_guid", "itemPortGuids"),
                                 ("base_guid", "materialGuids"), ("guid", "textureGuids")):
                if key in node:
                    display = cig_display(node[key])
                    node[key + "_display"] = display
                    if display in KNOWN_GUIDS[catalog]:
                        node[key + "_name"] = KNOWN_GUIDS[catalog][display]
            for child in list(node.values()):
                walk(child)
        elif isinstance(node, list):
            for child in node:
                walk(child)
    walk(result)
    return result


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("CHF Lab — local")
        self.geometry("1120x840")
        self.dll = tk.StringVar()
        self.female = tk.StringVar()
        self.male = tk.StringVar()
        self.part = tk.StringVar(value="Nose")
        self.slot = tk.IntVar(value=0)
        self.balance_slot = tk.IntVar(value=1)
        self.value = tk.StringVar()
        self.output = tk.StringVar()
        self.material_field = tk.StringVar()
        self.material_value = tk.StringVar()
        self.material_channel = tk.StringVar(value="R")
        self.material_control = tk.StringVar(value="raw material parameter")
        self.material_choices = []
        self.version = tk.StringVar(value="LIVE build to record")
        self.control = tk.StringVar(value="two balanced DNA weights")
        self.active = "female"
        self.records = {}
        self._layout()

    def _row(self, parent, row, label, variable, chooser=None):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=3)
        ttk.Entry(parent, textvariable=variable).grid(row=row, column=1, sticky="ew", padx=5)
        if chooser:
            ttk.Button(parent, text="Browse", command=chooser).grid(row=row, column=2, padx=5)

    def _layout(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=7)
        top.columnconfigure(1, weight=1)
        self._row(top, 0, "Zstandard DLL", self.dll,
                  lambda: self.dll.set(filedialog.askopenfilename() or self.dll.get()))
        self._row(top, 1, "Female preset .chf", self.female,
                  lambda: self.female.set(filedialog.askopenfilename(filetypes=[("CHF", "*.chf")]) or self.female.get()))
        self._row(top, 2, "Male preset .chf", self.male,
                  lambda: self.male.set(filedialog.askopenfilename(filetypes=[("CHF", "*.chf")]) or self.male.get()))
        actions = ttk.Frame(self)
        actions.pack(fill="x", padx=10)
        for title, command in (("Open female", lambda: self.open("female")),
                               ("Open male", lambda: self.open("male")),
                               ("Compare", self.compare)):
            ttk.Button(actions, text=title, command=command).pack(side="left", padx=3)
        self.state = ttk.Label(actions, text="No file open")
        self.state.pack(side="left", padx=12)
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=10, pady=8)
        self.overview = self._text_tab("Overview")
        self.dna = self._text_tab("DNA")
        self.itemports = self._text_tab("ItemPorts")
        self.materials = self._text_tab("Materials")
        self.diff = self._text_tab("Diff")
        self.evidence = self._text_tab("Evidence")
        edit = ttk.LabelFrame(self, text="DNA variant: two balanced weights, same region total")
        edit.pack(fill="x", padx=10, pady=7)
        for i in range(6):
            edit.columnconfigure(i, weight=1)
        ttk.Label(edit, text="Region").grid(row=0, column=0)
        ttk.Combobox(edit, textvariable=self.part, values=("EyebrowLeft", "EyebrowRight", "EyeLeft", "EyeRight", "Nose", "EarLeft", "EarRight", "CheekLeft", "CheekRight", "Mouth", "Jaw", "Crown", "Neck"), state="readonly").grid(row=1, column=0, sticky="ew")
        ttk.Label(edit, text="Slot 0–3").grid(row=0, column=1)
        ttk.Spinbox(edit, from_=0, to=3, textvariable=self.slot).grid(row=1, column=1, sticky="ew")
        ttk.Label(edit, text="Value 0–65535").grid(row=0, column=2)
        ttk.Entry(edit, textvariable=self.value).grid(row=1, column=2, sticky="ew")
        ttk.Label(edit, text="Balancing slot 0–3").grid(row=2, column=0, columnspan=2, sticky="w")
        ttk.Spinbox(edit, from_=0, to=3, textvariable=self.balance_slot, width=5).grid(row=2, column=2, sticky="w")
        ttk.Label(edit, text="Game version").grid(row=0, column=3)
        ttk.Entry(edit, textvariable=self.version).grid(row=1, column=3, sticky="ew")
        ttk.Label(edit, text="Control being tested").grid(row=0, column=4)
        ttk.Entry(edit, textvariable=self.control).grid(row=1, column=4, sticky="ew")
        ttk.Button(edit, text="Export…", command=self.export).grid(row=1, column=5, padx=5)
        ttk.Label(edit, text="head_id values remain unchanged; validate appearance in Star Citizen.").grid(row=3, column=0, columnspan=6, sticky="w", pady=4)

        material_edit = ttk.LabelFrame(self, text="Material variant: one raw parameter")
        material_edit.pack(fill="x", padx=10, pady=7)
        material_edit.columnconfigure(0, weight=5)
        material_edit.columnconfigure(2, weight=2)
        ttk.Label(material_edit, text="Field present in the open preset (source-backed name)").grid(row=0, column=0, sticky="w")
        self.material_combo = ttk.Combobox(material_edit, textvariable=self.material_field, state="readonly")
        self.material_combo.grid(row=1, column=0, sticky="ew", padx=5)
        self.material_combo.bind("<<ComboboxSelected>>", self._material_selection_changed)
        ttk.Label(material_edit, text="Color channel").grid(row=0, column=1)
        channel = ttk.Combobox(material_edit, textvariable=self.material_channel,
                               values=("R", "G", "B", "A"), state="readonly", width=5)
        channel.grid(row=1, column=1, padx=5)
        channel.bind("<<ComboboxSelected>>", self._material_selection_changed)
        ttk.Label(material_edit, text="New value (float or 0–255)").grid(row=0, column=2, sticky="w")
        ttk.Entry(material_edit, textvariable=self.material_value).grid(row=1, column=2, sticky="ew", padx=5)
        ttk.Button(material_edit, text="Export…", command=self.export_material).grid(row=1, column=3, padx=5)
        ttk.Label(material_edit, text="Control being tested / description").grid(row=2, column=0, sticky="w")
        ttk.Entry(material_edit, textvariable=self.material_control).grid(row=3, column=0, columnspan=3, sticky="ew", padx=5)
        ttk.Label(material_edit, text="A field name does not identify its BioCorp control; see the evidence catalog.").grid(row=4, column=0, columnspan=4, sticky="w", pady=4)

    def _text_tab(self, name):
        frame = ttk.Frame(self.tabs)
        self.tabs.add(frame, text=name)
        text = tk.Text(frame, wrap="none", font=("Consolas", 10))
        text.pack(fill="both", expand=True)
        return text

    def _show(self, widget, value):
        widget.delete("1.0", "end")
        widget.insert("1.0", json.dumps(value, ensure_ascii=False, indent=2))

    def _material_selection_changed(self, _event=None):
        index = self.material_combo.current()
        if not 0 <= index < len(self.material_choices):
            return
        _, _, kind, _, entry = self.material_choices[index]
        if kind == "float":
            self.material_value.set(str(entry["value"]))
        else:
            self.material_value.set(str(entry["rgba"]["RGBA".index(self.material_channel.get())]))

    def _set_material_choices(self, record):
        self.material_choices = []
        labels = []
        for mi, material in enumerate(record["material_definitions"]):
            for si, sub in enumerate(material["submaterials"]):
                for field, kind in (("floats", "float"), ("colors", "color")):
                    for pi, entry in enumerate(sub[field]):
                        self.material_choices.append((mi, si, kind, pi, entry))
                        name = KNOWN_NAMES.get(entry["name_hash"], "unknown")
                        labels.append(f"material {mi} / submaterial {si} / {kind} {pi} / {name} [{entry['name_hash']}]")
        self.material_combo.configure(values=labels)
        if labels:
            self.material_combo.current(0)
            self._material_selection_changed()
        else:
            self.material_field.set("")
            self.material_value.set("")

    def open(self, which):
        try:
            path = Path((self.female if which == "female" else self.male).get())
            record = inspect_file(path, Path(self.dll.get()))
            self.records[which] = record
            self.active = which
            self.state.configure(text=f"{which}: {record['sha256'][:12]}… — v{record['version']}")
            self._show(self.overview, {k: v for k, v in record.items() if k not in ("face_parts", "itemport_tree_preorder", "material_definitions")})
            self._show(self.dna, record["face_parts"])
            self._show(self.itemports, annotate_hashes(record["itemport_tree_preorder"]))
            self._show(self.materials, annotate_hashes(record["material_definitions"]))
            self._show(self.evidence, evidence_report(record))
            self._set_material_choices(record)
            if self.part.get() not in record["face_parts"]:
                self.part.set(next(iter(record["face_parts"])))
            self.value.set(str(record["face_parts"][self.part.get()][self.slot.get()][0]))
        except (OSError, ValueError, KeyError, IndexError) as error:
            messagebox.showerror("CHF rejected", str(error))

    def compare(self):
        try:
            if set(self.records) != {"female", "male"}:
                raise ValueError("Open both presets first")
            self._show(self.diff, structural_diff(self.records["female"], self.records["male"]))
            self.tabs.select(4)
        except ValueError as error:
            messagebox.showerror("Comparison", str(error))

    def export(self):
        try:
            source = Path((self.female if self.active == "female" else self.male).get())
            if self.active not in self.records:
                raise ValueError("Open a preset first")
            name = filedialog.asksaveasfilename(defaultextension=".chf", filetypes=[("CHF", "*.chf")])
            if not name:
                return
            result = variant(source, Path(name), Path(self.dll.get()), self.part.get(),
                             self.slot.get(), int(self.value.get()), self.balance_slot.get(),
                             self.version.get(), self.control.get())
            self._show(self.diff, result["structured_diff"])
            self.tabs.select(4)
            messagebox.showinfo("Structural export validated", f"{result['output_sha256']}\nIn-game test: not tested")
        except (OSError, ValueError, KeyError, IndexError, OverflowError, struct.error) as error:
            messagebox.showerror("Export rejected", str(error))

    def export_material(self):
        try:
            if self.active not in self.records:
                raise ValueError("Open a preset first")
            index = self.material_combo.current()
            if not 0 <= index < len(self.material_choices):
                raise ValueError("Select a parameter present in this preset")
            mi, si, kind, pi, entry = self.material_choices[index]
            source = Path((self.female if self.active == "female" else self.male).get())
            name = filedialog.asksaveasfilename(defaultextension=".chf", filetypes=[("CHF", "*.chf")])
            if not name:
                return
            result = variant_param(source, Path(name), Path(self.dll.get()),
                                   self.records[self.active]["sha256"], mi, si, kind, pi,
                                   entry["name_hash"], self.material_value.get(),
                                   self.material_channel.get() if kind == "color" else None,
                                   self.version.get(), self.material_control.get())
            self._show(self.diff, result["structured_diff"])
            self.tabs.select(4)
            messagebox.showinfo("Structural export validated", f"{result['output_sha256']}\nIn-game test: not tested")
        except (OSError, ValueError, KeyError, OverflowError, struct.error) as error:
            messagebox.showerror("Export rejected", str(error))


if __name__ == "__main__":
    App().mainloop()
