# Changelog

## 0.9.0 — 2026-10-30

- Core: the word "Russian" is gone (1182 → 1201 words with the rule below). With
  it, agent sessions on English coding tasks ended with a Russian final report
  in 14 of 60 sessions; without it, 0 of 32, measured on Claude Sonnet 5.5 in
  Claude Code only. The English examples and the Cursor rule's description drop
  the word too; plugin catalogs keep it for search. The language rule keeps "An English question gets an English reply",
  the style section reads "Any language: natural syntax and useful native
  equivalents", the description is "Compact, clear replies." and the example
  links read `ru` and `en`. Checked on 126 single replies and 44 agent sessions
  (2026-10-30 in the development log).
- Core: when work waits on the reader's answer, a progress or error reply
  names the needed decision in the first sentence and asks the question once,
  as the last sentence (pilot of 2026-10-29 in the development log).
- `mods/palych-toggle` is in the Claude Code marketplace as
  `palych-toggle@palych`; `scripts/build_packages.py` adds it to
  `.claude-plugin/marketplace.json` from the mod's own manifest. INSTALL.md
  installs it with the global-instructions route for Claude Code and covers its
  update and removal; it is not meant for the `palych@palych` plugin.
- `mods/palych-toggle`: the band now puts the switch first, then usage figures
  drawn after usage-band (MIT): 5h and 7d limits with reset countdowns and the
  context window; `/palych-tab` hides or shows the band for the session. The
  README has a section on the band with a screenshot.
- `mods/palych-toggle`: the switch is now the usage-quota mod's iOS-style pill
  (MIT) in the app theme's colours, with only the label «Палыч» beside it, both
  at the right of the band; the terminal shows a `●`/`○` button.
- `mods/palych-toggle`: a Claude Code mod with a «Палыч вкл / Палыч выкл»
  switch above the prompt that turns Palych off or on for the current
  conversation; checked with `claude plugin validate` and `claude plugin test`,
  not yet in a live session.
- `evals/session_replies.py` compares visible reply length in local Claude Code
  sessions before and after the core's installation; results are in the
  development log (2026-10-17).

## 0.8.0 — 2026-10-17

- Core: when the source states an irreversible effect of a step (erased
  settings, permanent deletion), the reply states that effect before the step,
  even ahead of the answer, and adds no preparation or backup advice the source
  lacks (1153 → 1182 words); pilot results are in the development log
  (2026-10-17).
- The core's self-check is one sentence that points back to the rules instead
  of repeating them (1176 → 1153 words); pilot results are in the development
  log (2026-10-15).
- `evals/cache_usage.py` estimates from local Claude Code and Codex logs how much
  of an always-on core's input is read from the prompt cache; results are in the
  development log (2026-10-15).
- Hermes installs the canonical `skills/palych` folder; `packages/hermes/` is no
  longer generated or published. A skill installed from the old path must be
  uninstalled and installed again.
- Repository size: the README banner is a JPEG (921 KB → 143 KB) and the plugin
  icon is 512×512 (560 KB → 132 KB per copy).
- `docs/STATUS.md` now holds only the current state and open limits; the dated
  records moved unchanged to `docs/history/STATUS-LOG.md`.

- Move the canonical skill to `skills/palych/` (`SKILL.md`, `references/`, a
  generated `LICENSE`). `npx skills add ponomr/palych` now installs only that
  folder instead of the whole repository. The adapter link in the core points to
  GitHub, so it also works in a standalone copy. Generated packages are unchanged.
- Claude Code plugin: add a 512×512 listing icon, built from `assets/icon.png`
  into `.claude-plugin/icon.png`, for the plugin directory's "No icon" warning.
- Core: «Отключи Палыча» / "Turn off palych" turns Palych off for the current
  conversation only. The core no longer tells the agent to remove the global
  instructions block or to look for a helper; only an explicit always-on request
  targets future sessions, and the agent edits no files or settings for a mode
  change. Found in Cursor, where a plain off request sent the agent searching
  for a way to persist it.

## 0.7.1 — 2026-10-14

- Drop the Gemini CLI extension: `gemini-extension.json`, `packages/gemini/`
  and its installation instructions. Gemini CLI is no longer a supported host.
- INSTALL: choose one route per host (global instructions or a plugin) up front;
  trusting the Codex hook in `/hooks` is an explicit required step; update
  commands for the Claude Code and Codex plugins; `npx skills` installs the
  skill folder instead of copying the whole repository.
- The runtime core (`SKILL.md`) is unchanged from 0.6.0.

## 0.7.0 — 2026-10-14

- Generate committed host packages from `SKILL.md`: Claude Code and Codex
  plugins with a SessionStart hook, a Gemini CLI extension, a Hermes skill and
  a Cursor rule, plus Claude Code, Codex and Cursor plugin catalogs.
  `scripts/build_packages.py --check` fails when a generated file drifts.
- Codex resume and fork no longer repeat the core when the session already
  holds the current one; changed cores, unmarked sessions and off mode still emit.
- Document installation from plugin catalogs and packages, Hermes preloading
  with `hermes -s palych` and Codex hook trust. Record offline and live host checks.
- README typography for Russian and English; SEO keywords, FAQ and author section.
- The runtime core (`SKILL.md`) is unchanged from 0.6.0.

## 0.6.0 — 2026-10-13

- Do not turn "optional" into a safety reassurance such as "nothing will break"
  or "safe to skip" without support. Add four focused RU/EN cases.
- Keep bounds such as "from", "at least" and "more than", and name conflicting
  supplied facts instead of choosing one. Add original RU/EN examples and eight
  focused cases. A broader empty-moves candidate failed its blind pilot and was dropped.
- Prepare a narrow candidate that merges semantic duplicates, makes headings
  and body add different information, reduces unambiguous noun echoes and avoids
  routine colon chains. Keep stable terminology and all source-fidelity rules;
  add original RU/EN examples and focused evaluation cases. Live testing pending.
- Test a shorter core with fresh paired controls; reject it after source audits
  find unsupported process actions and restore the preceding runtime core.
  Add RU/EN compactness fixtures, preserve optional-pointer trimming for both
  layouts and make installation checks independent of prose headings.
- Build full comparisons per option, check the supplied values, and put the
  recommendation first. Add RU/EN checks for full lists, unknown prices and
  short choice-only replies; keep assessor criteria separate from later workflow.
- Follow the question's language explicitly; retain Russian priority in package
  examples and evaluation rather than forcing English questions into Russian.
- Keep definitions within the requested concept and comparisons within the
  decision criteria. Check actor counts, routes and exclusive-role claims.
- Keep optional advice separate from behavioral guarantees. Preserve copies
  during diagnosis; recovery changes need evidence of need and authorization.
- Calibrate assessor criteria and keep unblinded audits separate from locked scores.
- Make compact, clear replies the primary goal. Put reply construction before
  activation details: direct answer, smallest useful form, necessary detail only.
- Choose content by task: definition, explanation, ordered instructions,
  comparison, progress/error or clarification. Avoid repeating one explanation
  as a list, diagram and recap; retain requested items and depth.
- Preserve supported causes and conditions; keep unknown reasons unknown and
  avoid unsupported universal claims or implementation guarantees.
- Add original RU/EN examples and a separate 20-case compactness regression set,
  including completeness and detailed-explanation counterchecks.
- Keep always-on loading, mode controls and optional examples unchanged.
- This is an instruction revision; new controlled model and reader tests remain
  separate. Existing historical results are not evidence for this version.

## 0.5.0 — 2026-10-11

- Make always-on the normal installation for Codex and Claude Code: generate the
  runtime rules into global instructions, without a separate skill call.
- Preserve other instructions, back up changed files, update without duplication,
  and remove only the managed block. Respect existing Codex global overrides.
- Default new hook-plugin state to on. Retain saved off states and avoid repeating
  the full core on ordinary turns; restore it at context boundaries.
- Rewrite both READMEs with an agent install prompt, example and main principles.
  Introduce the namesake as А.П. Чехов.
- Add isolated installer checks. Live-host loading and compaction remain unverified.

## 0.4.0 — 2026-10-10

- Publish the independent Palych repository; Russian display name: Палыч.
- Name chosen in honor of Anton Pavlovich Chekhov.
- Rename the runtime skill, plugin manifests, helper messages, commands and state
  directory from clear-replies to palych.
- Add natural Russian commands such as “Включи Палыча” and “Отключи Палыча”.
- Add standalone development, provenance, status and package-check documentation.
- Preserve the original MIT notice and all historical evaluation evidence.

## Before the independent repository

Clear Replies 0.3.0 compacted the core and hook payloads; 0.2.0 introduced the
optional state adapter and masked-evaluation tools. Historical measurements and
limitations remain under evals/. They are not new evaluations of this release.
