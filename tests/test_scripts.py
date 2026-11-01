import csv
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import ats_check  # noqa: E402
import name_dedupe  # noqa: E402

UTC = timezone.utc


class AtsCheck(unittest.TestCase):
    def test_ashby_filters_by_title_and_date(self):
        data = {"jobs": [
            {"title": "Senior Smart Contract Engineer", "location": "Remote US",
             "jobUrl": "u1", "publishedAt": "2026-10-20T10:00:00.000Z"},
            {"title": "Backend Engineer", "location": "Remote",
             "jobUrl": "u2", "publishedAt": "2026-09-01T10:00:00.000Z"},
            {"title": "Engineering Manager", "location": "Remote",
             "jobUrl": "u3", "publishedAt": "2026-10-25T10:00:00.000Z"},
            {"title": "Account Executive", "location": "NYC",
             "jobUrl": "u4", "publishedAt": "2026-10-25T10:00:00.000Z"},
        ]}
        jobs = ats_check.normalize("ashby", data)
        keep = ats_check.select(jobs, since=datetime(2026, 10, 1, tzinfo=UTC))
        self.assertEqual([j["url"] for j in keep], ["u1"])

    def test_lever_millisecond_timestamps(self):
        ms = int(datetime(2026, 10, 15, tzinfo=UTC).timestamp() * 1000)
        jobs = ats_check.normalize("lever", [
            {"text": "ML Engineer", "categories": {"location": "Remote"},
             "hostedUrl": "x", "createdAt": ms}])
        self.assertEqual(jobs[0]["date"].date().isoformat(), "2026-10-15")
        self.assertEqual(len(ats_check.select(jobs, since=datetime(2026, 10, 1, tzinfo=UTC))), 1)

    def test_greenhouse_updated_date_is_not_filtered(self):
        jobs = ats_check.normalize("greenhouse", {"jobs": [
            {"title": "Protocol Engineer", "location": {"name": "Remote"},
             "absolute_url": "g", "updated_at": "2026-01-01T00:00:00-05:00"}]})
        self.assertFalse(jobs[0]["date_is_posting"])
        self.assertEqual(len(ats_check.select(jobs, since=datetime(2026, 10, 1, tzinfo=UTC))), 1)

    def test_ai_titles_match_but_ai_sales_does_not(self):
        jobs = [dict(title=t, location="", url=t, date=None, date_is_posting=False)
                for t in ["Applied AI Engineer", "LLM Inference Engineer",
                          "AI Sales Lead", "Research Engineer, Evals"]]
        titles = [j["title"] for j in ats_check.select(jobs)]
        self.assertEqual(sorted(titles), ["Applied AI Engineer", "LLM Inference Engineer",
                                          "Research Engineer, Evals"])

    def test_bad_spec_returns_nonzero(self):
        self.assertEqual(ats_check.main(["nosuchboard:x"]), 1)


class NameDedupe(unittest.TestCase):
    def test_suffixes_and_parentheses(self):
        self.assertEqual(name_dedupe.normalize("Acme Labs, Inc."), "acme")
        self.assertEqual(name_dedupe.cell_keys("Widget (Widget Protocol)"), {"widget"})

    def test_check_against_csv_tabs(self):
        with tempfile.TemporaryDirectory() as d:
            p1, p2 = Path(d, "Shortlist.csv"), Path(d, "DeadEnds.csv")
            with open(p1, "w", newline="") as f:
                csv.writer(f).writerows([["Tier", "Company"], ["1", "Acme Labs"]])
            with open(p2, "w", newline="") as f:
                csv.writer(f).writerows([["Company"], ["Globex (Globex Finance)"]])
            new, found = name_dedupe.check(["ACME", "Globex", "Initech"],
                                           name_dedupe.index_tabs([p1, p2]))
            self.assertEqual([n for n, _ in new], ["Initech"])
            self.assertEqual(dict(found), {"ACME": ["Shortlist.csv"], "Globex": ["DeadEnds.csv"]})


if __name__ == "__main__":
    unittest.main()
