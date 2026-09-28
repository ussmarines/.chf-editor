"""Bounded, source-linked UI evidence for material fields and DNA regions.

Private preset fingerprints are intentionally omitted from the public catalog.
An identical structural signature alone never transfers a visual mapping.
"""

import json
from pathlib import Path


CATALOG = json.loads(Path(__file__).with_name("field_evidence.json").read_text(encoding="utf-8"))
DNA_CATALOG = json.loads(Path(__file__).with_name("dna_evidence.json").read_text(encoding="utf-8"))
PUBLIC_SOURCE = "docs/EXPERIMENTS.md#published-evidence-catalog"


def material_evidence(record):
    """Return structural matches without exposing private file fingerprints."""
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
                            matches.append({
                                "path": f"material_definitions[{mi}].submaterials[{si}].{field}[{pi}]",
                                "value": entry["value"] if kind == "float" else entry["rgba"],
                                "control": item["control"],
                                "observed_effect": item["effect"],
                                "evidence_level": item["level"],
                                "build": item["build"],
                                "scope": "matching structural context; verify the effect on this file",
                                "source": PUBLIC_SOURCE,
                            })
    return {"matched_fields": matches,
            "record_caveats": [],
            "unknown_field_occurrences": total - len(matches),
            "total_field_occurrences": total,
            "note": "Other occurrences remain unknown. A hash label alone does not prove an effect."}


def dna_evidence(record):
    """Report a tested DNA group without assigning meaning to individual slots."""
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
        matched_regions.update(regions)
        matches.append({
            "path": " + ".join(f"face_parts.{region}" for region in regions),
            "raw_slots": (record["face_parts"][regions[0]] if len(regions) == 1 else
                          {region: record["face_parts"][region] for region in regions}),
            "control": item["control"],
            "observed_effect": item["effect"],
            "evidence_level": item["level"],
            "build": item["build"],
            "scope": "matching DNA signature; verify the effect on this file",
            "source": PUBLIC_SOURCE,
        })
    return {
        "matched_evidence": matches,
        "unknown_regions": sorted(set(record["face_parts"]) - matched_regions),
        "unknown_region_count": len(record["face_parts"]) - len(matched_regions),
        "total_regions": len(record["face_parts"]),
        "note": "UI pairs connect gestures to whole regions; no individual head_id or weight has an established anatomical meaning.",
    }


def evidence_report(record):
    return {"dna": dna_evidence(record), "materials": material_evidence(record)}
