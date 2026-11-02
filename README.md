# agent-skills

Claude skills built from real projects. Each skill has its own folder with
prompts, schemas, field notes from actual use, and scripts that use only the
Python standard library and come with tests. No folder holds personal data:
you bring your own config, sheets and files.

## Skills

| Skill | What it does |
|---|---|
| [job-pipeline](job-pipeline/) | Two scheduled agents that sync job-search email and refresh job and funding leads into one Google Sheet. |
| [trip-planner](trip-planner/) | Plans a multi-week road trip from one itinerary file, with trackers for hotels, restaurants and producers. |
| [forge-attest](https://github.com/crossecute/forge-attest) | Builds Gnosis Safe transactions as Forge scripts and proves the queued transaction is their output. Kept in its own repo. |

forge-attest is a Claude Code plugin, not a folder in this repo. Its skills
run scripts from the plugin's own root, so install it as its repo's README
describes rather than copying files.

## Install

Each folder in this repo is one skill and works on its own. Install only the
ones you want.

**Claude Code.** Copy or symlink one skill folder into `~/.claude/skills/`:

```bash
cp -r trip-planner ~/.claude/skills/trip-planner
```

```bash
ln -s "$PWD/trip-planner" ~/.claude/skills/trip-planner
```

Claude Code picks up the new skill in a running session. If
`~/.claude/skills/` did not exist when the session started, run
`/reload-skills`. Then copy `config.example.yaml` to `config.yaml` in the
skill folder and fill it in.

**Claude app.** Code execution must be enabled (on individual plans, under
Settings > Capabilities; on Team and Enterprise, an owner enables it). Zip one
skill folder so the folder itself is at the root of the zip:

```bash
zip -r trip-planner.zip trip-planner
```

Then go to Customize > Skills, click "+", choose "Create skill", then
"Upload a skill", and select the zip.

## Scheduled tasks

job-pipeline also runs as two scheduled tasks, one per agent. Setup steps are
in [job-pipeline/README.md](job-pipeline/README.md#setup).

## License

MIT. See [LICENSE](LICENSE).
