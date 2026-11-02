# Itinerary format

One Markdown file per trip. It is the only record of where the travelers are
each night. `scripts/itinerary_lint.py` reads it, so keep the header line and
the date grid in exactly this shape.

## Header

```
# <Trip name>

**Dates:** Fri 11 Sep – Thu 8 Oct 2026 (27 nights)
**In:** <home airport> → <arrival airport> · **Out:** <departure airport> → <home airport>
**Party:** 2 adults
**Style:** one line on what the trip is for
```

The `**Dates:**` line must give weekday, day and month for both ends, the year
at least once, and the night count. The linter checks the night count against
the dates.

## Date grid

```
| Date | Day | Start | End | Notes |
|---|---|---|---|---|
| 11 Sep | Fri | FCO | Rome | Arrive. Car picked up on landing. |
| 12 Sep | Sat | Rome | Rome | ... |
```

One row per calendar day, from arrival day to departure day, so a 27-night trip
has 28 rows. `Start` of each row must equal `End` of the row before. The linter
checks weekdays, gaps, repeats and the Start/End chain, and handles a trip
that crosses New Year.

Put in Notes what the traveler needs on that day: transport with times and
operator, the hotel for that night, timing limits ("last ferry 18:35"), and why
the day is planned the way it is ("Sunday because both restaurants close
Monday"). Write "unverified" next to any estimate; the linter lists those rows.

## Detail sections

Free-form sections after the grid for legs that need more than a cell: a
transit network, a car plan, a day with alternatives. Keep facts here
consistent with the grid. When they disagree, fix both in the same edit.

## Open decisions

```
## Open decisions

- [ ] Confirm the Sep 15 ferry against the published timetable
- [x] Hotel for Sep 26-29 booked
```

Every unresolved item goes here as `- [ ]`. Tick it only when confirmed by the
source, and put the confirmation in the line. The linter lists unticked items.

## What stays out

If the file will be shared or published, remove confirmation numbers, PINs,
card names and personal names first. In a private working copy they are
useful; keep them there.
