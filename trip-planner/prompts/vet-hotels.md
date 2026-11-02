# Vet hotels for a base

Input: a base town, check-in and check-out dates, and `config.yaml`.

1. Read the itinerary row for each night. Confirm the base and dates there,
   not from memory.
2. Find candidates. Filter on the constraints in `config.yaml` (budget,
   parking if there is a car, gym needs, distance to what the days need).
3. For each candidate, collect: price, parking and its cost, check-in and
   check-out times, late check-out terms, breakfast hours, cancellation terms.
4. **Gym.** Do not trust the amenity list on a booking site. It often says
   "fitness center" for a room with one bike, or leaves out a good gym. Check
   the hotel's own site for photos and equipment. If the traveler needs a
   specific machine or early access, draft an email to the hotel
   (`prompts/write-to-business.md`) asking: what equipment, what hours, and
   whether staff can open it earlier. Early access before the posted time is
   rare but sometimes possible through the night porter.
5. **Arrival time.** If the drive or ferry gets in late, check whether the
   hotel needs notice for late arrival, and add it to Open decisions.
6. **Nearby cafes.** List up to three with opening time and walking distance,
   earliest first. If none are walkable, say so instead of padding the list.
7. Check the hotel is still operating. A listing can outlive the business.
8. Add rows to the hotels tracker. Mark unconfirmed fields yellow.
9. Report: the short list with the trade-off for each, what you could not
   confirm, and the emails you drafted.

Do not book. Booking links go in the Notes column.
