# Contributing

Keep each change focused on one feature or fix. Use a branch and open a pull
request against `main`. Use Conventional Commits for commit messages, such as
`fix(trip-planner): handle year rollover` or `ci: run offline tests`.

## Changes

- Keep each skill installable on its own. Include the files and license it
  needs inside its folder, and check paths from that folder.
- Keep scripts limited to the Python standard library. Discuss a new runtime
  dependency before adding it.
- Keep personal data, credentials, filled-in configs and exports out of the
  repo. Use made-up data in examples and test fixtures.
- Update affected prompts, schemas, examples and documentation when behavior
  or file formats change. Check callers and references when renaming files.
- Add or update regression tests for behavior changes. Keep tests offline,
  without API keys, accounts or personal config.

## Validation

Run both suites from the repo root in separate processes:

```bash
python3 -m unittest discover -s job-pipeline/tests -v
python3 -m unittest discover -s trip-planner/tests -v
git diff --check
```

Each suite has a `test_scripts` module and imports scripts by name. Running
them separately keeps those imports isolated.

When adding a skill with tests, add it to the matrix in
[CI](.github/workflows/ci.yml) and update the test commands here and in the
[README](README.md#tests). If required check names change, update the GitHub
ruleset for `main` to match.

## Pull requests

Describe the problem, the resulting behavior and the checks you ran. Mention
any limits that reviewers need to assess. Keep commit messages and PR
descriptions free of generated-by footers and assistant attribution.

The merge rules for `main` require all four CI checks to pass, the branch to
be up to date, and review conversations to be resolved. Direct pushes,
force pushes and branch deletion are blocked. An approving review is
optional so the maintainer can merge solo changes.
