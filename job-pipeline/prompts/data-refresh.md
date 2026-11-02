# Data refresh agent prompt

Fill every `{{PLACEHOLDER}}` from `config.yaml`. Give this task the sheet
connector, a shell, web fetch and browser access. Put API keys in the task
text only, in the KEYS block at the end, never in this repo.

Sources are lettered so the prompt can say where each one's pull date lives.
Delete the ones you do not use. Endpoints and quirks for each are in
`sources/catalog.md`.

---

Weekly free-data refresh for {{OWNER_NAME}}'s job search. It may also be run by
hand several times a week, so always use the recorded pull dates and skip
anything already on a tab. The data goes into the Google Sheet "{{SHEET_NAME}}"
(spreadsheet id {{SHEET_ID}}). The sheet is the only source of truth. Do not
create files, snapshots or spreadsheet copies (temporary scratch files for API
calls are fine).

This task only refreshes data sources. A separate task syncs email; do not read
email here and do not change Pipeline or Recruiters.

STEP 0: CHECK THE BROWSER (before anything else)
Several sources need a real browser. Load the browser tools and list the open
tabs. If the browser is not reachable, change nothing in the sheet and run no
other source. Send one short message saying the browser could not be reached,
the refresh did not run, and it needs to be run again. Then stop. If the
browser stops responding after you start, stop there and report which sources
finished and which did not.

TABS
Pipeline ({{TAB_PIPELINE}}, read only, for duplicate checks), Shortlist
({{TAB_SHORTLIST}}), Watchlist ({{TAB_WATCHLIST}}), New Raises
({{TAB_NEW_RAISES}}), Companies ({{TAB_COMPANIES}}), Dead Ends
({{TAB_DEAD_ENDS}}). Row 1 of each tab is a description with pull dates, row 2
the header. Layout is in schema/sheet.md.

PULL DATES
Pull only items newer than the last pull for each source. Pull dates are in row
1 of the tab the source writes to: Shortlist for job sources, Companies for
category sources, New Raises for funding sources. If you cannot find a date for
a source, skip it and say so in the report. When a source is done, append its
new pull date to that tab's row 1 in the same style.

DUPLICATES
Before adding anything, check it against every tab. Write the candidate names
to a scratch file and compare them with a script (scripts/name_dedupe.py), not
by eye. Skip anything already on a tab. Never add a company that is on Dead
Ends.

SCOPE
Roles: {{TARGET_ROLES}}. Individual contributor roles at levels
{{TARGET_LEVELS}}; skip managers, sales engineers, solutions architects, IT
support, design, product, marketing, sales, operations and recruiting.
Locations: {{ALLOWED_LOCATIONS}}. Skip {{EXCLUDED_REGIONS}} and in-person-only
roles. Skip staffing agencies. Company types to skip: {{EXCLUDED_COMPANY_TYPES}}.
Tiers: {{TIER_RULES}}.
Do not count roles that only mention a target term in passing (for example an
"AI sales" role).

VERIFY AT THE SOURCE
An aggregator row is a lead, not a fact. Add a role to Shortlist only after
confirming it is live on the employer's own board or careers page. If you
cannot confirm it, put it in the report as an unverified lead with the link and
what you tried. Before writing a stated fact about a company or round, confirm
it refers to that company (short board slugs often match a different company)
and that it is current.

WATCHLIST
Watchlist is the list of boards this task re-checks. After each source, for
every company you add to Shortlist, Companies (with a careers page) or New
Raises (with a board), check Watchlist column A. If it is not there, append one
row (Company, Why on list, Source tabs, Board type, Board slug, Careers URL,
Last job check, Notes). If it is there, add the new tab name to column C.

SOURCES (details in sources/catalog.md)
a) Job API with free token ({{SOURCE_A_URL}}). Merge all tags, sort by date,
   keep rows since the last pull. Wait between calls as the catalog says.
b) Category lists from a market data API with a free key. Finds companies, not
   jobs. Add new ones to Companies with their careers page.
c) Funding rounds page read in the browser (first page per filter only; later
   pages need a login).
d) Second funding rounds page read in the browser.
e) Hiring aggregator JSON file (public). Filter active rows since the last
   pull, then confirm each on the employer's board.
f) Remote job search API (public). Loose search: confirm on the employer's own
   board or list as unverified.
g) Watchlist board re-check. For every Watchlist row with a known board type
   and slug, run scripts/ats_check.py with --since set to the last pull date
   (for rows added since the last pull, use no date so all open roles print).
   Write today's date in column G for every row read. Run this source last, so
   companies added this run get their first check.
h) VC portfolio job boards (some by API, some only in the browser). Read the
   newest postings back to the cutoff rather than running many keyword
   searches.
i) Non-industry funding news pages (public articles). Keep rounds that meet
   {{RAISE_FILTER}}.
Not used, with reasons: {{SOURCES_NOT_USED}}.

RULES
- Free sources only. Never use a paid plan, never sign in, never try to pass a
  bot check or CAPTCHA.
- Never send, draft or reply to email.
- Close every browser tab you open.
- Do not guess.
- Write rows in batches, one call for many rows. On a Sheets quota error, wait
  about a minute and retry.
- A cell value starting with "=" is read as a formula; prefix it with "'".
- {{EXTRA_RULES}}

KEYS (only in the task text, never in the sheet, a kept file or the report)
{{KEYS_BLOCK}}
If a call fails with an auth error, report it instead of retrying more than
twice.

REPORT
Send one short message: (a) changes made to the sheet; (b) new Shortlist roles
and companies (names for top-tier roles, counts for the rest), Watchlist rows
added, New Raises rows added per source group; (c) anything that needs a
decision: skipped or failed sources, boards that failed to load, assumptions
you made, and unverified leads. Plain prose, short sentences. If nothing
changed, say so in one sentence.
