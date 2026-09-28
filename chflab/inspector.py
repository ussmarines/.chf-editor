"""Read-only structural inspection of local Star Citizen CHF v7/v8 files.

Uses the installed zstd shared library; does not edit or repack presets.
The layout follows diogotr7/StarBreaker starbreaker-chf at
08302fbdd3a1cc704a0bc0977fb1841927a637bf.
"""

import argparse
import ctypes
import hashlib
import json
import struct
from pathlib import Path


FACE_PARTS = (
    "EyebrowLeft", "EyebrowRight", "EyeLeft", "EyeRight", "Nose",
    "EarLeft", "EarRight", "CheekLeft", "CheekRight", "Mouth",
    "Jaw", "Crown", "Neck",
)


class Reader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def take(self, count):
        if count < 0 or self.pos + count > len(self.data):
            raise ValueError(f"read outside payload at {self.pos}, count {count}")
        chunk = self.data[self.pos:self.pos + count]
        self.pos += count
        return chunk

    def number(self, fmt):
        return struct.unpack("<" + fmt, self.take(struct.calcsize(fmt)))[0]

    def expect(self, fmt, expected):
        offset = self.pos
        actual = self.number(fmt)
        if actual != expected:
            raise ValueError(f"offset {offset}: expected {expected}, got {actual}")


def crc32c(data):
    crc = 0xFFFFFFFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            crc = (crc >> 1) ^ (0x82F63B78 if crc & 1 else 0)
    return crc ^ 0xFFFFFFFF


def decompress(data, size, dll_path):
    lib = ctypes.CDLL(str(dll_path))
    lib.ZSTD_decompress.argtypes = (ctypes.c_void_p, ctypes.c_size_t,
                                    ctypes.c_void_p, ctypes.c_size_t)
    lib.ZSTD_decompress.restype = ctypes.c_size_t
    lib.ZSTD_isError.argtypes = (ctypes.c_size_t,)
    lib.ZSTD_isError.restype = ctypes.c_uint
    output = ctypes.create_string_buffer(size)
    source = ctypes.create_string_buffer(data)
    actual = lib.ZSTD_decompress(output, size, source, len(data))
    if lib.ZSTD_isError(actual) or actual != size:
        raise ValueError(f"zstd decompression failed or size mismatch: {actual} != {size}")
    return output.raw


def parse_itemport(reader, nodes, depth=0):
    if depth > 64 or len(nodes) > 10000:
        raise ValueError("itemport depth/count limit exceeded")
    name = reader.take(4).hex()
    guid = reader.take(16).hex()
    child_count = reader.number("I")
    tail_count = reader.number("I")
    if child_count > 10000:
        raise ValueError("unreasonable child count")
    node = {"port_hash": name, "item_guid": guid,
            "children": child_count, "tail_count": tail_count, "depth": depth}
    nodes.append(node)
    for _ in range(child_count):
        parse_itemport(reader, nodes, depth + 1)


def parse_material(reader):
    material = {
        "attachment_hash": reader.take(4).hex(),
        "base_guid": reader.take(16).hex(),
        "flags": reader.number("I"),
    }
    reader.expect("16s", bytes(16))
    count = reader.number("I")
    if count > 10000:
        raise ValueError("unreasonable submaterial count")
    reader.expect("I", 5)
    submaterials = []
    for index in range(count):
        sub = {"name_hash": reader.take(4).hex()}
        texture_count = reader.number("I")
        if texture_count > 10000:
            raise ValueError("unreasonable texture count")
        textures = []
        for _ in range(texture_count):
            reader.expect("I", 0)
            textures.append({"index": reader.number("B"), "guid": reader.take(16).hex()})
        sub["textures"] = textures
        float_count = reader.number("Q")
        if float_count > 10000:
            raise ValueError("unreasonable float count")
        floats = []
        for _ in range(float_count):
            name_hash = reader.take(4).hex()
            value_offset = reader.pos
            floats.append({"name_hash": name_hash, "value": reader.number("f"),
                           "payload_offset": value_offset})
            reader.expect("I", 0)
        sub["floats"] = floats
        color_count = reader.number("Q")
        if color_count > 10000:
            raise ValueError("unreasonable color count")
        colors = []
        for _ in range(color_count):
            name_hash = reader.take(4).hex()
            value_offset = reader.pos
            colors.append({"name_hash": name_hash, "rgba": list(reader.take(4)),
                           "payload_offset": value_offset})
            reader.expect("I", 0)
        sub["colors"] = colors
        submaterials.append(sub)
        if index + 1 < count:
            reader.expect("I", 5)
        elif reader.pos + 4 <= len(reader.data) and struct.unpack_from("<I", reader.data, reader.pos)[0] == 5:
            reader.expect("I", 5)
    material["submaterials"] = submaterials
    return material


def inspect(path, dll_path, details):
    raw = path.read_bytes()
    if len(raw) != 4096:
        raise ValueError(f"expected 4096 bytes, got {len(raw)}")
    magic, flags, stored_crc, compressed_size, payload_size = struct.unpack_from("<HHIII", raw)
    if magic != 0x4242 or not 0 < compressed_size <= 4080:
        raise ValueError("invalid magic or compressed size")
    if not 0 < payload_size <= 16 * 1024 * 1024:
        raise ValueError("invalid or excessive decompressed size")
    actual_crc = crc32c(raw[16:])
    if actual_crc != stored_crc:
        raise ValueError(f"CRC32C mismatch {stored_crc:08x} != {actual_crc:08x}")
    payload = decompress(raw[16:16 + compressed_size], payload_size, dll_path)
    reader = Reader(payload)
    reader.expect("I", 2)
    version = reader.number("I")
    if version not in (7, 8):
        raise ValueError(f"unsupported internal version {version}")
    body_guid = reader.take(16).hex()
    voice_guid = reader.take(16).hex()
    dna_size = reader.number("Q")
    dna = Reader(reader.take(dna_size))
    dna_name_hash = dna.take(4).hex()
    gender_hash = dna.take(4).hex()
    variant_hash = dna.take(4).hex()
    dna.expect("I", 0)
    parts, blends, unknown, max_head = struct.unpack("<HHHH", dna.take(8))
    if parts != (13 if version == 8 else 12) or blends != 4:
        raise ValueError(f"unexpected DNA dimensions {parts} x {blends}")
    face_parts = {name: [] for name in FACE_PARTS[:parts]}
    for index in range(parts * blends):
        face_parts[FACE_PARTS[index % parts]].append(list(struct.unpack("<HH", dna.take(4))))
    if dna.pos != dna_size:
        raise ValueError(f"unparsed DNA bytes: {dna_size - dna.pos}")
    declared_nodes = reader.number("Q")
    nodes = []
    parse_itemport(reader, nodes)
    if declared_nodes != len(nodes):
        raise ValueError(f"ItemPort count mismatch {declared_nodes} != {len(nodes)}")
    reader.expect("I", 5)
    materials = []
    while reader.pos + 4 <= len(payload) and struct.unpack_from("<I", payload, reader.pos)[0] != 0:
        if len(materials) > 10000:
            raise ValueError("material count limit exceeded")
        materials.append(parse_material(reader))
    if version == 8:
        reader.expect("I", 0)
    if reader.pos != len(payload):
        raise ValueError(f"unparsed payload bytes: {len(payload) - reader.pos}")
    result = {
        "file": str(path), "sha256": hashlib.sha256(raw).hexdigest(),
        "container_size": len(raw), "flags": flags, "crc32c": f"{stored_crc:08x}",
        "compressed_size": compressed_size, "payload_size": payload_size,
        "payload_sha256": hashlib.sha256(payload).hexdigest(),
        "padding_nonzero_bytes": sum(byte != 0 for byte in raw[16 + compressed_size:]),
        "tail8_hex": raw[-8:].hex(), "version": version,
        "body_guid": body_guid, "voice_guid": voice_guid,
        "dna": {"size": dna_size, "name_hash": dna_name_hash,
                "gender_hash": gender_hash, "variant_hash": variant_hash,
                "parts": parts, "blends": blends, "unknown": unknown,
                "max_head_id": max_head},
        "itemports": len(nodes), "itemport_tail_values": sorted(set(n["tail_count"] for n in nodes)),
        "materials": len(materials),
        "submaterials": sum(len(m["submaterials"]) for m in materials),
        "textures": sum(len(s["textures"]) for m in materials for s in m["submaterials"]),
        "float_params": sum(len(s["floats"]) for m in materials for s in m["submaterials"]),
        "color_params": sum(len(s["colors"]) for m in materials for s in m["submaterials"]),
        "parsed_payload_bytes": reader.pos,
    }
    if details:
        result.update({"face_parts": face_parts, "itemport_tree_preorder": nodes,
                       "material_definitions": materials})
    return result


def structural_diff(before, after):
    """Compare parsed fields without assigning visual meaning to opaque values."""
    changes = []

    def walk(left, right, path):
        if type(left) is not type(right):
            changes.append({"path": path, "before": left, "after": right})
        elif isinstance(left, dict):
            for key in sorted(left.keys() | right.keys()):
                walk(left.get(key), right.get(key), f"{path}.{key}")
        elif isinstance(left, list):
            for index in range(max(len(left), len(right))):
                walk(left[index] if index < len(left) else None,
                     right[index] if index < len(right) else None,
                     f"{path}[{index}]")
        elif left != right:
            changes.append({"path": path, "before": left, "after": right})

    for key in ("flags", "compressed_size", "payload_size", "tail8_hex",
                "version", "body_guid", "voice_guid", "dna", "face_parts",
                "itemport_tree_preorder", "material_definitions"):
        walk(before[key], after[key], key)
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--zstd-dll", type=Path, required=True,
                        help="installed libzstd.dll / libzstd.so path")
    parser.add_argument("--details", action="store_true", help="include opaque GUIDs and values")
    parser.add_argument("--compare", action="store_true",
                        help="compare exactly two parsed files by field and array position")
    args = parser.parse_args()
    if args.compare and len(args.files) != 2:
        parser.error("--compare requires exactly two CHF files")
    records = []
    for path in args.files:
        try:
            record = inspect(path, args.zstd_dll, args.details or args.compare)
            records.append(record)
            if not args.compare:
                print(json.dumps(record, ensure_ascii=False))
        except (OSError, ValueError, struct.error) as error:
            print(json.dumps({"file": str(path), "error": str(error)}))
            raise SystemExit(1) from error
    if args.compare:
        print(json.dumps({"before": str(args.files[0]), "after": str(args.files[1]),
                          "changes": structural_diff(*records)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
