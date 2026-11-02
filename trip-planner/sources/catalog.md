# Source catalog and field notes

What was learned planning and taking a 27-night road trip through Italy
(Rome, Sardinia, Ischia, the Amalfi Coast and Cilento) in September and
October 2026. Each note is "last observed", not a permanent fact. Check
again before relying on one.

## How reliable each kind of source was

| Source | Reliable for | Not reliable for |
|---|---|---|
| The business's own site | Hours, menus, booking rules | Hours in shoulder season (often not updated) |
| An email reply from the business | Everything it answers | Questions it skipped, so ask at most three |
| Booking sites (OTAs) | Price, cancellation terms | Gym equipment and hours, parking details |
| Map listings | Location, rough rating | Category tags, closing days, whether still open |
| Aggregator rating sites | Spotting split listings | A single score; the same place can appear twice with very different ratings |
| Booking platforms for tastings | Whether a slot exists | The producer's walk-in hours |

## Search technique

- **Local-language queries.** For small producers and shops, Italian
  queries found hours and direct-sale details that English queries did not.
  Terms that worked: "orari apertura" (opening hours), "vendita diretta"
  (direct sales), "visita degustazione" (tasting visit). Put your own
  language's terms in `config.yaml`.
- **Hidden emails.** Several producer sites loaded their contact email with
  JavaScript, so a plain page fetch returned nothing. A web search for the
  business name plus "email" or the town often found it. Some producers had
  a phone number only.
- **Permanent closures.** A hotel still listed on booking sites had closed
  for good. Check recent reviews or the business's own site before shortlisting.

## Closures and timing

- **Weekly closing day.** In Italy, Monday was the usual restaurant closing
  day. Two day trips were moved to Sunday because the restaurants they were
  built around closed Monday. `scripts/closure_check.py` catches this.
- **Weekend producers.** Several small producers opened weekdays only, with
  weekends by reservation. A Sunday visit needed a booking days ahead.
- **Early sell-outs.** One well-known buffalo mozzarella dairy sold out
  before mid-morning, which conflicted with a no-morning constraint. The plan
  used two other dairies.
- **End of season.** In early October on the southern coast, boat
  excursions and some restaurants were already cutting back. Seasonal ferry
  routes ran through October but with fewer sailings. Recheck timetables in
  the last two weeks.

## Hotels

- **Gyms.** Booking-site amenity lists were wrong often enough to be
  useless for a traveler who needs a treadmill at a set time. Emailing the
  hotel worked. Access before 06:00 was rare; one hotel offered it through
  the night porter, one confirmed 24-hour access, and one declined 05:00 but
  offered 06:00.
- **Late check-out and car parking.** Hotels often offered late check-out
  for a fee, or for less, kept the car in the garage until evening. This
  made a day trip on check-out day possible.
- **Late arrival.** Some properties required notice for arrival after a set
  hour. Put the deadline in Open decisions.

## Ferries and driving

- **Day trips by foot.** Leaving the car at the port and crossing as a foot
  passenger was cheaper and avoided questions about whether the rental
  agreement covered the island.
- **Vehicle rules on islands change.** One island restricted non-resident
  cars in high season, but the 2026 rule applied only to residents of the
  surrounding region, so a rental from elsewhere was allowed. Check the
  current year's ordinance; do not reuse last year's answer.
- **Passenger caps.** One operator capped passengers on specific sailings
  that carried dangerous goods. The cap applied only to certain weekday
  departures, not to the whole route. Read the notice for the exact sailings.
- **Port queues.** Short car ferries with no booking had long queues at
  commute hours in season. Arrive early.
- **Comparing operators.** Where several operators ran the same crossing,
  a comparison site showed all timetables in one place.

## Booking platforms

Platforms used on the trip, for reference. Terms change; read them at
booking time.

- Hotels: Booking.com, Hotels.com, Expedia, Agoda, Super.com
- Ferries: Direct Ferries, Ferryhopper, operator sites
- Producer tastings: Winedering worked for several wineries that had no
  booking system of their own
- Excursions: GetYourGuide

## Customs

Bringing food home depends on your home country's rules. For a US
traveler in 2026, the general pattern was: fresh soft cheese not practical,
hard aged cheese vacuum-packed generally allowed, pork products not allowed.
Check the current rules for your country before buying.
