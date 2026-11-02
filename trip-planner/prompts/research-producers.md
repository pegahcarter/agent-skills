# Research producers

Wineries, dairies, distilleries, farm shops, specialty food makers. These are
small businesses. Their hours are the hardest facts on the trip to pin down
and the easiest to get wrong.

Input: a base or a driving leg, the candidate dates, and `config.yaml`.

1. Read the itinerary for those dates. Note the free windows, keeping the
   blocked windows in `config.yaml` free (for example, no visits before noon).
2. Find candidates near the base or within a short detour from the day's
   route. Give the detour in minutes.
3. Search for hours and contact details in the local language, using the
   terms in `config.yaml` (`local_search_terms`). These queries find posted
   hours, direct sales and tasting pages that English searches miss.
4. Many small producers hide their email behind JavaScript, so a page fetch
   shows nothing. Fall back to a web search for the address, or to a booking
   platform's profile. If only a phone number exists, write "phone only" in
   Contact, since the user will have to call.
5. Check the specific date. Weekend and holiday hours often differ, and "by
   reservation only" on weekends means a walk-in will fail.
6. Check what can come home. If the user is bringing food back, note customs
   limits for the product type (fresh dairy and meat are often not allowed;
   hard aged cheese vacuum-packed often is). Say this is general and the user
   should check their own country's rules.
7. Check timing limits. Some products sell out early in the day.
8. Deduplicate, add rows to the producers tracker with Status, then run
   `scripts/closure_check.py`.
9. Draft an email for each producer whose hours are unconfirmed
   (`prompts/write-to-business.md`).
10. Report: which producers fit which day, which need a booking, and which
    emails are ready to send.
