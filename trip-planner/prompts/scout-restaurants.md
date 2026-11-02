# Scout restaurants

Input: base, night(s), and the restaurant rules in `config.yaml` (meals,
budget per person, minimum rating, dietary limits, walking preference).

1. Read the itinerary rows for those nights. Note the hotel address and what
   the day involves (a long drive day means near the hotel).
2. Check the weekday of each night. Find which local restaurants close that
   day before you search. In many regions one weekday is the common closing
   day.
3. Search in English and the local language. Favor places locals return to
   over places near the main sight that are priced for tour groups.
4. For each candidate, collect two independent ratings with review counts.
   If listings disagree a lot (the same place under two names with very
   different scores), say so in the notes and say which you trust and why.
5. Do not trust map category tags. A "winery" tag can be a seafood
   restaurant. Confirm what the place is from its own menu or site.
6. Record the closed days. If you cannot find them, leave the cell blank so
   `closure_check.py` reports it as unknown.
7. Deduplicate with `scripts/name_dedupe.py`, then add rows.
8. Run `scripts/closure_check.py` on the export. Fix or flag every conflict.
9. Report: two or three picks per night with one line each on why, plus any
   that need a reservation.
