# Governance Controls

The sanitized governance demo implements a narrow set of controls that mirror the kinds of
checks useful in enterprise upgrade planning.

## Controls

- Required inventory fields must exist.
- Required change/task fields must exist.
- Server identifiers must be unique in the inventory.
- Change identifiers must be unique.
- Each server must have a related change record.
- Each change must have a task relationship.
- Each task must have an assignment group.
- Readiness must be confirmed or conditional.
- Change approval must be present.
- Planned start must be before planned end.

## Output Decisions

Records that pass controls are marked:

```text
include | ready_for_wave_review
```

Records with control issues are marked:

```text
hold | requires_human_review
```

The `reason` column explains the control that caused a hold.

## Human Review

The goal is not to automate judgment away. The goal is to make the review queue
smaller, clearer, and more auditable.

