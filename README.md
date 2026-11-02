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
| [forge-attest](https://github.com/crossecute/forge-attest) | Builds Gnosis Safe transactions as Forge scripts and proves the queued transaction is their output. Lives in its own repo. |

forge-attest is not a folder in this repo. It is a Claude Code plugin with
two skills that run scripts from the plugin's own root, so it installs as a
plugin only. This repo's marketplace points to its default branch. To pin a
reviewed commit, follow its README instead.

## Install

Install only the skills you want. Each one works on its own.

**Claude Code, as plugins.** This repo is a plugin marketplace named
`pegahcarter`. Add it once, then install any of the three:

```bash
claude plugin marketplace add pegahcarter/agent-skills
```

```bash
claude plugin install trip-planner@pegahcarter
```

The other two are `job-pipeline@pegahcarter` and `forge-attest@pegahcarter`.
Claude Code keeps the installed copy in its plugin cache and replaces it on
update, so keep your `config.yaml` outside it and tell the skill where it is.

**Claude Code, as a folder.** Copy or symlink one skill folder into
`~/.claude/skills/`:

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

## Tests

Run both offline test suites from the repo root. No extra packages, API keys
or personal config are needed:

```bash
python3 -m unittest discover -s job-pipeline/tests -v
python3 -m unittest discover -s trip-planner/tests -v
```

[CI](.github/workflows/ci.yml) runs each skill's tests separately on Python
3.11 and 3.14 for every push and pull request. It can also be run manually
from GitHub Actions.

## License

MIT. See [LICENSE](LICENSE). Each skill folder carries its own copy, so the
notice stays with a skill that is installed or copied alone.
