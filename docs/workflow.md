# Workflow

## Run

```bash
./scripts/run_demo.sh
```

## Review Outputs

Generated files:

- `outputs/demo_output.csv`
- `outputs/exception_report.csv`

The output file shows all records and their governance decision. The exception
report shows only records that require human review.

## Before And After

Before:

```text
Spreadsheet rows + hidden assumptions + manual interpretation
```

After:

```text
Validated inputs + explicit controls + reviewable exceptions + repeatable output
```

## Publication Gate

Before publishing or linking this asset:

1. Run `./scripts/run_demo.sh`.
2. Run `./scripts/verify_public_export.sh`.
3. Review the HTML page manually.
4. Confirm no private names, systems, IDs, paths, or screenshots are present.
5. Approve final wording.

