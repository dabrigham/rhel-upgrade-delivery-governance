# Screenshot Redaction Guide

Raw screenshots are source evidence only. They are not public assets.

Public visuals must be cropped, recreated, or fully sanitized so no internal
names, domains, workbook tabs, file paths, server names, application names,
status labels, or record identifiers remain.

## Do Not Publish

Do not publish screenshots that contain:

- internal workbook or tab names,
- internal application names,
- internal domains, hostnames, or network paths,
- client or company references,
- employee names or user names,
- real server, application, task, change, or ticket identifiers,
- real status/context labels that reveal operating details,
- production values,
- formula bars that expose internal references,
- screenshots of internal systems.

## Safe Public Approach

Use synthetic recreations that preserve the workflow lesson without copying the
source image. Acceptable public assets include:

- generic spreadsheet-style mockups,
- synthetic warning banners,
- recreated output tables with generic row labels,
- simple diagrams that show relationships without real names or records.

All public visuals should state or imply that they are sanitized recreations, not
raw production screenshots.

## Verification

Before publication:

1. Run `./scripts/verify_public_export.sh`.
2. Review every SVG and HTML page manually.
3. Confirm the public `web/` bundle contains no raw screenshots.
4. Confirm no private terms from the local deny list appear in public files.
5. Confirm claims remain limited to implemented and validated behavior.
