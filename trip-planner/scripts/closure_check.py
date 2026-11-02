#!/usr/bin/env python3
"""Flag planned visits that fall on a day the place is closed.

Usage:
    closure_check.py --year 2026 TRACKER.csv [TRACKER.csv ...]

Each CSV is an export of a tracker tab (restaurants, producers, sights). The
script uses three columns, found by header name, case-insensitive:

    Name         the place
    Visit date   one date or several, e.g. "12 Sep", "2026-09-12",
                 "9/12/2026", "Sep 15-16", "12 Sep; 14 Sep"
    Closed days  weekdays the place is closed, e.g. "Mon", "Sun, Mon",
                 "Mon-Tue". Blank means unknown and is reported as such.

Prints CONFLICT for any visit date on a closed day, and UNKNOWN for rows with
a visit date but no closed-days value, since an unknown closing day is the
usual way a dinner plan fails. Exit code 1 on any conflict. Standard library
only.
"""
import argparse
import csv
import re
import sys
from datetime import date

MONTHS = {m: i for i, m in enumerate(
    "jan feb mar apr may jun jul aug sep oct nov dec".split(), start=1)}
DAYS = "mon tue wed thu fri sat sun".split()
NAME_KEYS = ("name", "restaurant name", "option", "place", "hotel name")
DATE_KEYS = ("visit date", "date", "date(s)", "date / location")
CLOSED_KEYS = ("closed days", "closed", "closing days")


def find_col(header, keys):
    low = [h.strip().lower() for h in header]
    for k in keys:
        if k in low:
            return low.index(k)
    return None


def parse_dates(text, year):
    text = text.split("\n")[0]
    out = []
    for m in re.finditer(r"(\d{4})-(\d{2})-(\d{2})", text):
        out.append(date(int(m[1]), int(m[2]), int(m[3])))
    for m in re.finditer(r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b", text):
        out.append(date(int(m[3]), int(m[1]), int(m[2])))
    if out:
        return out
    # "12 Sep", "12-14 Sep"
    for m in re.finditer(r"\b(\d{1,2})(?:\s*[-–]\s*(\d{1,2}))?\s+([A-Za-z]{3})[a-z]*\b", text):
        mo = MONTHS.get(m[3].lower())
        if mo:
            lo, hi = int(m[1]), int(m[2] or m[1])
            out += [date(year, mo, d) for d in range(lo, hi + 1)]
    # "Sep 12", "Sep 15-16"
    for m in re.finditer(r"\b([A-Za-z]{3})[a-z]*\s+(\d{1,2})(?:\s*[-–]\s*(\d{1,2}))?\b", text):
        mo = MONTHS.get(m[1].lower())
        if mo:
            lo, hi = int(m[2]), int(m[3] or m[2])
            out += [date(year, mo, d) for d in range(lo, hi + 1)]
    return sorted(set(out))


def parse_closed(text):
    days = set()
    for part in re.split(r"[,;/]|\band\b", text.lower()):
        part = part.strip()
        rng = re.match(r"([a-z]{3})[a-z]*\s*[-–]\s*([a-z]{3})", part)
        if rng and rng[1] in DAYS and rng[2] in DAYS:
            i, j = DAYS.index(rng[1]), DAYS.index(rng[2])
            k = i
            while True:
                days.add(DAYS[k])
                if k == j:
                    break
                k = (k + 1) % 7
        elif part[:3] in DAYS:
            days.add(part[:3])
    return days


def check(rows, year):
    conflicts, unknown = [], []
    for name, when, closed in rows:
        dates = parse_dates(when, year)
        if not dates:
            continue
        if not closed.strip():
            unknown.append(name)
            continue
        shut = parse_closed(closed)
        for d in dates:
            if DAYS[d.weekday()] in shut:
                conflicts.append((name, d, DAYS[d.weekday()].title()))
    return conflicts, unknown


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    for i, header in enumerate(rows[:3]):
        n, d, c = (find_col(header, k) for k in (NAME_KEYS, DATE_KEYS, CLOSED_KEYS))
        if n is not None and d is not None:
            body = rows[i + 1:]
            return [(r[n], r[d] if d < len(r) else "", r[c] if c is not None and c < len(r) else "")
                    for r in body if len(r) > n and r[n].strip()]
    raise SystemExit(f"{path}: no Name and Visit date columns in the first 3 rows")


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("files", nargs="+")
    a = ap.parse_args(argv)
    rows = [r for p in a.files for r in read(p)]
    conflicts, unknown = check(rows, a.year)
    for name, d, day in conflicts:
        print(f"CONFLICT  {name}: visit {d.isoformat()} is a {day}, listed as closed")
    for name in unknown:
        print(f"UNKNOWN   {name}: no closed days recorded")
    if not conflicts and not unknown:
        print("No conflicts.")
    return 1 if conflicts else 0


if __name__ == "__main__":
    sys.exit(main())
