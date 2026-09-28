"""Bounded, source-linked UI evidence for material fields and DNA regions.

An identical hash alone never transfers a visual mapping to another preset.
"""

import json
from pathlib import Path


CATALOG = json.loads(Path(__file__).with_name("field_evidence.json").read_text(encoding="utf-8"))
DNA_CATALOG = json.loads(Path(__file__).with_name("dna_evidence.json").read_text(encoding="utf-8"))
RECORD_CAVEATS = {
    "4c520e124eba4b5c19f7ab6043bebd71ead7f45888ceb99ae172a759cadf34b2": [
        "ItemPort cheveux hair_36 mais sous-matériau 3 bun_long_hair_01_m : BioCorp remplace "
        "ce sous-matériau par hair_36_m au réenregistrement. Ne pas transférer le mapping "
        "BaseMelanin de hair_36_m à ce champ brut sans essai contrôlé "
        "(docs/GAME_TEST_2026-09-27.md, FH01)."
    ]
}


def material_evidence(record):
    """Return scoped matches and the number of material values still unmapped."""
    matches = []
    total = 0
    for mi, material in enumerate(record["material_definitions"]):
        for si, sub in enumerate(material["submaterials"]):
            for kind, field in (("float", "floats"), ("color", "colors")):
                for pi, entry in enumerate(sub[field]):
                    total += 1
                    for item in CATALOG:
                        selector = item["selector"]
                        if (selector["material_index"] == mi
                                and selector["submaterial_index"] == si
                                and selector["submaterial_hash"] == sub["name_hash"]
                                and selector["kind"] == kind
                                and selector["param_index"] == pi
                                and selector["name_hash"] == entry["name_hash"]):
                            if record["sha256"] == item["reference_sha256"]:
                                scope = "fichier de référence de cet essai"
                            elif record["sha256"] in item.get("additional_tested_sha256", []):
                                scope = "fichier testé partiellement ; voir niveau de preuve"
                            else:
                                scope = "même structure ; effet à vérifier sur ce fichier"
                            matches.append({
                                "path": f"material_definitions[{mi}].submaterials[{si}].{field}[{pi}]",
                                "value": entry["value"] if kind == "float" else entry["rgba"],
                                "control": item["control"],
                                "observed_effect": item["effect"],
                                "evidence_level": item["level"],
                                "build": item["build"],
                                "reference_sha256": item["reference_sha256"],
                                "scope": scope,
                                "source": item["source"],
                            })
    return {"matched_fields": matches,
            "record_caveats": RECORD_CAVEATS.get(record["sha256"], []),
            "unknown_field_occurrences": total - len(matches),
            "total_field_occurrences": total,
            "note": "Les autres occurrences restent inconnues. Une étiquette de hash n'est pas une preuve d'effet."}


def dna_evidence(record):
    """Report only the exact DNA group tested, without assigning roles to slots."""
    matches = []
    matched_regions = set()
    dna = record["dna"]
    for item in DNA_CATALOG:
        selector = item["selector"]
        regions = selector.get("regions", [selector.get("region")])
        if (not all(region in record["face_parts"] for region in regions)
                or record["body_guid"] != selector["body_guid"]
                or dna["gender_hash"] != selector["gender_hash"]
                or dna["variant_hash"] != selector["variant_hash"]):
            continue
        if record["sha256"] == item["reference_sha256"]:
            scope = "fichier de référence de cet essai"
        elif record["sha256"] in item.get("additional_tested_sha256", []):
            scope = "fichier testé ; voir niveau de preuve"
        else:
            scope = "même signature ADN ; effet à vérifier sur ce fichier"
        matched_regions.update(regions)
        matches.append({
            "path": " + ".join(f"face_parts.{region}" for region in regions),
            "raw_slots": (record["face_parts"][regions[0]] if len(regions) == 1 else
                          {region: record["face_parts"][region] for region in regions}),
            "control": item["control"],
            "observed_effect": item["effect"],
            "evidence_level": item["level"],
            "build": item["build"],
            "reference_sha256": item["reference_sha256"],
            "scope": scope,
            "source": item["source"],
        })
    return {
        "matched_evidence": matches,
        "unknown_regions": sorted(set(record["face_parts"]) - matched_regions),
        "unknown_region_count": len(record["face_parts"]) - len(matched_regions),
        "total_regions": len(record["face_parts"]),
        "note": "Les paires UI relient leurs gestes à des régions entières ; aucun head_id ni poids isolé n'a de sens anatomique établi.",
    }


def evidence_report(record):
    return {"dna": dna_evidence(record), "materials": material_evidence(record)}
