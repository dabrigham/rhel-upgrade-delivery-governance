from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


REQUIRED_INVENTORY_FIELDS = [
    "server_id",
    "application_id",
    "owner_group",
    "environment",
    "readiness_status",
    "target_wave",
]

REQUIRED_CHANGE_FIELDS = [
    "change_id",
    "server_id",
    "task_id",
    "task_assignment_group",
    "planned_start",
    "planned_end",
    "approval_status",
]

READY_STATUSES = {"ready", "conditional"}
APPROVED_STATUSES = {"approved"}


@dataclass(frozen=True)
class GovernanceResult:
    server_id: str
    application_id: str
    owner_group: str
    environment: str
    target_wave: str
    change_id: str
    task_id: str
    task_assignment_group: str
    decision: str
    review_gate: str
    reason: str


def read_rows(path: Path, required_fields: list[str]) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        missing = [field for field in required_fields if field not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"{path} is missing required field(s): {', '.join(missing)}")
        return [
            {field: (row.get(field) or "").strip() for field in reader.fieldnames or []}
            for row in reader
        ]


def validate_unique(rows: list[dict[str, str]], key: str, label: str) -> list[str]:
    seen: set[str] = set()
    errors: list[str] = []
    for row in rows:
        value = row.get(key, "")
        if not value:
            errors.append(f"{label} row missing {key}")
        elif value in seen:
            errors.append(f"{label} duplicate {key}: {value}")
        seen.add(value)
    return errors


def evaluate_row(inventory: dict[str, str], change: dict[str, str] | None) -> GovernanceResult:
    reasons: list[str] = []
    review_gate = "ready_for_wave_review"
    decision = "include"

    if inventory["readiness_status"].lower() not in READY_STATUSES:
        reasons.append("readiness_not_confirmed")
    if not inventory["owner_group"]:
        reasons.append("missing_owner_group")
    if not change:
        reasons.append("missing_change_record")
    else:
        if not change["task_id"]:
            reasons.append("missing_task_relationship")
        if not change["task_assignment_group"]:
            reasons.append("missing_task_assignment_group")
        if change["approval_status"].lower() not in APPROVED_STATUSES:
            reasons.append("change_not_approved")
        if change["planned_start"] >= change["planned_end"]:
            reasons.append("invalid_schedule_window")

    if reasons:
        decision = "hold"
        review_gate = "requires_human_review"

    return GovernanceResult(
        server_id=inventory["server_id"],
        application_id=inventory["application_id"],
        owner_group=inventory["owner_group"],
        environment=inventory["environment"],
        target_wave=inventory["target_wave"],
        change_id=change["change_id"] if change else "",
        task_id=change["task_id"] if change else "",
        task_assignment_group=change["task_assignment_group"] if change else "",
        decision=decision,
        review_gate=review_gate,
        reason=";".join(reasons) if reasons else "validated_relationships_and_controls",
    )


def run_governance_pipeline(
    inventory_path: Path,
    change_path: Path,
    output_path: Path,
    exception_path: Path,
) -> list[GovernanceResult]:
    inventory_rows = read_rows(inventory_path, REQUIRED_INVENTORY_FIELDS)
    change_rows = read_rows(change_path, REQUIRED_CHANGE_FIELDS)

    validation_errors = validate_unique(inventory_rows, "server_id", "inventory")
    validation_errors.extend(validate_unique(change_rows, "change_id", "change"))
    if validation_errors:
        raise ValueError("; ".join(validation_errors))

    changes_by_server = {row["server_id"]: row for row in change_rows}
    results = [
        evaluate_row(inventory, changes_by_server.get(inventory["server_id"]))
        for inventory in inventory_rows
    ]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    exception_path.parent.mkdir(parents=True, exist_ok=True)

    write_results(output_path, results)
    write_results(exception_path, [result for result in results if result.decision == "hold"])
    return results


def write_results(path: Path, results: list[GovernanceResult]) -> None:
    fields = list(GovernanceResult.__dataclass_fields__.keys())
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for result in results:
            writer.writerow({field: getattr(result, field) for field in fields})

