# agent-job-pipeline

A job search run by two scheduled AI agents, with a Google Sheet as the only record.

One agent reads your email and updates the processes you are in. The other pulls
new openings and new funding rounds from free public sources, checks each lead
on the employer's own job board, and adds what fits. Both write to the same
sheet, both record what they checked and when, and both stop and tell you when
something they depend on is down.

This repo holds the prompts, the sheet layout, a catalog of free sources with
their quirks, and two small scripts the agents call from a shell. It contains no
data. You bring your own sheet, email account and search criteria.

It was built with Claude scheduled tasks and Claude's Gmail, Google Sheets and
Chrome connectors, but the prompts are plain text and the design does not
depend on one vendor.

## How it works

```
                 Monday 04:37 (your time zone)
                 ┌─────────────────────────────┐
                 │                             │
   ┌─────────────▼───────────┐   ┌─────────────▼──────────────┐
   │ Email sync agent        │   │ Data refresh agent          │
   │ read-only mail tools    │   │ shell, web fetch, browser   │
   │ no browser, no keys     │   │ API keys in the task only   │
   └─────────────┬───────────┘   └─────────────┬──────────────┘
                 │ Pipeline, Recruiters,       │ Shortlist, Watchlist,
                 │ Shortlist status            │ New Raises, Companies
                 ▼                             ▼
          ┌──────────────────────────────────────────┐
          │ Google Sheet (only source of truth)      │
          │ row 1 of each tab: what was pulled, when │
          └──────────────────────────────────────────┘
                 │
                 ▼
          short report to you: changes, due follow-ups,
          decisions needed, sources that failed
```

## Design rules

These are the parts worth copying even if you use none of the prompts.

1. **One record.** The sheet is the only source of truth. Agents read it before
   they write, match rows by company name rather than cell position, and never
   keep their own copies or snapshots.
2. **Split agents by tool access.** The email agent gets read and search tools
   only, so it cannot send, draft, label or delete mail. The data agent never
   touches email. Keys for free-tier APIs live only in the data agent's
   task, never in the sheet, a file or a report.
3. **Stop when a dependency is down.** Several sources need a real browser. The
   data agent checks the browser first. If it cannot reach it, it changes
   nothing and reports that the run did not happen. If the browser drops
   mid-run, it reports which sources finished.
4. **Provenance in the record.** Row 1 of each tab says which sources fed it and
   the last pull date for each. Every run reads those dates, pulls only newer
   items, and appends the new date. A run can be repeated by hand without
   duplicating work.
5. **Verify at the source.** An aggregator listing is a lead, not a fact. A role
   goes on the sheet only after it is confirmed on the employer's own job board.
   A lead that cannot be confirmed goes in the report as unverified.
6. **Deduplicate across every tab** before adding anything, with a script rather
   than by eye (`scripts/name_dedupe.py`).
7. **Free sources only.** No paid plans, no logins, no getting past a bot check
   or CAPTCHA. When a source needs one of those, it goes on the "not used" list
   with the reason.
8. **Batch writes and respect quotas.** Many rows per write call. On a quota
   error, wait a minute and retry.
9. **Say what you assumed.** Defaults the agent chose (a funding floor, a tier
   for a new kind of role) are listed in the report so you can change them.
10. **Short reports.** One message: what changed, what is due, what needs your
    decision.

## Repo layout

| Path | What it is |
|---|---|
| `prompts/email-sync.md` | Prompt for the email agent |
| `prompts/data-refresh.md` | Prompt for the data agent |
| `schema/sheet.md` | Tabs, columns and the row 1 provenance format |
| `sources/catalog.md` | Free sources, endpoints, limits and known quirks |
| `config.example.yaml` | Every placeholder the prompts use |
| `scripts/ats_check.py` | Lists recent engineering roles from public ATS boards |
| `scripts/name_dedupe.py` | Finds which candidate names are already on the sheet |
| `tests/` | Offline tests for both scripts |

## Setup

1. Make a Google Sheet with the tabs in `schema/sheet.md`. Put a one-paragraph
   description in row 1 of each tab and the column headers in row 2.
2. Copy `config.example.yaml` to `config.yaml` (it is in `.gitignore`) and fill
   it in: sheet id, tab ids, time zone, target roles, regions to skip, and any
   free API keys you have.
3. Fill the placeholders in both prompts from your config. Put API keys only in
   the data agent's task, never in this repo.
4. Create two scheduled tasks, one per prompt. Give the email agent only the
   mail and sheet connectors. Give the data agent the sheet connector, a shell
   and browser access. If you use browser-only sources, bind the data task to
   the computer that runs the browser.
5. Run each task once by hand and read the report before you let it run on a
   schedule.

## Running the scripts

```bash
# Recent engineering roles on public boards, newest first
python3 scripts/ats_check.py --since 2026-10-01 \
  ashby:examplecorp greenhouse:example lever:example

# Which of these names are already on any tab (export tabs to CSV first)
python3 scripts/name_dedupe.py --candidates new.txt exports/*.csv

python3 -m unittest discover -s tests
```

Both scripts use only the Python standard library.

## Limits

- Greenhouse's public API gives an "updated" date, not a posting date.
- Some boards read only in a real browser, so those sources need the browser
  bound to the task.
- Free aggregators lag and repeat each other. The verify-at-source rule exists
  because of this.
- Scheduled runs cost model usage. Track tokens per run for the first few runs
  and cut sources that never produce a verified lead.

## License

MIT. See `LICENSE`.
