import csv
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import closure_check  # noqa: E402
import itinerary_lint  # noqa: E402
import name_dedupe  # noqa: E402

GOOD = """**Dates:** Fri 14 May – Mon 17 May 2027 (3 nights)

| Date | Day | Start | End | Notes |
|---|---|---|---|---|
| 14 May | Fri | LIS | Lisbon | Arrive |
| 15 May | Sat | Lisbon | Lisbon | Drive time unverified |
| 16 May | Sun | Lisbon | Porto | |
| 17 May | Mon | Porto | LAX | |

## Open decisions

- [ ] Book dinner
- [x] Hotel booked
"""


class ItineraryLint(unittest.TestCase):
    def test_good_file_passes_and_lists_open_items(self):
        errors, notes = itinerary_lint.lint(GOOD)
        self.assertEqual(errors, [])
        self.assertIn("15 May: has an unverified or TBD item.", notes)
        self.assertIn("Open: Book dinner", notes)
        self.assertFalse(any("Hotel booked" in n for n in notes))

    def test_wrong_weekday(self):
        errors, _ = itinerary_lint.lint(GOOD.replace("| 15 May | Sat |", "| 15 May | Sun |"))
        self.assertTrue(any("actually Sat" in e for e in errors))

    def test_gap_and_broken_chain(self):
        text = GOOD.replace("| 16 May | Sun | Lisbon | Porto |", "| 16 May | Sun | Faro | Porto |")
        errors, _ = itinerary_lint.lint(text)
        self.assertTrue(any("starts at 'Faro'" in e for e in errors))
        errors, _ = itinerary_lint.lint(GOOD.replace("| 16 May | Sun | Lisbon | Porto | |\n", ""))
        self.assertTrue(any("gap or repeat" in e for e in errors))

    def test_night_count_mismatch(self):
        errors, _ = itinerary_lint.lint(GOOD.replace("(3 nights)", "(4 nights)"))
        self.assertTrue(any("Header says 4 nights" in e for e in errors))

    def test_year_rollover(self):
        text = """**Dates:** Thu 30 Dec 2027 – Sat 1 Jan 2028 (2 nights)
| 30 Dec | Thu | A | B | |
| 31 Dec | Fri | B | B | |
| 1 Jan | Sat | B | C | |
"""
        self.assertEqual(itinerary_lint.lint(text)[0], [])

    def test_sample_trip_passes(self):
        text = (ROOT / "examples/sample-trip/itinerary.md").read_text(encoding="utf-8")
        self.assertEqual(itinerary_lint.lint(text)[0], [])


class ClosureCheck(unittest.TestCase):
    def test_date_formats(self):
        y = 2026
        self.assertEqual(closure_check.parse_dates("2026-09-21", y), [date(2026, 9, 21)])
        self.assertEqual(closure_check.parse_dates("9/21/2026", y), [date(2026, 9, 21)])
        self.assertEqual(closure_check.parse_dates("Sep 15–16\nCala Gonone", y),
                         [date(2026, 9, 15), date(2026, 9, 16)])
        self.assertEqual(closure_check.parse_dates("21 Sep; 23 Sep", y),
                         [date(2026, 9, 21), date(2026, 9, 23)])

    def test_closed_ranges_wrap(self):
        self.assertEqual(closure_check.parse_closed("Mon-Tue"), {"mon", "tue"})
        self.assertEqual(closure_check.parse_closed("Sat–Mon"), {"sat", "sun", "mon"})
        self.assertEqual(closure_check.parse_closed("Sundays and Mondays"), {"sun", "mon"})

    def test_conflict_and_unknown(self):
        rows = [("Seafood place", "21 Sep", "Mon"),     # 21 Sep 2026 is a Monday
                ("Winery", "Sep 22", "Sun"),
                ("Cheese shop", "19 Sep", "")]
        conflicts, unknown = closure_check.check(rows, 2026)
        self.assertEqual([c[0] for c in conflicts], ["Seafood place"])
        self.assertEqual(unknown, ["Cheese shop"])

    def test_reads_csv_by_header(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "r.csv"
            with open(p, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["Restaurant name", "Visit date", "Closed days"])
                w.writerow(["A", "2026-09-21", "Mon"])
            self.assertEqual(closure_check.main(["--year", "2026", str(p)]), 1)


class NameDedupe(unittest.TestCase):
    def test_filler_and_accents(self):
        self.assertEqual(name_dedupe.normalize("Trattoria Da Maria"), name_dedupe.normalize("Da María"))
        self.assertEqual(name_dedupe.normalize("Cantina di Santadi"), "santadi")

    def test_check(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "t.csv"
            p.write_text("Name,Notes\nRistorante Da Maria,good\n", encoding="utf-8")
            new, found = name_dedupe.check(["Da Maria", "Other Place"], name_dedupe.index_files([p]))
            self.assertEqual(new, ["Other Place"])
            self.assertEqual(found[0][0], "Da Maria")


if __name__ == "__main__":
    unittest.main()
