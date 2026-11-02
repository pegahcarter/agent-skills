# Pre-trip audit

Run when the user asks to check the plan, after a big edit, and in the last
two weeks before departure.

1. Run `scripts/itinerary_lint.py` on the itinerary (path in `config.yaml`). Fix every error.
2. Export the trackers to CSV and run
   `scripts/closure_check.py --year YYYY exports/*.csv`. Resolve each
   CONFLICT. For each UNKNOWN that is a dinner or a planned visit, find the
   closing day or draft an email.
3. For each night in the grid, check the hotels tracker has a row whose dates
   cover it. List nights with no hotel.
4. For each ferry, train or flight in the grid, check the operator and time
   against the current published timetable. Seasonal routes thin out at the
   ends of the season; say which ones you could not confirm.
5. For every drive marked "unverified", get a current estimate and replace
   the marker with the time and its source, or leave it and say so.
6. Hotels with conditions: late arrival notice, parking that needs advance
   contact, non-refundable bookings that depend on an unconfirmed ferry.
   List each with the date it must be handled by.
7. Cancellation deadlines: list every free-cancellation date still ahead,
   soonest first.
8. Report in three parts: fixed now, needs the user's action (with dates),
   and still unverifiable.
