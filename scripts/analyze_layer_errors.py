import json
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class LayerStats:
    name: str
    errors: int = 0


def _safe_int(value: Any) -> Optional[int]:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _preliminary_esi(has_red_flags: bool, resource_count: int, vitals_critical: bool) -> int:
    if has_red_flags:
        preliminary = 2
    else:
        if resource_count >= 2:
            preliminary = 3
        elif resource_count == 1:
            preliminary = 4
        else:
            preliminary = 5

    if vitals_critical:
        preliminary = min(preliminary, 2)
    return preliminary


def _expected_resource_count(expected_esi: int) -> Optional[int]:
    if expected_esi == 3:
        return 2
    if expected_esi == 4:
        return 1
    if expected_esi == 5:
        return 0
    return None


def analyze(jsonl_path: Path) -> Dict[str, Any]:
    if not jsonl_path.exists():
        raise FileNotFoundError(f"Missing file: {jsonl_path}")

    counts = Counter()
    layer_stats = {
        "red_flag": LayerStats("red_flag"),
        "vitals": LayerStats("vitals"),
        "resource": LayerStats("resource"),
        "final_decision": LayerStats("final_decision"),
        "handbook_low_confidence": LayerStats("handbook_low_confidence"),
    }

    with jsonl_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                counts["invalid_json"] += 1
                continue

            expected = _safe_int(record.get("expected"))
            predicted = _safe_int(record.get("predicted"))
            if expected is None or predicted is None:
                counts["missing_labels"] += 1
                continue

            counts["total"] += 1
            if predicted != expected:
                counts["mismatches"] += 1

            intermediate = record.get("intermediate", {})
            has_red_flags = bool(intermediate.get("has_red_flags"))
            vitals = intermediate.get("vitals", {})
            vitals_critical = bool(vitals.get("critical"))
            resources = intermediate.get("resources", {})
            resource_count = int(resources.get("resource_count", 0))
            handbook = intermediate.get("handbook_verification", {})
            handbook_confidence = handbook.get("confidence")

            preliminary = _preliminary_esi(has_red_flags, resource_count, vitals_critical)

            # Heuristic layer conflicts
            if (has_red_flags and expected > 2) or (expected <= 2 and not has_red_flags and not vitals_critical):
                layer_stats["red_flag"].errors += 1

            if (vitals_critical and expected > 2) or (expected <= 2 and not vitals_critical and not has_red_flags):
                layer_stats["vitals"].errors += 1

            expected_resources = _expected_resource_count(expected)
            if expected_resources is not None and resource_count != expected_resources:
                layer_stats["resource"].errors += 1

            if preliminary == expected and predicted != expected:
                layer_stats["final_decision"].errors += 1

            if handbook_confidence is not None and handbook_confidence < 0.7 and predicted != expected:
                layer_stats["handbook_low_confidence"].errors += 1

    total = counts.get("total", 0)
    rates = {}
    for key, stat in layer_stats.items():
        rates[key] = (stat.errors / total) if total else 0.0

    highest_layer = max(rates.items(), key=lambda item: item[1])[0] if rates else None

    return {
        "file": str(jsonl_path),
        "total_cases": total,
        "total_mismatches": counts.get("mismatches", 0),
        "layer_errors": {k: v.errors for k, v in layer_stats.items()},
        "layer_error_rates": rates,
        "highest_error_layer": highest_layer,
        "notes": (
            "Rates are heuristic conflicts based on intermediate signals (red flags, vitals, resources) "
            "and may not reflect true per-layer ground truth."
        ),
    }


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python scripts/analyze_layer_errors.py <path-to-jsonl>")
        raise SystemExit(1)

    jsonl_path = Path(sys.argv[1]).expanduser()
    report = analyze(jsonl_path)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
