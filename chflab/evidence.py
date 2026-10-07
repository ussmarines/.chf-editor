"""Bounded, source-linked UI evidence for material fields and DNA regions.

Private preset fingerprints are intentionally omitted from the public catalog.
An identical structural signature alone never transfers a visual mapping.
"""

import json
from pathlib import Path


CATALOG = json.loads(Path(__file__).with_name("field_evidence.json").read_text(encoding="utf-8"))
DNA_CATALOG = json.loads(Path(__file__).with_name("dna_evidence.json").read_text(encoding="utf-8"))
PUBLIC_SOURCE = "docs/EXPERIMENTS.md#published-evidence-catalog"
POSITIVE_VISUAL_STATUSES = ("capture_supported", "owner_validated_capture", "reported_change")


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
                                "validation": dict(item.get("validation", {})),
                                "tested_channels": item.get("tested_channels", []),
                            })
    positive = sum(m["validation"].get("visual_effect") in POSITIVE_VISUAL_STATUSES for m in matches)
    negative = sum(m["validation"].get("visual_effect") in ("no_visible_change", "no_clear_change") for m in matches)
    return {"matched_fields": matches,
            "record_caveats": [],
            "unknown_field_occurrences": total - len(matches),
            "historical_visual_change_matches": positive,
            "historical_negative_matches": negative,
            "without_historical_visual_change": total - positive,
            "total_field_occurrences": total,
            "note": "Counts describe matching historical observations, not validation of this file. Unknown means no matching observation; negative and inconclusive observations are not positive visual validations."}


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
            "validation": dict(item.get("validation", {})),
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


def material_options(record, mode="Catalog observations"):
    """Guided choices require an exact catalog selector; names alone do not qualify."""
    if mode not in ("Catalog observations", "Observed visual changes", "All raw parameters"):
        raise ValueError("Unknown material filter")
    matches = {m["path"]: m for m in material_evidence(record)["matched_fields"]}
    options = []
    for mi, material in enumerate(record["material_definitions"]):
        for si, sub in enumerate(material["submaterials"]):
            for field, kind in (("floats", "float"), ("colors", "color")):
                for pi, entry in enumerate(sub[field]):
                    path = f"material_definitions[{mi}].submaterials[{si}].{field}[{pi}]"
                    match = matches.get(path)
                    if mode != "All raw parameters" and match is None:
                        continue
                    if mode == "Observed visual changes" and match["validation"].get("visual_effect") not in POSITIVE_VISUAL_STATUSES:
                        continue
                    options.append({"coordinates": (mi, si, kind, pi), "entry": entry,
                                    "evidence": match, "path": path})
    return options
