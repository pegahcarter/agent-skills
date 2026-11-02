#!/usr/bin/env python3
"""Check an itinerary file for the mistakes that are easy to make by hand.

Usage:
    itinerary_lint.py ITINERARY.md

The file follows schema/itinerary.md: a header line such as

    **Dates:** Fri 11 Sep - Thu 8 Oct 2026 (27 nights)

and a date grid table with the columns Date | Day | Start | End | Notes.

Checks:
  - every weekday in the grid matches its date
  - dates are consecutive, with no gaps or repeats
  - each row starts where the previous row ended
  - the grid covers the header's first and last date
  - the night count in the header matches the dates
Also lists, without failing:
  - rows that contain an "unverified" or "TBD" marker
  - unchecked items under "Open decisions"

Exit code 1 if any check fails. Standard library only.
"""
import re
import sys
from datetime import date, timedelta

MONTHS = {m: i for i, m in enumerate(
    "jan feb mar apr may jun jul aug sep oct nov dec".split(), start=1)}
DAYS = "mon tue wed thu fri sat sun".split()
HEADER_RE = re.compile(
    r"\*\*Dates:\*\*\s*(\w{3})\s+(\d{1,2})\s+(\w{3})(?:\s+(\d{4}))?\s*[-–—]+\s*"
    r"(\w{3})\s+(\d{1,2})\s+(\w{3})\s+(\d{4})\s*\((\d+)\s+nights?\)", re.I)
ROW_RE = re.compile(r"^\|\s*(\d{1,2})\s+(\w{3})\s*\|\s*(\w{3})\s*\|([^|]*)\|([^|]*)\|(.*)\|\s*$")
FLAG_RE = re.compile(r"\bunverified\b|\bTBD\b|\bnot yet (chosen|booked|confirmed)\b", re.I)


def month(token):
    return MONTHS[token[:3].lower()]


def parse_header(text):
    m = HEADER_RE.search(text)
    if not m:
        return None
    _, sd, sm, sy, _, ed, em, ey, nights = m.groups()
    end = date(int(ey), month(em), int(ed))
    start_year = int(sy) if sy else (end.year - 1 if month(sm) > month(em) else end.year)
    start = date(start_year, month(sm), int(sd))
    return start, end, int(nights)


def parse_grid(text, start_year):
    rows, year, last_month = [], start_year, None
    for line in text.splitlines():
        m = ROW_RE.match(line.strip())
        if not m:
            continue
        d, mon, day, start, end, notes = m.groups()
        mo = month(mon)
        if last_month and mo < last_month:
            year += 1
        last_month = mo
        rows.append({
            "date": date(year, mo, int(d)), "day": day.lower(),
            "start": start.strip(), "end": end.strip(), "notes": notes.strip(),
            "label": f"{d} {mon}",
        })
    return rows


def open_decisions(text):
    part = re.split(r"^#+\s*Open decisions\s*$", text, flags=re.I | re.M)
    if len(part) < 2:
        return []
    section = re.split(r"^#+\s", part[1], flags=re.M)[0]
    return [l.strip()[6:].strip() for l in section.splitlines() if l.strip().startswith("- [ ]")]


def lint(text):
    errors, notes = [], []
    header = parse_header(text)
    if not header:
        return ["No '**Dates:** ... (N nights)' header found."], notes
    start, end, nights = header
    if (end - start).days != nights:
        errors.append(f"Header says {nights} nights, but {start} to {end} is {(end - start).days}.")
    rows = parse_grid(text, start.year)
    if not rows:
        return errors + ["No date grid rows found."], notes
    if rows[0]["date"] != start:
        errors.append(f"Grid starts {rows[0]['date']}, header starts {start}.")
    if rows[-1]["date"] != end:
        errors.append(f"Grid ends {rows[-1]['date']}, header ends {end}.")
    for i, r in enumerate(rows):
        actual = DAYS[r["date"].weekday()]
        if r["day"][:3] != actual:
            errors.append(f"{r['label']}: listed as {r['day'].title()}, actually {actual.title()}.")
        if i:
            prev = rows[i - 1]
            if r["date"] != prev["date"] + timedelta(days=1):
                errors.append(f"{r['label']}: does not follow {prev['label']} (gap or repeat).")
            if r["start"].lower() != prev["end"].lower():
                errors.append(f"{r['label']}: starts at '{r['start']}' but {prev['label']} ended at '{prev['end']}'.")
        if FLAG_RE.search(r["notes"]):
            notes.append(f"{r['label']}: has an unverified or TBD item.")
    for item in open_decisions(text):
        notes.append(f"Open: {item}")
    return errors, notes


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip().splitlines()[2], file=sys.stderr)
        return 2
    with open(argv[1], encoding="utf-8") as f:
        errors, notes = lint(f.read())
    print("ERRORS" if errors else "ERRORS: none")
    for e in errors:
        print("  " + e)
    print("TO CHECK" if notes else "TO CHECK: none")
    for n in notes:
        print("  " + n)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
