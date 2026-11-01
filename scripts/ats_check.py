#!/usr/bin/env python3
"""List open engineering roles from public job board APIs.

Usage:
    ats_check.py [--since YYYY-MM-DD] [--pattern REGEX] BOARD:SLUG [...]

BOARD is one of ashby, greenhouse, lever, breezy, gem. Prints one tab-separated
line per matching role: board, slug, date, title, location, url. Roles with no
posting date (Greenhouse) are printed with "updated:" before the date and are
not filtered by --since, because Greenhouse only exposes an update time.

Standard library only.
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")

DEFAULT_PATTERN = (
    r"engineer|developer|smart contract|solidity|protocol|backend|back-end|"
    r"full.?stack|frontend|front-end|infrastructure|platform|security|"
    r"\bml\b|machine learning|\bai\b|llm|inference|agentic|research engineer|evals?"
)
EXCLUDE = r"manager|director|head of|recruit|sales|marketing|designer|intern|new grad|junior"


def board_url(board, slug):
    s = urllib.parse.quote(slug)
    return {
        "ashby": f"https://api.ashbyhq.com/posting-api/job-board/{s}",
        "greenhouse": f"https://boards-api.greenhouse.io/v1/boards/{s}/jobs",
        "lever": f"https://api.lever.co/v0/postings/{s}?mode=json",
        "breezy": f"https://{s}.breezy.hr/json",
        "gem": f"https://api.gem.com/job_board/v0/{s}/job_posts/",
    }[board]


def _iso(value):
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        secs = value / 1000 if value > 1e11 else value
        return datetime.fromtimestamp(secs, tz=timezone.utc)
    v = str(value).replace("Z", "+00:00")
    try:
        d = datetime.fromisoformat(v)
    except ValueError:
        try:
            d = datetime.strptime(v[:10], "%Y-%m-%d")
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def normalize(board, data):
    """Return a list of dicts: title, location, url, date, date_is_posting."""
    out = []
    if board == "ashby":
        for j in data.get("jobs", []):
            out.append(dict(title=j.get("title", ""), location=j.get("location", ""),
                            url=j.get("jobUrl", ""), date=_iso(j.get("publishedAt")),
                            date_is_posting=True))
    elif board == "greenhouse":
        for j in data.get("jobs", []):
            out.append(dict(title=j.get("title", ""),
                            location=(j.get("location") or {}).get("name", ""),
                            url=j.get("absolute_url", ""), date=_iso(j.get("updated_at")),
                            date_is_posting=False))
    elif board == "lever":
        for j in data if isinstance(data, list) else []:
            cats = j.get("categories") or {}
            out.append(dict(title=j.get("text", ""), location=cats.get("location", ""),
                            url=j.get("hostedUrl", ""), date=_iso(j.get("createdAt")),
                            date_is_posting=True))
    elif board == "breezy":
        for j in data if isinstance(data, list) else []:
            loc = j.get("location") or {}
            out.append(dict(title=j.get("name", ""),
                            location=loc.get("name", "") if isinstance(loc, dict) else str(loc),
                            url=j.get("url", ""), date=_iso(j.get("published_date")),
                            date_is_posting=True))
    elif board == "gem":
        rows = data if isinstance(data, list) else data.get("job_posts", data.get("data", []))
        for j in rows:
            loc = j.get("location") or {}
            out.append(dict(title=j.get("title", ""),
                            location=loc.get("name", "") if isinstance(loc, dict) else str(loc),
                            url=j.get("absolute_url", j.get("url", "")),
                            date=_iso(j.get("first_published_at") or j.get("created_at")),
                            date_is_posting=True))
    return out


def select(jobs, since=None, pattern=DEFAULT_PATTERN, exclude=EXCLUDE):
    inc, exc = re.compile(pattern, re.I), re.compile(exclude, re.I)
    keep = []
    for j in jobs:
        if not inc.search(j["title"]) or exc.search(j["title"]):
            continue
        if since and j["date_is_posting"] and (j["date"] is None or j["date"] < since):
            continue
        keep.append(j)
    keep.sort(key=lambda j: j["date"] or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return keep


def fetch(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("boards", nargs="+", help="BOARD:SLUG, e.g. ashby:examplecorp")
    ap.add_argument("--since", help="YYYY-MM-DD; keep roles posted on or after this date")
    ap.add_argument("--pattern", default=DEFAULT_PATTERN, help="title regex to keep")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between boards")
    a = ap.parse_args(argv)
    since = _iso(a.since) if a.since else None
    failed = 0
    for i, spec in enumerate(a.boards):
        board, _, slug = spec.partition(":")
        if board not in ("ashby", "greenhouse", "lever", "breezy", "gem") or not slug:
            print(f"skip\t{spec}\tbad BOARD:SLUG", file=sys.stderr)
            failed += 1
            continue
        if i:
            time.sleep(a.delay)
        try:
            jobs = normalize(board, fetch(board_url(board, slug)))
        except (urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
            print(f"fail\t{spec}\t{e}", file=sys.stderr)
            failed += 1
            continue
        for j in select(jobs, since, a.pattern):
            d = j["date"].strftime("%Y-%m-%d") if j["date"] else "-"
            if not j["date_is_posting"]:
                d = "updated:" + d
            print("\t".join([board, slug, d, j["title"], j["location"], j["url"]]))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
