# Case Study: Governed RHEL Upgrade Delivery Planning

## Headline

From Fragile Upgrade Tracker to Governed Delivery System

## Summary

This sanitized case study shows how enterprise RHEL upgrade planning can be
converted from a fragile tracker into a repeatable delivery-governance workflow.

The work focused on clarifying assumptions, validating baseline data, modeling
change/task relationships, creating review gates, and producing auditable output.

## Challenge

The operating problem was not that a spreadsheet existed. The challenge was that
the workflow had accumulated hidden assumptions around ownership, readiness,
schedule windows, implementation tasks, and reporting. Those assumptions made it
hard to rerun the process, explain exceptions, or know which records were safe
for downstream use.

## Approach

The public demo shows the pattern:

1. Normalize input data.
2. Validate required fields and uniqueness.
3. Model inventory-to-change/task relationships.
4. Apply deterministic governance controls.
5. Separate ready records from exceptions.
6. Preserve reasons for human review.

## Sanitized Visual Evidence

Any source screenshots are treated as private evidence only. Public visuals are
synthetic recreations that preserve the workflow lesson while removing internal
names, workbook tabs, domains, application names, record identifiers, paths, and
production values.

The current web bundle includes recreated visuals for:

- original tracker complexity,
- linked workbook dependency risk,
- derived manual review output,
- change/task relationship ambiguity.

## Demonstrated Result

The synthetic demo demonstrates deterministic classification, explicit review
reasons, and safe separation of ready records from exception records. The
purpose is not to simulate real scale; it is to show repeatable logic,
explainable controls, and auditable output.

## Derek's Role

Derek clarified the operating problem, translated delivery risk into concrete
controls, guided implementation with Claude Code, reviewed the generated logic,
tested behavior, and shaped the workflow into a safer delivery artifact.

## Claim Boundaries

This repository does not claim that it completed production upgrades. It
demonstrates governance, validation, and preparation patterns for upgrade
delivery work.

The business value is inferred from reducing hidden assumptions and improving
repeatability. Time savings are not claimed unless separately measured.
