---
name: job-pipeline
description: Use when the user wants to set up, run or fix the job-search agents that sync email and refresh job and funding data into a Google Sheet.
---

# Job pipeline

Two agents keep a job search current in one Google Sheet. The work lives in
the user's sheet. Your job is to set up or run the agents, keep the sheet
correct, and say what still needs the user.

Paths to `prompts/`, `schema/`, `sources/` and `scripts/` are relative to this
skill's folder (`${CLAUDE_SKILL_DIR}` in Claude Code). `config.yaml` sits in
the same folder. Its fields are listed in `config.example.yaml`.

## The two agents

- **Email sync** reads and searches the user's mail, then updates Pipeline,
  Recruiters and the applied or rejected status on Shortlist. It sets a
  follow-up date for every active process. It has read and search mail tools
  only.
- **Data refresh** pulls new openings and funding rounds from free public
  sources, confirms each role on the employer's own board, and adds what fits
  to Shortlist, Watchlist, New Raises and Companies. It never reads email.

Both report in one short message: what changed, what is due, what needs a
decision. The sheet layout is in `schema/sheet.md`.

## Rules

1. The sheet is the only record. Read it before writing, match rows by
   company name, and keep no copies or snapshots.
2. Each agent gets only the tools it needs. The email agent cannot send,
   draft, label or delete mail. The data agent does not touch email.
3. If the browser or another dependency is down, change nothing and report
   that the run did not happen, or which sources finished.
4. Row 1 of each tab records the sources and last pull dates. Pull only newer
   items and append the new date, so a run can be repeated safely.
5. A listing on an aggregator is a lead. Add a role only after it is confirmed
   on the employer's own board. Report the rest as unverified.
6. Deduplicate across every tab with `scripts/name_dedupe.py`, not by eye.
7. Use free sources only. No paid plans, no sign-ins, no bot checks or
   CAPTCHAs.
8. Write rows in batches. On a quota error, wait about a minute and retry.
9. List every default you chose in the report.

## Tasks

| Request | Use |
|---|---|
| Set up the scheduled tasks | `prompts/email-sync.md` and `prompts/data-refresh.md`, one task each, following Setup in `README.md` |
| Run the email sync now | `prompts/email-sync.md` |
| Run the data refresh now | `prompts/data-refresh.md` |
| Add a source | `sources/catalog.md` for the entry, then the SOURCES list in `prompts/data-refresh.md` |

When setting up the scheduled tasks, fill every `{{PLACEHOLDER}}` in the
prompt from `config.yaml`. A scheduled task does not run from this folder, so
write script and file paths in the task text as absolute paths into this
folder. Put API keys only in the task text, in the KEYS block. Never write a
key to a file, the sheet, a report or the repo.

When adding a source, record its endpoint, limits and quirks in
`sources/catalog.md`, say which tab holds its pull date, and run it once by
hand before it goes into a scheduled task.
