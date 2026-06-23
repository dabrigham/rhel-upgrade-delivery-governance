# Architecture

The demo architecture is intentionally simple.

```mermaid
flowchart TD
  A[synthetic_inventory.csv] --> C[Schema validation]
  B[synthetic_change_records.csv] --> C
  C --> D[Relationship modeling by server_id]
  D --> E[Governance controls]
  E --> F[demo_output.csv]
  E --> G[exception_report.csv]
```

## Components

- `examples/synthetic_inventory.csv`: sanitized inventory baseline.
- `examples/synthetic_change_records.csv`: sanitized change/task records.
- `src/rhel_upgrade_governance/pipeline.py`: deterministic validation and
  governance logic.
- `scripts/run_demo.sh`: one-command synthetic run.
- `scripts/verify_public_export.sh`: privacy and publication scanner.

## Design Choices

- CSV inputs keep the demo transparent to technical and nontechnical reviewers.
- The pipeline uses the Python standard library only.
- Governance reasons are explicit strings, not hidden formulas.
- Exception output is first-class, because human review is part of the control
  model.

