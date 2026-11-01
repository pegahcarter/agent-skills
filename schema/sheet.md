# Sheet layout

One Google Sheet. Row 1 of every tab is a short description that also records
the provenance of the tab's data. Row 2 is the header. Data starts on row 3.

## Row 1 provenance format

Agents append to row 1; they never rewrite it. Keep one line per pull:

```
Pulled: web3-jobs-api 2026-10-26; hiring-aggregator 2026-10-26; vc-boards 2026-10-26
Threshold change 2026-10-31: AI companies with a known board qualify for Watchlist.
```

A run finds the last date for each source here, pulls only newer items, and
appends the new date when that source is done. If no date exists for a source,
the run skips it and says so in the report (unless the prompt gives a first-run
cutoff).

## Tabs

### Pipeline (email agent writes; data agent reads for duplicate checks)

| Col | Field | Notes |
|---|---|---|
| A | Company | Match on this, not on row position |
| B | Role | |
| C | Channel | Recruiter, referral, job board, direct email |
| D | Stage | Applied, screen, interview, final, offer, closed |
| E | Last contact | YYYY-MM-DD |
| F | Follow up by | Rule below |
| G | Next step | |
| H | Contact | |
| I | Notes | |

Active rows at the top, then a row reading `Closed`, then closed rows with the
close date.

Follow-up rule for column F: 2 business days after an interview with no news,
1 week after a direct email application, 2 weeks after a job-board application.
After any reply, recompute from that reply's date. If someone named a decision
date, use the next business day after it.

### Recruiters (email agent)

Contact, firm, last contact, status, next step. An `Ignore` section at the
bottom holds senders flagged as scams: generic scraped pitches, domains that do
not match the company they claim, free-mail addresses posing as companies,
chat-app-first contact.

### Shortlist (data agent adds rows; email agent marks applied or rejected)

Tier, Company, Role, Location, Why it fits, Apply link, Where it's tracked,
Your notes. Tiers come from `config.yaml`. When a company has 3 or more
matching roles, use one row for the company and list the titles in Role.

### Watchlist (data agent)

| Col | Field |
|---|---|
| A | Company |
| B | Why on list (Applied, In process, Shortlist, Contacted, No openings, Careers page, AI company, ...) |
| C | Source tabs |
| D | Board type (Ashby, Greenhouse, Lever, Breezy, Recruitee, Workable, Gem, Other) |
| E | Board slug |
| F | Careers URL (board root) |
| G | Last job check |
| H | Notes |

This is the list of boards the data agent re-checks every run. A company goes
here only if it has a board or another qualifying fact, and never if it is on
Dead Ends.

### New Raises (data agent)

Week, Date, Project, Website, My Notes (name the source), Round, Amount ($m),
Est. valuation ($m), Investors, Top-fund investor, Category, On your list,
Details. Newest first.

### Companies (data agent)

Companies found from category lists rather than from jobs: Project, Status,
Your notes, Website, Careers URL. Highlight the Careers URL cell yellow when no
careers page was found, so you can search by hand.

### Dead Ends (both read)

Company and reason. Nothing on this tab gets added anywhere else.

## Sheet gotchas

- A value that starts with `=` is read as a formula. Prefix it with `'`.
- The Sheets connector has a per-minute read quota. On a quota error, wait about
  a minute and retry.
- Appending with a one-row range such as `Watchlist!A1:H1` adds rows after the
  last row and avoids off-by-one range errors.
