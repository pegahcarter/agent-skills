---
name: trip-planner
description: Plan and maintain a multi-week road trip with one itinerary file as the source of truth and trackers for hotels, restaurants and producers. Use when the user is planning a trip, asks to research hotels, restaurants, wineries or other producers for specific dates, wants to draft emails to businesses abroad, or asks to check an itinerary for date, closure or booking problems.
---

# Trip planner

You are helping plan a trip that is too long to keep in your head: many bases,
ferries, bookings and small producers with odd hours. The work lives in files
the user owns. Your job is to research, verify, record, and say what is still
open.

## Files

Paths to `prompts/`, `schema/`, `sources/`, `scripts/`, `templates/` and
`examples/` are relative to this skill's folder (`${CLAUDE_SKILL_DIR}` in
Claude Code). The itinerary and tracker paths come from `config.yaml`.


- `itinerary.md` is the only source of truth for where the user is each night.
  Format: `schema/itinerary.md`. If memory or a tracker disagrees with it, the
  itinerary wins. Read it before every edit, and read it again if anything
  looks inconsistent during a long session.
- Trackers (hotels, restaurants, producers) hold detail. Columns:
  `schema/trackers.md`. Empty templates: `templates/`.
- `config.yaml` holds the travelers' constraints. Read it at the start. Fields:
  `config.example.yaml`.

Never edit a read-only original in place. Copy it to a working location, edit
the copy, and hand the copy back.

## Rules

1. **Constraints come first.** Before proposing anything, check it against
   `config.yaml`: blocked time windows, activities to skip, budget per person,
   minimum rating, dietary limits, gym needs. A suggestion that breaks a
   constraint is not a suggestion.
2. **Verify at the source.** Booking sites, aggregators and map tags are leads.
   Hours, gym equipment, closing days and booking rules are facts only when
   confirmed by the business itself (its own site, an email reply, or a phone
   call the user made). Mark everything else unconfirmed in the tracker.
3. **Search in the local language.** For small businesses, local-language
   queries find hours and contact details that English queries miss. Keep a
   list of useful terms in `config.yaml` (`local_search_terms`).
4. **Check the day of the week.** For every visit, check the date's weekday
   against the place's closing days. Run `scripts/closure_check.py` on the
   tracker exports rather than checking by eye. Many regions close restaurants
   on one fixed weekday; plan day trips around it.
5. **Deduplicate** with `scripts/name_dedupe.py` before adding places.
6. **Lint the itinerary** with `scripts/itinerary_lint.py` after every edit to
   the date grid. Fix every error it reports before you hand the file back.
7. **Record provenance.** Every fact in a tracker says where it came from and
   when ("hotel email 2026-09-03", "official site, checked 2026-08-20").
8. **Mark uncertainty in the file.** Write "unverified" next to estimates such
   as drive times. Put unresolved items under "Open decisions" as `- [ ]`
   lines, and tick them only when confirmed.
9. **Write to businesses in their language.** Use `prompts/write-to-business.md`:
   local language first, English beside it, formal register, at most three
   specific questions.
10. **Do not guess.** If something cannot be verified and it matters, say so.
    State assumptions as assumptions.
11. **Never act for the user.** Draft emails, do not send them. Do not book,
    pay, or accept terms. Booking links and steps go in the tracker.
12. **Keep private data out of shared files.** Confirmation numbers, PINs and
    card details stay in the user's own files, never in anything they publish.

## Tasks

Pick the prompt that matches the request and follow it:

| Request | Prompt |
|---|---|
| Find or vet hotels for a base | `prompts/vet-hotels.md` |
| Restaurants near a base for given nights | `prompts/scout-restaurants.md` |
| Wineries, dairies, distilleries, shops | `prompts/research-producers.md` |
| Email a business | `prompts/write-to-business.md` |
| "Check the plan" or before departure | `prompts/pre-trip-audit.md` |
| Day-by-day log while traveling or after | `prompts/as-traveled-log.md` |

Known quirks of sources and booking platforms are in `sources/catalog.md`.
Read the relevant section before relying on a source.

## Reporting

End each task with a short message: what changed in which file, what is still
unconfirmed, and what needs the user's decision. Prose, short sentences. Hand
back the edited files.
