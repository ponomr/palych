# Developing Palych

Palych is an independent project at [ponomr/palych](https://github.com/ponomr/palych).
Use this repository as the source for future changes.

## Layout

- skills/palych/SKILL.md: compact Russian-first/English conversational instructions.
- skills/palych/references/: original examples and attribution to the adapted source.
- skills/palych/LICENSE: generated copy, so the folder installs as a complete skill.
- adapters/: optional persistent state helper and its subprocess tests.
- scripts/rules.py: renders the always-applied rule (Cursor) from SKILL.md.
- scripts/remove_global_block.py: removes the global-instructions block that releases
  before 0.10.0 installed; Palych no longer writes host instruction files.
- scripts/build_plugin.py: alternative Codex or Claude Code plugin builder.
- scripts/build_packages.py: generates the committed packages/ and plugin catalogs
  (.claude-plugin/, .agents/plugins/, .cursor-plugin/).
- scripts/check_package.py: offline frontmatter, JSON, local-link and generated-package checks.
- evals/: synthetic cases, masking tools, rubric and reader protocol.
- evals/results/: historical synthetic evidence; new runs need distinct files.

## Checks and packaging

Python 3.9+ on macOS/Linux runs the adapter. Checks need only the standard library.
From the repository root:

```sh
python3 scripts/build_packages.py
python3 scripts/check_package.py
python3 -m unittest discover -s adapters -p 'test_*.py'
python3 -m unittest discover -s evals -p 'test_*.py'
python3 scripts/build_plugin.py --host codex --output ./dist/palych-codex
python3 scripts/build_plugin.py --host claude-code --output ./dist/palych-claude-code
```

Commit regenerated packages with the source change; the package check fails on
drift. Keep host copies of SKILL.md under packages/ and none in the root, so
`npx skills add ponomr/palych` finds one skill and copies only skills/palych. Build targets must be new directories. Never publish dist/, local state or
reader responses automatically. The builder does not install a plugin. A fresh trusted plugin defaults to on;
existing saved defaults are preserved. The global-instructions installation is
documented in [INSTALL.md](../INSTALL.md); use one route at a time.
Core edits need relevant semantic checks using the existing evaluation protocol;
byte and format checks alone cannot prove reply quality.

## Evaluation and release

Use [evaluation instructions](../evals/README.md) and
[reader checks](../evals/reader-check.md). Run free offline checks first.
Paid generation is optional and requires an explicit budget; no API keys are needed
for the package or its local tests.

Record the exact revision, observed host/model settings and unavailable details.
Historical results before renaming are documented in [origin](ORIGIN.md).
Keep a clear distinction between packaging, simulated events, actual host
integration, model editorial judgments and human understanding.

The release version is in the builder manifest. Update that version and
[CHANGELOG.md](../CHANGELOG.md), regenerate packages, run checks, build both variants and verify
archive readback. Installing into a personal agent setup is a separate task.
