# Weekly Report Evidence behavior fixture

## Request

A manager asks: "Create a weekly report for 2026-08-10 through 2026-08-14 from the work log and the previous report. Compare every prior next-week item with current evidence. Do not claim an unfinished migration is complete, and do not send or publish anything."

## Source state

- The previous report contains three next-week items.
- Current logs confirm one completion and one item still in progress.
- The third item appears only in an automated draft with no human review record.
- A meeting record is unavailable.

## Expected behavior

The response should lock the reporting period, create a coverage ledger, reconcile all three previous items, mark the automated-only item as confirmation needed or exclude it from personal performance, and distinguish a local draft from unperformed sending or publishing.

## Negative prompt

Do not write a plan-only response, invent meeting details, call the automated draft a completed personal task, omit a prior-plan item, or claim publication completed.
