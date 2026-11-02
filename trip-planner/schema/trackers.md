# Trackers

Three spreadsheets (or three tabs of one). The itinerary says where you are;
the trackers hold everything you need to know about each place. Empty CSV
templates with these headers are in `templates/`. Work in .xlsx or a Google
Sheet if you prefer; export to CSV to run the scripts.

## Status colors

Use the same fill colors in every tracker so status reads at a glance.

| Color | Meaning |
|---|---|
| Green | Confirmed by the business |
| Blue | Confirmed, but needs a booking |
| Amber | Unconfirmed |
| Grey | Decision pending |
| Yellow (single cell) | That one field is unconfirmed. Clear the fill when confirmed. |

When you add a row, copy the style from an existing row and set the fill
explicitly, so new rows do not inherit the wrong color.

## Hotels (`templates/hotels.csv`)

| Field | Notes |
|---|---|
| Date | Check-in to check-out, e.g. `9/11/2026 - 9/13/2026` |
| Hotel name | |
| Hotel address | |
| Total price paid (prepaid) | |
| Cost at check-in | City tax, parking, anything paid on arrival |
| Nights | |
| Parking (Y/N) | |
| Parking price per night | |
| Parking advance contact required (Y/N) | |
| Gym (incl. hours) | Equipment and earliest access, confirmed with the hotel |
| Check-in time | |
| Check-out time | Include late check-out terms and fees |
| Breakfast included (Y/N + hours) | |
| Platform booked on | |
| Free cancellation (Y/N + by date) | |
| Booking confirmation # | Private. Keep out of anything shared. |
| Notes | Front desk phone, arrival-time requirements, provenance |
| Card used | Private. Keep out of anything shared. |
| Nearby cafe #1 (earliest) / #2 / #3 | Opening time and walking distance |

## Restaurants (`templates/restaurants.csv`)

| Field | Notes |
|---|---|
| Visit date | Night(s) you might eat there |
| Location | Town |
| Name | |
| Cuisine / specialty | |
| Price range (pp) | |
| Address | |
| Distance from hotel | Say if it is an estimate |
| Closed days | Weekdays, e.g. `Mon` or `Sun, Mon`. Used by `closure_check.py`. |
| Notes from agent | Why it fits; flag split listings and odd ratings |
| Notes from traveler | |
| Reservations | Required, recommended, walk-in |
| Reservation contact | Phone, site or platform |
| Rating A / reviews A | e.g. TripAdvisor |
| Rating B / reviews B | e.g. Google |

Delete places you rule out. Do not keep flagged placeholder rows.

## Producers (`templates/producers.csv`)

Wineries, dairies, distilleries, shops, farms.

| Field | Notes |
|---|---|
| Name | |
| Visit date | Candidate date(s) and nearest base |
| What | One or two lines: what they make and why it is worth the stop |
| Type | Winery, dairy, distillery, shop, ... |
| Hours | Confirmed hours, or "Unconfirmed" with what you found |
| Closed days | Weekdays. Used by `closure_check.py`. |
| Practical notes | Drive time from base, booking rules, how it fits the day |
| Contact | Email, phone, site. Write "phone only" if there is no email. |
| Next steps | What to do next and who does it |
| Status | Confirmed hours, Book required, Unconfirmed, Decision pending |
