#!/usr/bin/env python3
"""Find which candidate places are already in the trackers.

Usage:
    name_dedupe.py --candidates names.txt TRACKER.csv [TRACKER.csv ...]

names.txt has one name per line. Every cell of every CSV is checked, so the
column layout does not matter. Normalizing drops case, accents, punctuation
and common words such as Ristorante, Trattoria, Cantina, Hotel and Bar, so
"Trattoria Da Maria" matches "Da Maria".

Prints NEW (not found) and ON TRACKER (with the file it was found in).
Standard library only.
"""
import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path

FILLER = {
    "the", "il", "la", "lo", "le", "i", "gli", "l", "el", "los", "las", "le", "les",
    "ristorante", "trattoria", "osteria", "pizzeria", "enoteca", "bar", "cafe",
    "caffe", "restaurant", "bistro", "cantina", "azienda", "agricola", "tenuta",
    "hotel", "albergo", "resort", "spa", "b", "and", "e", "di", "del", "della",
}


def normalize(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    words = re.sub(r"[^a-z0-9]+", " ", s.lower()).split()
    core = [w for w in words if w not in FILLER]
    return " ".join(core or words)


def index_files(paths):
    index = {}
    for p in paths:
        with open(p, newline="", encoding="utf-8") as f:
            for row in csv.reader(f):
                for cell in row:
                    key = normalize(cell.split("\n")[0]) if cell.strip() else ""
                    if key:
                        index.setdefault(key, set()).add(Path(p).name)
    return index


def check(candidates, index):
    new, found = [], []
    for name in candidates:
        hit = index.get(normalize(name))
        (found.append((name, sorted(hit))) if hit else new.append(name))
    return new, found


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidates", required=True)
    ap.add_argument("files", nargs="+")
    a = ap.parse_args(argv)
    with open(a.candidates, encoding="utf-8") as f:
        names = [l.strip() for l in f if l.strip()]
    new, found = check(names, index_files(a.files))
    print("NEW")
    for n in new:
        print("  " + n)
    print("ON TRACKER")
    for n, where in found:
        print(f"  {n}  ({', '.join(where)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
