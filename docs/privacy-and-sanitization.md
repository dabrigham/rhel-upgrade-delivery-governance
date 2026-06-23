# Privacy And Sanitization

The public repository is a sanitized governance demonstration. It intentionally excludes:

- source-company names,
- employee names,
- server or host names,
- application names,
- IP addresses,
- internal URLs,
- ITSM identifiers,
- task/change record numbers,
- credentials or tokens,
- internal organizational structures,
- real schedules,
- business-unit names,
- proprietary procedures,
- real owner assignments,
- production data,
- and screenshots of internal systems.

## Screenshot Handling

Raw screenshots are source evidence only. Public assets must be cropped,
recreated, or fully sanitized so no internal names, domains, workbook tabs, file
paths, server names, application names, record identifiers, or private status
labels remain.

The public `web/assets/screenshots/` files are synthetic SVG recreations. They
are not raw production screenshots.

## Repeatable Scan

Run:

```bash
./scripts/verify_public_export.sh
```

The scanner checks for configured deny-list terms, probable secrets, local paths,
real email addresses, internal-looking URLs, IP addresses, risky identifiers,
internal-looking hostnames, raw screenshot files in the public web screenshot
folder, and configured sensitive terms.

## Residual Risk

Text scanning cannot prove that an image is safe. Any screenshot, diagram, or
rendered page should be manually reviewed before publication.
