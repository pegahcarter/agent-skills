# trip-planner

A Claude skill for planning a long road trip, with one itinerary file as the
only record of where you are each night.

It grew out of a 27-night trip through Italy: 14 overnight bases, 13 planned
ferry crossings, a rental car, and 26 small wineries, dairies and shops with
hours that were hard to pin down. The agent researched hotels, restaurants and
producers, drafted emails to businesses in Italian, kept three trackers
current, and caught the planning mistakes that are easy to make by hand: a
weekday that does not match its date, a night with no hotel, a dinner booked
on the restaurant's closing day.

This skill holds the instructions, the file formats, task prompts, a
catalog of what each kind of source was and was not reliable for, and three
small scripts the agent runs from a shell. It contains no trip data. You
bring your own itinerary, trackers and constraints.

## How it works

```
                      config.yaml
              (constraints: time windows, budget,
               rating floor, gym, language)
                           │
                           ▼
   ┌───────────────────────────────────────────────┐
   │ Agent (SKILL.md + one prompt per task)         │
   │ web search, local-language queries, drafting   │
   └──────┬───────────────────┬────────────────────┘
          │ edits              │ edits
          ▼                    ▼
   ┌──────────────┐    ┌───────────────────────────┐
   │ itinerary.md │    │ trackers                  │
   │ source of    │◄───┤ hotels / restaurants /    │
   │ truth        │    │ producers (status colors) │
   └──────┬───────┘    └────────────┬──────────────┘
          │                         │ CSV export
          ▼                         ▼
   itinerary_lint.py        closure_check.py, name_dedupe.py
          │                         │
          └────────────┬────────────┘
                       ▼
        short report: what changed, what is unconfirmed,
        what needs your decision, emails ready to send
```

## Design rules

These are the parts worth copying even if you use none of the prompts.

1. **One record.** `itinerary.md` says where you are each night. When memory,
   a tracker or a chat disagrees with it, the file wins. The agent reads it
   before every edit and never edits the original in place.
2. **Constraints before suggestions.** Hard limits (no plans before noon, a
   budget per person, a rating floor, a gym requirement) live in
   `config.yaml` and are checked before anything is proposed.
3. **Verify at the source.** A booking site, map listing or aggregator is a
   lead. Hours, closing days and gym equipment are facts only when the
   business confirms them. Everything else is marked unconfirmed in the file.
4. **Search in the local language.** Small producers post hours and direct
   sales details in their own language. The configured search terms find
   what English queries miss.
5. **Check the weekday, with a script.** Most failed dinner plans come from a
   closing day. `scripts/closure_check.py` compares every planned visit with
   the place's closed days and lists places whose closing day is unknown.
6. **Lint the plan.** `scripts/itinerary_lint.py` checks weekdays, gaps,
   repeated dates, the night count, and that each day starts where the last
   ended. It runs after every edit to the date grid.
7. **Uncertainty lives in the file.** Estimates are marked "unverified".
   Unresolved items are `- [ ]` lines under Open decisions, ticked only with
   the confirmation written in.
8. **Write to businesses in their language.** Local language first, English
   beside it, formal register, no more than three specific questions.
9. **Draft, never act.** The agent drafts emails and lists booking steps. It
   does not send, book, pay or accept terms.
10. **Short reports.** One message: what changed, what is unconfirmed, what
    needs a decision.

## Layout

Paths are relative to this folder.

| Path | What it is |
|---|---|
| `SKILL.md` | Skill entry point: files, rules, which prompt to use |
| `prompts/vet-hotels.md` | Find and check hotels for a base |
| `prompts/scout-restaurants.md` | Restaurants for given nights near a base |
| `prompts/research-producers.md` | Wineries, dairies, distilleries, shops |
| `prompts/write-to-business.md` | Bilingual email drafts |
| `prompts/pre-trip-audit.md` | Full check of the plan before departure |
| `prompts/as-traveled-log.md` | Record what actually happened |
| `schema/itinerary.md` | Itinerary header, date grid, Open decisions |
| `schema/trackers.md` | Tracker columns and status colors |
| `templates/` | Empty tracker CSVs with those columns |
| `sources/catalog.md` | What each kind of source was reliable for, and field notes |
| `config.example.yaml` | Every setting the agent reads |
| `scripts/itinerary_lint.py` | Checks the date grid |
| `scripts/closure_check.py` | Flags visits on closing days |
| `scripts/name_dedupe.py` | Finds places already in a tracker |
| `examples/sample-trip/` | A short made-up itinerary in the format |
| `tests/` | Offline tests for the scripts |

## Setup

1. Install the skill. For Claude Code, install the `trip-planner@pegahcarter`
   plugin, or copy or symlink this folder to `~/.claude/skills/trip-planner`. For the Claude app, zip this folder and
   add it as a custom skill. Steps for both are in the
   [repo README](../README.md#install).
2. Copy `config.example.yaml` to `config.yaml` (the repo's root `.gitignore` ignores it) and fill in your
   constraints and language.
3. Start an itinerary from `schema/itinerary.md`, or give the agent a rough
   plan and ask it to put it in the format. Copy the CSVs in `templates/` to
   start the trackers, or use .xlsx or a Google Sheet with the same columns.
4. Ask for a task in plain words: "find hotels in Paestum for Oct 3 to 5",
   "check the plan", "draft an email to this winery about Sep 22".

## Running the scripts

```bash
python3 scripts/itinerary_lint.py examples/sample-trip/itinerary.md

# Export tracker tabs to CSV first
python3 scripts/closure_check.py --year 2026 exports/restaurants.csv exports/producers.csv

python3 scripts/name_dedupe.py --candidates new.txt exports/*.csv

python3 -m unittest discover -s tests
```

All three scripts use only the Python standard library.

## Limits

- Hours from a business's site are often not updated for the shoulder
  season. An email reply is the only confirmation that held up.
- Closing-day data is only as good as the tracker. Blank cells are reported
  as unknown, not as open.
- Drive times are estimates until checked against a current route planner
  close to the date.
- The scripts read CSV. Export .xlsx or Google Sheets tabs before running
  them.

## License

MIT. See [`LICENSE`](LICENSE).
