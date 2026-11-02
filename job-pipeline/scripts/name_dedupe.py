#!/usr/bin/env python3
"""Find which candidate company names are already on the sheet.

Usage:
    name_dedupe.py --candidates names.txt TAB.csv [TAB.csv ...]

names.txt has one name per line. Each CSV is an export of one tab; every cell
is checked, so the column layout does not matter. A name counts as present when
its normalized form matches a cell, or matches a name in parentheses inside a
cell (for example "Acme (Acme Labs)"). Normalizing drops case, punctuation and
common suffixes such as Labs, Inc, Protocol and Finance.

Prints two sections: NEW (not found) and ON SHEET (with the tab file it was
found in). Standard library only.
"""
import argparse
import csv
import re
import sys
from pathlib import Path

SUFFIXES = {
    "inc", "llc", "ltd", "labs", "lab", "protocol", "finance", "network",
    "foundation", "technologies", "technology", "ai", "io", "xyz", "co", "corp",
    "hq", "the",
}


def normalize(name):
    words = re.sub(r"[^a-z0-9]+", " ", name.lower()).split()
    core = [w for w in words if w not in SUFFIXES]
    return " ".join(core or words)


def cell_keys(cell):
    keys = set()
    cell = cell.strip()
    if not cell:
        return keys
    keys.add(normalize(re.sub(r"\(.*?\)", "", cell)))
    for inner in re.findall(r"\(([^)]*)\)", cell):
        keys.add(normalize(inner))
    keys.discard("")
    return keys


def index_tabs(paths):
    index = {}
    for p in paths:
        with open(p, newline="", encoding="utf-8") as f:
            for row in csv.reader(f):
                for cell in row:
                    for k in cell_keys(cell):
                        index.setdefault(k, set()).add(Path(p).name)
    return index


def check(candidates, index):
    new, found = [], []
    for name in candidates:
        tabs = set()
        for k in cell_keys(name):
            tabs |= index.get(k, set())
        (found if tabs else new).append((name, sorted(tabs)))
    return new, found


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--candidates", required=True)
    ap.add_argument("tabs", nargs="+")
    a = ap.parse_args(argv)
    names = [l.strip() for l in open(a.candidates, encoding="utf-8") if l.strip()]
    new, found = check(names, index_tabs(a.tabs))
    print("NEW")
    for n, _ in new:
        print(f"  {n}")
    print("ON SHEET")
    for n, tabs in found:
        print(f"  {n}\t{', '.join(tabs)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
