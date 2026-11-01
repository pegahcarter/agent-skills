# Free source catalog

Everything here was free and worked without a login when last checked
(October 2026). Sites change; treat each note as "last observed", and re-check
before relying on it. Never use a paid plan, sign in, or get past a bot check.

## Employer job boards (public, no key)

These are where every lead gets verified. `scripts/ats_check.py` reads them.

| Board | Endpoint | Posting date field | Notes |
|---|---|---|---|
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/SLUG` | `publishedAt` | Returns 403 to Python's default User-Agent; send a browser User-Agent. Add `?includeCompensation=true` for pay. |
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/SLUG/jobs` | none | `updated_at` is not a posting date; some boards show the same recent date on every role. `/jobs/ID?pay_transparency=true` gives the description. |
| Lever | `https://api.lever.co/v0/postings/SLUG?mode=json` | `createdAt` (ms) | |
| Breezy | `https://SLUG.breezy.hr/json` | `published_date` | |
| Gem | `https://api.gem.com/job_board/v0/SLUG/job_posts/` | `first_published_at` | |
| Recruitee | `https://COMPANY-DOMAIN/api/offers/` | `published_at` | Some companies post one role per country, so dedupe by title. |

Short slugs give false hits: a slug that matches a common word often belongs to
a different company. Confirm the board is the right company from the job
description text or the company's own careers page footer. Some companies run
two boards, and many use none of the above (BambooHR, Workday, Rippling, a
custom page).

## Job aggregators

**web3.career Jobs API** (free token). `https://web3.career/api/v1?token=TOKEN&tag=TAG&remote=true&limit=100&show_description=false`.
Limit 1 to 100, no offset, so merge tags and sort by date. Rows have date
(RFC 2822 string), title, location, apply_url and salary; there is no company
field, and the company follows " at " in the title. Wait about 7 seconds
between calls. Many tags return nothing; test new tags once and keep the ones
with recent rows. With the 100-row cap, busy tags reach back only weeks.

**hashtagweb3.com** (public JSON). `https://hashtagweb3.com/data/jobs-runtime.json`,
about 1,500 rows, roughly the last month. Each row has title, company, link
(the employer's own posting), date, source (board type and slug), location,
active, and sometimes salary. curl with a browser User-Agent. `/api/jobs` is not
deployed.

**Himalayas search API** (public). `https://himalayas.app/jobs/api/search?q=QUERY&sort=recent&page=N`,
20 rows per page; `page` works, `offset` does not. `pubDate` is Unix seconds.
`locationRestrictions` is a country list. `applicationLink` is a Himalayas page,
not the employer's. Loose search: general queries return many large non-target
employers and some staffing agencies. Wait about 3 seconds between calls.

**cryptocurrencyjobs.co** (server-rendered HTML). Category pages
(`/engineering/`, `/security/`, `/remote/`) show 50 cards; page 2 returns 404.
Attributes are unquoted (`<time datetime=2026-10-19T12:57:16>`). Some cards
carry a refreshed date at 08:00:00 even for old roles, so confirm the posting
date on the employer's board.

## VC portfolio job boards

**Getro boards** (many crypto and AI funds). POST
`https://api.getro.com/api/v2/collections/ID/search/jobs` with
`content-type: application/json`, `accept: application/json` and an `origin`
header for any Getro board, body `{"hitsPerPage":20,"page":N,"query":""}`.
An empty query returns all jobs, newest first; hitsPerPage is capped at 20.
Wait about 4 seconds between calls; faster calls return an empty body. The
collection id is in the board page's `__NEXT_DATA__`
(`props.pageProps.network.id`). Ignore placeholder organizations that repost
other listings.

**Consider boards** (for example a16z and Pantera). Browser only; the API
rejects shell calls with a CSRF error. Click "Show more jobs" until the last
loaded job is older than the cutoff, then read `document.body.innerText` and
split on the "Apply" separator. Keep output compact to avoid truncation. a16z's
list can be filtered by market with a URL parameter; read the parameter value
from the filter control rather than guessing it.

## Funding rounds

**DefiLlama raises.** Read the page; the raises API needs a paid plan.

**RootData fundraising** (browser, no login). First 30 rows per tag filter;
page 2 needs a login. In page JavaScript, do not return the page URL (query
strings get blocked), and re-run `find` before each click because element
references go stale.

**DropsTab latest rounds** (browser). First 50 rows free. CryptoRank shows only
the latest 20 with amounts hidden, so use it only to spot names.

**Crunchbase News** (free articles, web fetch). The weekly "biggest funding
rounds" article has a full table without a paywall. Do not sign in.

**StartupHub.ai recent funding rounds** (web fetch). About 50 rounds covering
roughly the last 8 days, no page 2. Company names link to StartupHub profiles,
not to the company.

**FinSMEs** (browser; web fetch returned a stale copy). Paginate the country
category until a post is older than the cutoff. Titles read "X Raises $NM in
Series Y Funding", so the company, amount and round can come from the title.

**NeuronFeed AI funding** (web fetch). 30 rows per page, month only in the
list; open a row for the exact date.

## Company lists

**CoinMarketCap categories** (free Basic key, header `X-CMC_PRO_API_KEY`).
`/v1/cryptocurrency/categories` and `/v1/cryptocurrency/category?id=ID`. The
`listings/new` and `trending` endpoints return an error on the free plan.

**RWA.xyz** (browser). Home and platform tables are free; CSV export, API and
MCP access are paid. Each table renders as a name table plus a data table.

## Tried and not used

TechCrunch venture (mostly events and acquisitions), SEC Form D search (mostly
funds and SPVs), FundUp (bot check, account needed), Seedtable (10 rows without
sign-in), Axios Pro Rata (would not load). Recheck occasionally.
