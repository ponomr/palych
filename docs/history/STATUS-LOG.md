# Palych — dated development records

## Blocking-question rule integrated — 2026-10-29

Question: when work waits on the reader's answer, does a rule in the
Progress/error item put the needed decision first and end with one question?
60 replies, Sonnet 5.5, Claude Code 2.1.312, 3 repetitions, no retries; cases
from `main` c8d7ee0 with the reply language named. Current core SHA-256
`97c69a6f…97d7`, candidate `378fa190…bcd8`, keys `4a9debe5…e58e`, responses
`93aa9e70…c9f8`.

Added sentence: "When work waits on the reader's answer, name the needed
decision in the first sentence without asking it there; ask the question once,
as the last sentence."

| 18 blocking replies per condition | Current core | Candidate |
|---|---:|---:|
| Decision named in the first sentence | 1 | 18 |
| Reply ends with a question | 5 | 18 |
| No question at all | 6 | 0 |
| First sentence already a question | 0 | 0 |
| More than one question | 0 | 0 |

- An earlier wording ("name the decision in the first sentence; end with that
  one question") was piloted the same day on the old cases without a reply
  language: decision first in 16 of 18, but the first sentence was already the
  question in 7 and the question was asked twice in 3.
- The 12 non-blocking replies per condition asked no question.
- English replies in Russian: 0 of 30.
- Visible words over all 30 replies: 1648 current, 1521 candidate (−8%).
  `output_tokens`: 3757 against 5252 (+40%); the reason is unknown.
- Unsupported additions remain in the date case: the candidate added a plan for
  after the answer in 2 of 6 replies and said the mailing cannot be recalled in 1;
  the current core added plans in all 6. No invented options in either condition.
- One reader, who also wrote the cases and the candidate, checked all 36
  blocking replies; the counts match `shape_metrics.py` and the question
  checks. This is reply shape, not reader comprehension.
- Output: `~/ai-hub/outputs/2026-10-29-palych-blocking-question-v3/`
  (first wording: `…-blocking-question/`).

## Reply language in English eval cases — 2026-10-29

Question: why did 16 of 30 English blocking-question replies come back in Russian?
93 replies, Sonnet 5.5, Claude Code 2.1.312, 3 repetitions; core SHA-256
`97c69a6f…97d7`. Russian replies counted by letter share outside code spans.

| Arm | Russian replies |
|---|---:|
| No core | 11 of 15 |
| Current core | 6 of 15 |
| Core without Cyrillic | 4 of 15 |
| Current core, prompt ends "…in English." | 0 of 15 |
| Current core, request phrased as a question | 3 of 15 |
| 2026-10-16 English cases and core | 0 of 18 |

- Only "in English" differs from the current core significantly (Fisher p = 0.017).
- Russian text in the core is not needed for the effect; a CLI change did not turn
  the old English cases Russian. The model-side reason for Russian with no Russian
  input is unknown.
- The prompts ask for a message to "the user" without naming that reader's
  language. The blocking-question and label-reference cases now name the reply
  language in both RU and EN prompts. Earlier results on those sets used the
  old wording.
- The owner decided not to add a recipient-language rule to the core.
- Output: `~/ai-hub/outputs/2026-10-29-palych-lang-probe/`.

## Reply shape without a judge — 2026-10-29

Question: do deterministic shape metrics, adapted from attention-span v0.11
(`8a6e225`, ideas only, no text), separate Palych from no skill on the
2026-10-13 pilot? No model calls.

- Branch `claude/shape-metrics` (base c13c879) adds `evals/shape_metrics.py` and
  `evals/answer-keys.json`. The keys were written from the prompts alone and
  fixed before scoring (SHA-256 `4fd7f1e9…4334`, 2026-10-29T01:08:50Z); only the
  `ru-definition` replies had been seen. The depth cases have no key.
- The pilot's `responses.json` was not kept. The 180 replies were rebuilt from
  its `pairs.md`, whose hash matched the pilot's checksums; the rebuilt totals
  matched the pilot report (98 562 and 51 390 characters, 15 919 and 8 588 words).

| Median, 84 keyed replies per condition | No skill | Palych | Buried control |
|---|---:|---:|---:|
| Words | 150.5 | 73 | 104 |
| Words before the point | 4 | 2 | 33 |
| Point in the first sentence | 79.8% | 95.2% | 0% |
| Longest unbroken block, words | 37 | 33.5 | 73 |
| Longest sentence, words | 23 | 19 | 31 |
| Replies with headings | 14.4% | 5.6% | 0% |
| Deliverable wrapper | 6.7% | 0% | 0% |
| Closing offer | 3.3% | 0% | 0% |

- The buried control is built from the Palych replies: a warm-up paragraph is
  added and every block is joined into one. Every metric scored it worse.
- Audit of the 21 replies with the point outside the first sentence: 16 of 17
  without the skill are real warm-ups («In plain terms:»), wrappers or background
  first; 1 is a key miss. For Palych 3 of 4 are key misses (paraphrases of
  "optional") and 1 is borderline. Keys were not changed after scoring.
- The first-sentence rule was changed after reading these replies: bold labels,
  bold title lines and a letter greeting no longer count as the first sentence.
  Before the change the shares were 61.9% and 84.5%. This change needs a check
  on fresh replies.
- Ceremonial openers were 0% in both conditions; that lexicon separated only the
  constructed control.
- Output: `~/ai-hub/outputs/2026-10-29-palych-shape-metrics/`.

## Band mod from the marketplace — 2026-10-20

- PR ponomr/palych#36 (`de2c6a8`) added usage figures and `/palych-tab` to
  `mods/palych-toggle`; PR ponomr/palych#37 (`4b6ab06`) listed it as
  `palych-toggle@palych` and put it in INSTALL.md's Claude Code route.
- Mod checks: `claude plugin validate mods/palych-toggle` passed and
  `claude plugin test mods/palych-toggle` gave 12 pass, 0 fail.
- In a temporary `CLAUDE_CONFIG_DIR`, `claude plugin marketplace add ponomr/palych` and
  `claude plugin install palych-toggle@palych` installed version 0.1.0 as enabled, and
  `claude plugin uninstall` removed it.
- On the Mac (Claude Code 2.1.304) it was installed in the owner's settings, and
  `claude -p "/palych-tab"` printed `palych-toggle: Панель Палыча скрыта`.
- The desktop band was checked from owner screenshots of a session that
  loaded the mod folder, not the marketplace install.
- The terminal band was checked only by tests.

## Visible replies in agent sessions before and after installation — 2026-10-17

Question: do the pilot's output savings (45.4% on single replies) appear in
real agent sessions with tool loops? Observational comparison, no model calls.

- `python3 evals/session_replies.py --cutover 2026-10-13T07:58Z --days 14
  --cwd ~/ai-hub --cwd ~/repos --model claude-opus-5-5` at branch
  `claude/session-replies` (base 4afc4e9) on the Mac's Claude Code transcripts.
  The cutover is the always-on installation on the Mac (backup
  `20261013T075805692403Z`); later sessions had the global block in
  `~/.claude/CLAUDE.md`. Turns answered only by `claude-opus-5-5`, sessions in
  `~/ai-hub` and `~/repos`.

| Measure per turn | Before: 14 sessions, 298 turns | After: 22 sessions, 194 turns | Median difference, 95% |
|---|---|---|---|
| Visible text, characters, median (mean) | 1265 (1807) | 1161 (1454) | −525 … +211 |
| Final message, characters | 1010.5 (1200) | 1035 (1214) | −312 … +318 |
| Text messages | 1 (2) | 1 (2) | −1 … +1 |
| Output tokens (text, tools, thinking) | 2571 (10042) | 2790.5 (5412) | −1243.5 … +1230.5 |
| Prose slash chains per 1000 words | 0.22 (14 in 63876 words) | 0.43 (15 in 35038) | — |

- Without sessions in the Palych repository (13 before, 11 after): visible
  median 1258 → 954.5 (−743 … +409); slash chains 14 → 2, 0.24 → 0.16 per 1000
  words. Most after-period slash chains came from Palych development sessions.
- All sessions and models (38 before, 35 after): visible median 1200 → 1057
  (−511 … +115); output median 2290 → 2803.
- Intervals are percentile bootstraps over sessions. Every interval includes
  zero: these logs show no clear change in reply length. Means fell more than
  medians, but long outlier turns and different tasks drive means.
- Not controlled: task mix, the number of turns per session, other loaded
  instructions (`i-have-adhd` was switched off at the same cutover), host
  versions. Russian prompts were 92% of turns.
- Not measured: Codex (3 top-level Mac sessions after the cutover), clovis,
  Cursor, Hermes, and subscription usage-limit debits, which local logs do not
  record.
- Output: `~/ai-hub/outputs/2026-10-17-palych-session-replies/`.

## Unknown-reason probe; no candidate — 2026-10-17

Question: `ru-unknown-reason` failed 3 of 3 for the candidate in the last three
pilots («разработчики», «вышла новая версия», unchanged-behavior reassurance).
Is there a defect in the current core worth a candidate?

- Probe: the core at `main` b1ea1c7 (SHA-256 `97c69a6f…97d7`, 1182 words),
  `claude-sonnet-5-5`, effort medium, the same isolated harness, Claude Code
  2.1.292. 15 replies: `ru-unknown-reason` ×6, `en-unknown-reason` ×3 and two
  new Russian prompts of the same shape (optional printer-driver update,
  optional cache cleanup) ×3 each. Read by the agent, no assessor.
- `ru-unknown-reason`: an invented actor («Разработчики советуют») in 1 of 6;
  «Вышла новая версия», an added release event, in 2 of 6; no promise of
  unchanged behavior. Three replies recast "optional" as "not a violation"
  («не считается ошибкой», «не нарушите никаких правил», «ничего обязательного
  не нарушится»), which says nothing about effects.
- `en-unknown-reason` and both new prompts: no invented actor, release event or
  reassurance in 9 replies; the cache prompt kept the unknown source
  («Кто и почему дал этот совет, неизвестно») in 3 of 3.
- Decision: no candidate. The failures are rare and tied to the wording of one
  prompt; three earlier unknown-actor rules failed their pilots. The case stays
  as a regression guard. Run files:
  `~/ai-hub/outputs/2026-10-17-palych-unknown-reason-probe/`.

## Supplied-effect-first pilot; candidate integrated — 2026-10-17

Second candidate for the warning-order defect recorded below. The previous
candidate failed because "Answer first" still opened the reply with the action,
and "prerequisites" beside "warnings" invited invented preparation. Same
harness, 14 cases, settings and assessor setup as the warning-order pilot:
masked exploratory pilot, `claude-sonnet-5-5`, effort medium, safe mode, no
tools, a fresh process per reply, Claude Code 2.1.292; same-model assessors;
three repetitions, 42 pairs. Generated 2026-10-16…17.

- Baseline: the core at `main` 4fb5884 (unchanged since 3d6509a), SHA-256
  `435d2e82…a7fa0`, 1153 words.
- Candidate (`claude/nervous-hopper-ced014` a03614f, SHA-256 `97c69a6f…97d7`,
  1182 words): one sentence added after "Number actions when order matters":
  "When the source states an irreversible effect of a step, state that effect
  before the step, even ahead of the answer; add no preparation or backup
  advice it lacks." The prerequisites wording is unchanged.
- Preferences: candidate 21, baseline 6, ties 15. Semantic failures: baseline
  19, candidate 6; 3 candidate regressions. Output tokens 3.1% lower with the
  candidate (10209 vs 10533; Russian −2.8%, English −3.5%).
- Target behavior (agent reading of the 12 router and account replies per
  condition): the effect came before the first instruction in 10 candidate
  replies (router 6 of 6, account 4 of 6) and in 0 baseline replies.
- Invented additions in the six warning-order cases (agent reading): baseline
  8 replies (Reset needs a paperclip, prepare provider data, save files first,
  "no need to restart" in `en-theme`); candidate 0. One candidate reply
  (`en-router-reset` 2) answered in Russian and then repeated the answer in
  English; the assessor did not flag it.
- Candidate regressions: all three in `ru-unknown-reason`, the case that
  failed 3 of 3 for the candidate in the two previous pilots too: «Без неё
  всё продолжит работать так же» (unsupported reassurance), «Разработчики»
  (invented actor) and «Вышла новая версия». Baseline replies 1 and 3 also
  said «Вышла новая версия» and passed, so this assessor reading is
  inconsistent.
- Decision: the candidate is integrated. Not tested: reader comprehension,
  other models and hosts, warnings the source places after a step for a
  reason other than irreversibility.
- Locked judgments: packet `62886b37…1f1f`, judgments `61dea1ae…bdd5f`. Run
  files: `~/ai-hub/outputs/2026-10-16-palych-order-run2/`.

## Warning-order pilot; candidate rejected — 2026-10-16

Idea source: the warning-before-step rule of simple-writing-skills c70750c.
A probe of the current core first (8 replies, read by the agent,
`~/ai-hub/outputs/2026-10-16-palych-order-probe/`): for a database migration
whose source said "Important" the core put the warning first in 4 of 4
replies; for a router reset it said that all settings are erased only after
"hold Reset" in 4 of 4.

Masked exploratory pilot, `claude-sonnet-5-5`, effort medium, safe mode, no
tools, a fresh process per reply; same-model assessors; 14 cases, three
repetitions, 42 pairs. Cases: the new warning-order set (router reset, account
deletion, dark-theme guard; RU/EN) plus unknown-reason, roles, depth and
verification in RU and EN.

- Baseline: the core at `main` 3d6509a, SHA-256 `435d2e82…a7fa0`, 1153 words.
- Candidate (`claude/warning-order` 4ac1ec3, SHA-256 `665f4f60…3f9b`, 1160
  words): the Instructions line "prerequisites/failure conditions beside the
  affected step" became "prerequisites, conditions and warnings of supplied
  irreversible effects go before the affected step".
- Preferences: candidate 9, baseline 11, ties 22. Semantic failures: baseline
  14, candidate 17; 8 candidate regressions. Output tokens 10.3% higher with
  the candidate (11117 vs 10081).
- Target behavior (keyword placement check of the 12 router and account replies
  per condition): the warning came before the first instruction in 0 baseline
  replies (one of them was a clarifying question) and in 4 candidate replies.
  Assessors also failed most replies of both conditions on this criterion.
- Candidate regressions: invented preparation ("save any files you need
  first", "have your provider login") in router and account cases; "no restart
  needed" added in both theme cases; `ru-unknown-reason` 3 of 3 again
  («разработчики»), as in the label-reference pilot; `depth` 2.
- Decision: the rule is not integrated; the core stays at 3d6509a. Warnings
  after the step remain an open defect; the case set stays for the next
  candidate.
- Locked judgments: packet `084e9eca…48e3`, judgments `310258af…002f`. Run
  files: `~/ai-hub/outputs/2026-10-16-palych-order-run/`.

## Full-grammar probe; no pilot — 2026-10-16

Hypothesis: a compact core produces telegraphic fragments and slash chains
("result/effect"), so a "keep full grammar" rule from simple-writing-skills
c70750c could help. Checked before writing a candidate.

- Past pilot replies with the core: 0 prose slash chains in 386 replies
  (2026-10-13…16 runs, words of three or more letters on both sides of `/`,
  code spans excluded).
- Local Claude Code assistant texts of the last seven days: about 15 of 760
  texts longer than 200 characters had a prose slash chain («ключи/сеть»,
  «решения/действия»); repository names and code terms excluded by hand. These
  sessions mix hosts, tool loops and cores and are not a controlled sample.
- Probe: the current core (`main` 3d6509a, SHA-256 `435d2e82…a7fa0`) on six
  new RU/EN prompts that ask for brevity (release notes, renewal conditions,
  short status report), two replies each, `claude-sonnet-5-5`, effort medium,
  same isolated harness as the label-reference pilot, Claude Code 2.1.292.
  All 12 replies used full sentences or grammatical list items; none had a
  slash chain or dropped connectives. Read by the agent, no assessor.
- Decision: no candidate and no pilot; the single-turn harness shows nothing to
  fix. Tool-loop sessions remain unmeasured. Run files:
  `~/ai-hub/outputs/2026-10-16-palych-grammar-probe/`.

## Label-reference pilot; candidate rejected — 2026-10-16

Masked exploratory pilot, `claude-sonnet-5-5`, effort medium, safe mode, no
tools, a fresh process per reply; same-model assessors; 12 cases, three
repetitions, 36 pairs. Cases: the new label-reference set (progress on numbered
steps, report on a numbered option, RU/EN) plus unknown-reason, roles, depth and
verification in RU and EN. Idea source: the internal-reference rule of
[simple-writing-skills](https://github.com/dperhar/simple-writing-skills) c70750c.

- Baseline: the core at `main` 3d6509a, SHA-256 `435d2e82…a7fa0`, 1153 words.
- Candidate (`claude/label-reference` ce2a4e7, SHA-256 `65c3796e…2df7`, 1173
  words): after "do not rotate synonyms." it added "A label or pointer (option
  2, step 3, as above) does not carry meaning alone; add the content it names."
- Preferences: candidate 5, baseline 17, ties 14. Semantic failures: baseline
  3, candidate 8; 7 candidate regressions. Output tokens 13.6% higher with the
  candidate (8974 vs 7903).
- Target behavior: no reply in either condition used a step or option number
  alone; the current core already named the content in all 24 label replies.
- Regressions: `ru-label-decision` 3 of 3 (invented "logs are no longer kept on
  your server", an invented local-archive question or subscription step);
  `ru-unknown-reason` 3 of 3 («разработчики» as an invented actor, «вышла новая
  версия»); `en-label-progress` 1 ("The backup is intact").
- Language: one candidate reply to an English prompt and one baseline reply to
  an English prompt were in Russian.
- Decision: the rule is not integrated; the core stays at 3d6509a. The case set
  remains for the recorded evidence.
- Locked judgments: packet `46b3760d…6e66`, judgments `f1cee768…03ea`. Run
  files: `~/ai-hub/outputs/2026-10-16-palych-label-run/`.

## Bad/good example pilot; candidate rejected — 2026-10-15

Masked exploratory pilot, `claude-sonnet-5-5`, effort medium, safe mode, no
tools, a fresh process per reply; same-model assessors; three repetitions, 48
pairs. Cases: the four unknown-actor and four reassurance cases, plus
unknown-reason, roles, depth and verification in RU and EN.

- Baseline: the core at `main` 7955b41, SHA-256 `435d2e82…a7fa0`, 1153 words.
- Candidate (`claude/example-candidate` 3848974, SHA-256 `23634920…c9136`,
  1160 words): the two sentences "Optional means not required;
  …" and "Add no reassurance (…) the source does not support." were replaced by
  a labelled hypothetical example. Source: "A portfolio is advised but
  optional." Bad: "Recruiters advise it; skipping it costs nothing." Good: "A
  portfolio is advised but optional; the source names no adviser and no effect
  of skipping it."
- Preferences: candidate 8, baseline 13, ties 27. Semantic failures: baseline
  9, candidate 7; 4 candidate regressions. Output tokens 4.4% lower with the
  candidate (8114 vs 8486).
- Reassurance: in `optional-step` the candidate added "probably safe" or
  "usually low-risk" in 4 of 6 replies (3 regressions); the baseline did so in
  2 of 6. The removed sentences covered exactly this.
- Unknown actors: no failures in the four impersonal cases in either core.
  `ru-optional-backup` still drew «разработчик(и)» in 2 of 3 candidate and 2
  of 3 baseline replies; the candidate also added «авторы» once in
  `ru-optional-step`.
- The fourth regression (`en-depth`, "directly … not through the reviewer")
  is the route failure the core already targets.
- Decision: the example does not replace the rules; the core stays at 7955b41.
- Locked judgments: packet `5620d209…a061c`, judgments `ac228225…6cda`. Run
  files: `~/ai-hub/outputs/2026-10-15-palych-example-run/`.

## Self-check shortening pilot — 2026-10-15

Same harness, cases and settings as the core-trim pilot below: masked
exploratory pilot, `claude-sonnet-5-5`, effort medium, safe mode, no tools, a
fresh process per reply; same-model assessors; 16 cases, three repetitions, 48
pairs. The baseline replies are the 48 core-trim baseline replies, reused; only
the candidate replies were generated in this run.

- Baseline: the core at `main` f3a55d9 (unchanged since edc98c2), SHA-256
  `0dce8f6b…194de`, 1176 words.
- Candidate (`claude/selfcheck-trim` 94d5cdf, SHA-256 `435d2e82…`, 1153 words):
  the self-check list ("correct language; direct answer; … universal claims
  supported or conditional") became "silently check the reply against the rules
  above"; the rest of the core is unchanged.
- Preferences: candidate 16, baseline 8, ties 24. Semantic failures: baseline 7,
  candidate 5; 4 candidate regressions. Output tokens 6.4% lower with the
  candidate (9629 vs 10287; Russian −11.3%, English +0.4%).
- The four regressions are the failure types still open in the full core:
  unknown actors in `optional-backup` (ru ×1, en ×1, the latter also an added
  data-loss example), invented consequences and exclusive knowledge in
  `en-depth`, and reassurance in `ru-unknown-reason` («спешить нет причин»).
  The baseline showed the same types in this run.
- Assessor variation: the same 48 baseline replies drew 8 semantic failures in
  the core-trim run and 7 here.
- Decision: the shorter self-check is integrated. Not tested: reader
  comprehension, other models and hosts.
- Locked judgments: packet `c927490a…98535`, judgments `283700de…3c5a`. Run
  files: `~/ai-hub/outputs/2026-10-15-palych-selfcheck-run/`.

## Core-trim pilot; candidate rejected — 2026-10-15

Masked exploratory pilot, `claude-sonnet-5-5`, effort medium, safe mode, no
tools, a fresh process per reply; same-model assessors. 16 cases (ru/en: cost,
unknown-reason, roles, deadline, verification, seven, depth, optional-backup),
three repetitions, 48 pairs.

- Baseline: the core at `main` edc98c2, SHA-256 `0dce8f6b…194de`, 1176 words.
- Candidate (`claude/core-trim` 34b23e6, SHA-256 `7db4da6b…fc8a3`, 1130 words):
  the lowest-total-price sentence became "Calculate only what the criteria
  need."; the four role/transport sentences became one ("report the assigned
  actor, action and recipient, and the stated actors and steps; add no route,
  handoff or exclusive ability the source does not state"); the self-check list
  became one sentence.
- Preferences: candidate 15, baseline 14, ties 19. Semantic failures: baseline
  8, candidate 11; 8 candidate regressions. Output tokens 5.2% lower with the
  candidate (9749 vs 10287).
- Roles: the baseline won all three `en-roles` pairs and two `ru-roles` pairs;
  three of the six candidate role replies invented a route or excluded an
  intermediary ("sends the result directly to it", «а не буферу», «Он сам
  забирает»). Neither prompt states a route; the removed transport sentence
  covered this. The baseline had no role failures.
- The other five candidate regressions (deadline, depth, unknown-reason ×2,
  optional-backup) are the same failure types the baseline also showed in this
  run (invented outcomes, actors or exclusive knowledge), so the pilot does not
  separate them from noise.
- Decision: the candidate is not integrated; the core stays at edc98c2. The
  pricing and self-check cuts were not tested in isolation.
- Locked judgments: packet `851258ed…02d07`, judgments `695ea90c…fc420`.
  Run files: `~/ai-hub/outputs/2026-10-15-palych-core-trim-run/`.

## Prompt-cache share of the core's input cost — 2026-10-15

`python3 evals/cache_usage.py --days 14` at branch `claude/cache-measure` (base
16c409a) on the Mac's local logs: Claude Code transcripts and Codex rollouts
modified in the last 14 days. The script prints aggregates only. It does not
check whether Palych was loaded in each session; it estimates how an always-on
block placed in a session's first request is billed on later requests.

| Host | Sessions | Requests | Warm | Cold | Ambiguous | Core price vs. uncached |
|---|---|---|---|---|---|---|
| Claude Code | 123 | 9419 | 8888 | 159 + 123 first | 249 | 0.133–0.184 |
| Codex | 150 | 4024 | 3202 | 494 + 150 first | 178 | 0.244–0.284 (cached read assumed 0.1) |

- Claude multipliers, from the claude-api skill's prompt-caching guide (cached
  2026-10-06): cache read 0.1× base input (0.05× on Opus 5.5, 0.025× on Fable
  5.1), 5-minute write 1.25×, 1-hour write 2×. Claude Code wrote 1-hour entries.
  Most requests ran on `claude-opus-5-5`. Codex logs show no write premium; its
  cached-read price is an assumption, not a verified price.
- Claude Code: the 2600-token core costs about 346–478 base-input tokens per
  request. On Opus 5.5 ($4 input, $20 output per MTok) that equals 69–96 output
  tokens, 7–10% of the mean 964 output tokens per request in these sessions.
  The 2026-10-13 pilot measured 45.4% fewer output tokens on single replies;
  agent sessions with tool loops were not measured, so the net effect there is
  unknown.
- The bounds come from cache positions, not from per-block billing: a request is
  warm when its cached input covers the whole first request, cold when it covers
  no more than the first request's cached prefix, ambiguous otherwise.
- Not measured: subscription usage-limit debits, Cursor and Hermes, and sessions
  without a long tool loop (short chats repay the first write over fewer reads).

## Hermes install from skills/palych — 2026-10-15

Hermes Agent v0.22.0 (2026.9.24) on clovis, as the `hermes` user with temporary
`HERMES_HOME` directories, deleted afterwards. No model calls.

- `hermes skills install ponomr/palych/skills/palych --yes` from `main` d044d6f:
  scan verdict SAFE (skills-guard-v10, community source), five files installed
  (`SKILL.md`, `LICENSE`, three references). Their SHA-256 sums match
  `skills/palych` in branch `claude/repo-slimming` (1cd0a9c) byte for byte.
- Hermes installs GitHub skills only from the default branch. The same command
  was also run through a wrapper that reported commit 1cd0a9c as the default
  branch: same verdict and files; `hermes skills list` showed `palych` enabled
  and `hermes skills check` reported it up to date.
- Not checked: preloading with `hermes -s palych` from this path (needs a model
  call) and replacing an existing install from `packages/hermes/palych`.

## Cursor live check; plain off request fixed — 2026-10-14

Cursor 3.24.18 on the Mac, Free plan, agent model grok-4.6. The owner typed the
prompts in a test project; replies were read from Cursor's local chat store.
Core before this change = 0.7.1; the fix was then tested with the same plugin.

- `packages/cursor` copied to `~/.cursor/plugins/local/palych` loads as a local
  plugin: the log shows `loadUserLocalPlugin palych`, and the plugin rule count
  rose from 45 to 46 (skills stayed 45). Asked which rules apply, the agent named
  `palych.mdc` as always applied. A file change was reloaded in the open window.
- «Чем отличается git merge от git rebase? Коротко.» got a short answer ending with
  a rule of thumb; no control run, so this shows no style difference.
- The English question was answered in Russian because of the owner's Cursor user
  rule "Always respond in Russian", not because of Palych.
- «отключи палыча в этом чате» → «Палыч в этом чате выключен…»; the next answer
  (DNS) was longer, with a numbered list and an analogy.
- Bare «Отключи Палыча.» with the 0.7.1 core: the agent announced it was looking
  for a way to keep Palych off in future sessions and ran 40 steps of file
  searches and reads in `~/.cursor`, `~/.claude` and the installed Palych copies
  until the owner stopped it. No writes were found: the plugin was unchanged and
  the Claude Code state file kept `always_on: true`. Cause: the core told the
  agent to "remove its block for future sessions" and to "use its helper before
  claiming saved state".
- After the core change (plain off = this conversation only; no file edits or
  helper search for mode changes), the same bare request got «Палыч выключен в
  этом чате. Состояние не сохранено: в следующих сессиях он снова будет включён
  по умолчанию, пока не снимете установленное правило.» with no tool calls; the
  DNS answer after it was three short paragraphs. One run per case.
- Cursor also loads Claude Code plugins (`loadClaudePlugin` in its log); whether
  the Palych Claude Code plugin behaves there was not checked.
- The test plugin was removed afterwards.

## Hermes live check on clovis — 2026-10-14

Hermes Agent v0.22.0 (2026.9.24) on clovis, temporary profile `palychtest`,
model gpt-6.1-sol through the ChatGPT/Codex subscription. Five one-shot runs
(`hermes -z`); the profile was deleted afterwards.

- `hermes skills install ponomr/palych/packages/hermes/palych` installed the
  skill (scan verdict SAFE, five files); `hermes skills list` shows it enabled.
- Loading with `-s palych`: the preloaded skill text is not stored in
  `state.db` (the stored system prompt has the same hash in every run, and
  message `api_content` is empty), so loading was inferred from input tokens.
  The control run without `-s` used 8876 input tokens; the three `-s palych`
  sessions used 10636, 10633 and 10831 (the last one has two turns). The
  difference, about 1760 tokens, matches the size of `SKILL.md` (8126 bytes).
  This is indirect evidence, not a read of the prompt.
- Replies: the Russian and English questions were answered in their own
  languages. The control reply to the same Russian question was also short,
  so these single replies do not show a style difference.
- “Отключи Палыча.” returned «Палыч отключён в этом разговоре. Настройка для
  будущих сессий не изменена.» A follow-up with `--continue -z` joined the same
  session (one session, four messages). Whether the next reply followed the
  off state cannot be told from one short answer.
- `skills.auto_load` exists in v0.22.0 (`agent/skill_commands.py`
  `resolve_auto_load_skills`, `tests/agent/test_skills_auto_load.py`): a list in
  the profile config whose skills are rendered into every new session's prompt.
  It was not run with Palych. INSTALL.md now mentions it.

## Installation checks after 0.7.0 — 2026-10-14

Offline checks in temporary `HOME`, `HERMES_HOME` and `CODEX_HOME` directories,
without model calls. They cover installation, not how a model applies the rules.

- Hermes v0.16.0: `hermes skills install ponomr/palych/packages/hermes/palych`
  from GitHub `main` installs the skill (resolved through skills.sh, scan verdict
  SAFE); the five installed files match `packages/hermes/palych` byte for byte.
  `hermes skills check` reports it up to date; `uninstall` (after its
  confirmation prompt) and reinstall work. Preloading with `hermes -s palych` was
  not checked: it needs a model call.
- `npx skills@1.7.2 add ponomr/palych` (telemetry disabled) finds exactly one
  skill but copies the whole repository, 1.8 MB with evals, docs and packages,
  into `.agents/skills/palych`. `npx skills add ponomr/palych/packages/hermes/palych`
  (and the matching GitHub `tree` URL) installs only the skill folder, 48 KB;
  `npx skills remove palych` removes it. INSTALL.md now gives the folder form.
- Codex CLI 0.162.1 plugin from a local marketplace path: 0.7.0 installed; after
  the catalog was rebuilt as 0.7.1 in the temporary copy, `codex plugin list`
  still showed 0.7.0 and `codex plugin add palych@palych` replaced the cache with
  0.7.1. Upgrading a GitHub marketplace (`codex plugin marketplace upgrade`) was
  not observed, because no newer version is published.
- Codex hook trust: the Codex hooks documentation says trust is given in `/hooks`
  in the CLI and recorded against the hook's current hash. Whether Palych's trust
  survives a plugin update was not checked; the TUI flow was not run.
- Cursor: not checked. Cursor.app is not installed and `cursor-agent`
  2025.09.18 has no plugin commands.
- Claude Code update commands added to INSTALL.md (`claude plugin marketplace
  update`, `claude plugin update`) come from `claude plugin --help` 2.1.287 and
  were not run in this check; the 2026-10-13 record covers an update 0.6.0 → 0.6.1.

## Gemini CLI removed — 2026-10-14

The Gemini CLI extension and its instructions were removed at the owner's
request; Gemini CLI is no longer a supported host. Earlier dated records below
still mention it as history.

## 0.7.0 release — 2026-10-14

PR #13 merged as `4b1810d` and tagged `v0.7.0`; no GitHub release page was
created. Plugin manifests and catalogs report version 0.7.0.
Builds for `--host codex` and `--host claude-code` from that commit matched
`packages/`. The runtime core (`SKILL.md`) is unchanged from 0.6.0. Personal
installations were not updated. Users of a plugin catalog get 0.7.0 when they
update the plugin; the live checks below were run on 0.6.0.

Unmerged branches `codex/palych-clarity` and `claude/palych-unknown-actor` were
deleted after the merge. Neither candidate was integrated. The unknown-actor pilot is recorded below;
the clarity pilot has no record in this repository.

## Host installation checks — 2026-10-13

Offline checks of branch `claude/distribution-packaging` (`59a7ee0`) in temporary
config directories, without model calls. They cover installation, hook output and
mode state, not how a model applies the rules.

- Claude Code 2.1.287 plugin (local and GitHub marketplace): install, update
  0.6.0 → 0.6.1, uninstall and reinstall work. The SessionStart hook emits the
  core on startup, resume, clear and compact; a saved off survives compact and
  resume; always-on/always-off apply to new sessions; subagent events are ignored.
- Codex CLI 0.162.1 plugin (local and GitHub marketplace): `codex plugin add`,
  `remove` and reinstall work; mode state survives reinstall. The hook output is
  about 2,221 Codex tokens (UTF-8 bytes / 4), within `additionalContextLimit: 6000`,
  so it stays inline. A version upgrade was not observed.
- Hermes v0.16.0: the skill loads with `hermes -s palych`; there is no
  `skills.auto_load` setting. GitHub install works only after `packages/` reaches
  the default branch.
- Cursor, Gemini CLI and `npx skills`: files validated only; not run in a host.
- Known limitation: installing both the global block and the Claude Code or Codex
  plugin loads the rules twice, and their mode states can conflict. The hook
  does not detect the global block; INSTALL.md tells users to choose one route.
- Not verified offline: live model conversations; see the live checks below.

## Live host checks — 2026-10-14

Branch `claude/distribution-packaging` (`26cd3ac`), plugin 0.6.0. Claude Code
2.1.287 (`--model sonnet`, `--setting-sources project`, `--plugin-dir` copy with
a temporary `--state-dir`) and Codex CLI 0.162.1 (temporary `CODEX_HOME`, GitHub
marketplace, `--dangerously-bypass-hook-trust`). Rule loading was confirmed from
hook context in the Claude transcript and the Codex rollout, not from reply style.

- Both hosts: a new conversation received the core; a Russian question without
  Palych's name and a later English question on another topic got replies in the
  matching language. "Отключи Палыча" saved off for the conversation; after a
  real compaction (`/compact` in Claude Code, automatic compaction in Codex) the
  core was absent and off was delivered. A new conversation received the core again.
- Codex adds the core again on every `exec resume` (about 2,221 tokens each),
  because the adapter emits it on each SessionStart. Claude Code showed no
  duplicate after resume. Fixed in the adapter afterwards; see below.
- Codex does not run plugin hooks without persisted hook trust: the plugin is
  enabled but loads no rules and reports no error. How a user persists trust
  (TUI or config) was not checked.
- Not verified live: progress messages, plugin update and reinstall followed by a
  conversation, the global-block installation route, and Hermes, Cursor, Gemini
  CLI and `npx skills`.

## Codex resume deduplication — 2026-10-14

The adapter no longer re-emits the core on a Codex `resume` when this session's
emission marker matches the current core. It still emits on a changed core, a
session without a marker (started before installation) and in off mode (short
off block). Claude Code resume, startup, clear, compact and fork are unchanged.
Offline checks pass: `check_package.py`, `build_packages.py --check`, adapter
and eval unit tests, including new Codex resume cases with synthetic events.
Live check with codex-cli 0.162.1 and the plugin from commit e3c98c0, in a
temporary `HOME` and `CODEX_HOME` with `--dangerously-bypass-hook-trust`:
`codex exec` and then `codex exec resume` on the same thread wrote both turns
into one rollout file with one `thread_id`. That rollout holds one core message
(one `## Build the reply` and one adapter block), from the first turn; the
resumed turn added none. Both replies followed the skill. That the hook ran on
resume and chose to skip is inferred from the earlier duplicate on the same
path, not logged directly.

`codex exec fork` of that thread duplicates the core in the model context. The
fork's rollout holds only the new turn with its own core message and points to
the parent through `forked_from_id`; Codex loads the parent history, which
already holds a core. The fork turn used 18,319 input tokens against 16,421 for
the resumed turn with the full history, about one core more, although its
prompt was shorter. The adapter saw a new session id without a marker and
emitted; fork detection was added afterwards, see below.

## Codex fork deduplication — 2026-10-14

On a Codex `fork` SessionStart the adapter reads the first (`session_meta`) line
of the new rollout from `transcript_path`, takes `forked_from_id` when
`payload.id` equals the hook's session id, and copies the parent's emission
marker and saved mode to the fork. The fork then follows the resume rule: no
core when the marker matches the current core, the full core on a changed core
or a parent without a marker, the short off block in off mode. A fork of a fork
finds the first fork's marker. A missing, unreadable or mismatched rollout (an
ephemeral fork has no `transcript_path`) emits the full core as before. Claude
Code fork is unchanged. The payload shape (`source="fork"`, the new session id,
`transcript_path` to an already written rollout whose first line names the
parent) comes from the codex-cli 0.162.1 source (tag `rust-v0.162.1`), not from a
logged live event. Offline checks pass with synthetic fork events.

Limits: the hook does not know the fork point. A fork taken before the parent
received the core (for example, Palych enabled mid-conversation) gets no core;
a fork taken before the parent was switched off inherits off. This is the first
transcript read in the adapter: one line of about 22 KB with Codex base
instructions and session metadata, parsed in memory and not stored.

Live check with codex-cli 0.162.1 and the plugin from commit a30b7f5, in a
temporary `HOME` and `CODEX_HOME` with `--dangerously-bypass-hook-trust`:
`codex exec`, then `codex exec fork` of it, then `codex exec fork` of that fork.
The first rollout holds one core message (one `## Build the reply` and one
adapter block); both fork rollouts hold none, and each names its parent through
`forked_from_id`. Input tokens per turn were 16,375, 16,414 and 16,449, growing
only with the short history, against 18,319 for the earlier fork with a
duplicated core. The state file holds three emission markers with one core hash,
so the hook ran on both forks and copied the parent's marker; without a parent
it would have emitted the core. All three replies followed the skill. The hook
event itself was not logged: the logging wrapper added to the installed
`hooks.json` was gone by the time of the run, so the payload shape is still
inferred from the source. Not checked live: a fork in off mode, a fork after a
core change, `codex fork` in the TUI.

## Unknown-actor pilot; candidate not integrated — 2026-10-13

Across the four Claude pilots both cores sometimes supplied developers, organizers,
an administrator or a support team absent from the source. Optional examples are
not loaded at runtime, so a candidate added a short inline example beside the
existing actor rule (1118 → 1126 words), SHA-256 `7298dd755a6c0f3e6c8d84170cb7d38369d2dff734e06ae9561a711c3f222f3c`,
with matching RU/EN reference examples. The candidate stayed on the branch
`claude/palych-unknown-actor`, deleted unmerged; the core in `main` does not contain it. The four-case
[unknown-actor set](../../evals/unknown-actor-prompts.json) is kept for future attempts.

A three-repetition exploratory masked pilot (`claude-sonnet-5-5`, effort medium,
isolated Claude Code sessions) used the four unknown-actor cases, unknown-reason and
optional-backup in RU and EN against `main` 466fb77: 48 fresh replies, four same-model
assessor sessions, judgments locked before unblinding. Locked results: 5 candidate
preferences, 7 current-core preferences, 12 ties; 8 semantic failures each, 5
candidate regressions. The Russian example removed «Разработчики рекомендуют» in
`ru-unknown-reason`, but every English candidate reply turned the passive into
"Someone recommends". "Ask the developer" advice and replies speaking as the company
remained in both cores. The candidate was not integrated.

## Palych versus no skill; combined rules — 2026-10-13

Exploratory masked pilots on `claude-sonnet-5-5` (effort medium, isolated Claude Code
2.1.287 subscription sessions, same-model assessors, judgments locked before
unblinding). Reader comprehension was not tested.

No skill versus `main` 466fb77 (SHA-256 `3b176dce…a6828`): 30 RU/EN cases from the
compact, bounds/conflicts and reassurance sets, three fresh replies per condition,
180 replies and 15 assessor sessions. Locked results: 86 Palych preferences, 1
no-skill preference, 3 ties. Semantic failures: 45 without Palych, 3 with it; one
Palych regression (`en-depth`, an unsupported "cannot be undone" claim). Palych
replies were 45.4% fewer output tokens and 47.9% fewer characters, in both languages.
Input tokens rose by about 2600 per request because the core is sent each time;
cached-input pricing and subscription debits were not measured.

Combined rules: the pre-merge core (`eba7a41f…efc92`) versus `main` on eight cases
with earlier failures (unknown-reason, deadline, conflict, optional-backup; RU/EN),
three replies each. The `main` replies were reused from the no-skill pilot. Locked
results: 13 `main`, 4 pre-merge, 7 ties; semantic failures 12 versus 4. The pre-merge
core chose one conflicting term in 5 of 6 conflict replies, `main` in none. All three
`main` regressions are in `optional-backup`, where "the app works without it" persists.

## Actors, promises and next steps — 2026-10-13

After the no-reassurance pilot, one clause was added: do not add actors, promises
or next steps the source does not state (1100 → 1113 words), SHA-256
`5161ced213ad40e116ffe7a4a56c4780f9428b1bc089e34d7619af942e3c9bd5`. It targets the
remaining candidate failures: an invented "developers will not require it" and an
added "fix the problem before trying again".

A focused three-repetition exploratory pilot on unknown-reason and deadline (RU/EN,
24 fresh replies, two same-model assessor sessions, locked before unblinding) gave
5 candidate preferences, 4 current-core preferences and 3 ties. The assessor marked
1 current and 3 candidate failures; the source audit confirms two candidate failures
(an invented "developers" subject, an added "ask the organizers") and treats the
literal reading of "before 09:40" as an assessor error. Both cores wrote "fix the
problem and pass the check first". The clause showed no measurable effect on the
targeted additions. Input tokens +1.79%, output −4.82%, characters −5.22%.
The clause was removed; the core returns to the tested no-reassurance version,
SHA-256 `adaa8b2c40d8e0224166adfc568c4a4ca8b7cdda16a030d8c613c35709011d0c`.

## No-reassurance candidate prepared — 2026-10-12

In both 2026-10-12 Claude pilots, both cores sometimes turned an optional update into
a guarantee ("nothing will break", "you can safely skip it") despite the existing
rule. The candidate restates the rule with these surface forms (1082 → 1100 words), SHA-256
`adaa8b2c40d8e0224166adfc568c4a4ca8b7cdda16a030d8c613c35709011d0c`.
Original example lines and a four-case [reassurance set](../../evals/reassurance-prompts.json)
were added.

A three-repetition exploratory masked pilot on `claude-sonnet-5-5` (effort medium,
isolated Claude Code 2.1.287 subscription sessions) used the four focused cases,
unknown-reason, and roles/deadline/conflict guards in RU and EN: 72 fresh replies,
six same-model assessor sessions, judgments locked before unblinding. Locked results:
19 candidate preferences, 7 current-core preferences, 10 ties. Semantic failures:
13 current, 5 candidate, including 4 candidate regressions.

In the 18 targeted replies the current core added an unsupported reassurance 8 times,
the candidate once. Candidate regressions: an invented "developers will not require
it" actor and promise (`ru-unknown-reason`, twice), "the device will keep working"
(`ru-optional-backup`), an added "fix or ask before trying again" (`en-deadline`).
The assessor passed similar current-core phrases, so the regressions partly reflect
assessor inconsistency; the invented actor appears only in candidate replies.
The fixed semantic gate is formally not met. Input tokens +1.17%, output +2.28%,
answer characters +1.66%. Reader comprehension untested.

## Narrowed bounds/conflicts candidate — 2026-10-12

After the failed pilot only one rule was kept: keep "from", "at least" and
"more than" bounds, and name conflicting supplied facts instead of choosing one.
The other candidate rules, examples and documentation were reverted to `main`.
The core grows from 1082 to 1100 words, SHA-256 `bba312add40b81cd0727f40d3f5de7e207163e21973a09ea1d83d7a657cebaa8`.
An eight-case [bounds and conflicts set](../../evals/bounds-conflicts-prompts.json)
was added.

A three-repetition exploratory masked pilot on `claude-sonnet-5-5` (effort medium,
isolated Claude Code 2.1.287 subscription sessions) used the eight focused cases and
six guards (unknown-reason, roles, deadline): 84 fresh replies, seven same-model
assessor sessions, judgments locked before unblinding. Locked results: 16 candidate
preferences, 9 current-core preferences, 17 ties. Semantic failures: 6 current,
2 candidate. The current core chose one conflicting delivery term or price in 5 of
12 conflict replies; the candidate chose none. Both cores kept every bound.

Both candidate failures are guard regressions of a pre-existing type: an unsupported
"nothing will break" guarantee (`ru-unknown-reason`, which the current core produced
in the previous pilot) and an added "fix the problem first" instruction
(`en-deadline`). The fixed semantic gate is formally not met; integration is the
owner's decision. Input tokens +1.30%, output tokens +2.75%, answer characters
+6.34%, mostly where the candidate explains a conflict. Reader comprehension untested.

## Empty-moves pilot: semantic gate failed — 2026-10-12

An exploratory masked pilot compared the current core (SHA-256 `eba7a41f…efc92`)
with the candidate (`e6990d03…22245`) on `claude-sonnet-5-5`, effort medium, through
an isolated Claude Code 2.1.287 subscription session. 32 cases (12 empty-moves,
20 compact) received one fresh reply per core: 64 processes with empty tools, MCP,
skills and hooks. Eight fresh same-model assessor sessions judged masked pairs;
judgments were locked before unblinding. One batch was re-judged before unblinding
after violating the protocol; 16 calls were rejected by an item-count schema error.

Locked results: 13 candidate preferences, 10 current-core preferences, 9 ties.
Semantic failures: 3 current, 2 candidate; both candidate failures are regressions.
`en-unknown-reason` promised unchanged behavior; `ru-roles` added a direct route as
"not through the buffer". The current core picked one conflicting delivery term in
`en-conflict`; the candidate named the conflict. A separate unblinded source audit
confirmed all five failures and found two borderline candidate statements.

Input tokens rose 6.84% (103449 → 110527) and output tokens 2.13%; answer characters
fell 2.21%. Neither core produced grading labels or manner praise, so the run shows
no measurable benefit from the empty-moves rule. The fixed semantic gate failed:
the candidate is not ready for integration. Reader comprehension was not tested.

## Empty-moves candidate prepared — 2026-10-12

Several public Russian editing skills were reviewed for principles; no text or
code from them is bundled. The candidate adds about 100 words to the core
(1082 → 1182): it removes empty rhetorical moves, keeps causal and contrast links
when shortening, replaces unsupported evaluations with facts, names failures
plainly, keeps lower bounds and "more than" conditions, and names conflicting
supplied facts. Rejected ideas included mandatory output blocks, scores, required
numbers, minimum lengths, fixed paragraph sizes and automatic rounding.

Original RU/EN examples and a 12-case [empty-moves set](../../evals/empty-moves-prompts.json)
support the change. No model run was made; shorter replies, token savings and
reader comprehension are not established. A paired blind run of the current and
candidate cores is the next step. Candidate SKILL.md SHA-256:
`e6990d032eb06ed47110573becc6eecdf685c850c871d3a2472beed7e9522245`.

## 0.6.0: compact replies

The revised core prioritizes compactness and clarity through task-specific reply
construction, single representations, necessary detail and a concrete stop rule.
It also checks supported causes, universal claims and implementation assumptions.
See [design and verification scope](../COMPACT-REPLIES.md).

Original RU/EN examples and separate regression sets are included.
The previous prompt set and historical result files remain unchanged. Reader
comprehension tests have not been performed; model pilots are recorded below.
An exploratory one-response-per-case Claude Code pilot was performed on the
earlier candidate. It showed shorter replies but automatic judgments missed
content and language errors. The core and assessor rubric were revised from the
source audit; repeat runs are recorded separately by tested core hash.
These results do not establish reader comprehension or universal compliance.
The source revision does not update personal installations or establish live
hook delivery. Released as 0.6.0 on 2026-10-13; the release does not establish
model or reader validation.

## Repetition candidate prepared — 2026-10-12

The owner supplied a human-preferred edit of one Russian publication explanation
and identified missing brevity, repeated meanings/terms and overused colon links.
This is specific reader editorial feedback, not a blinded comparison or evidence
of improved comprehension across readers.

The next candidate is a narrow revision of the restored 1048-word core. It merges
semantic duplicates, joins a step's action and purpose, lets a heading carry a
complete step, and removes previews/recaps that add no information. Pronouns or
ellipsis reduce nearby noun echoes only when unambiguous; terminology stays stable.
Ordinary sentence links prefer full stops/conjunctions, keeping useful colons.

The meaning-preservation, agent-work and activation sections are byte-for-byte
unchanged. No broad compression of the accuracy rules was repeated. Original
RU/EN examples and a focused repetition set support the new rules. The core
grew from 1048 to 1082 words; shorter generated replies or token savings have not
been established. No new model calls were made for this candidate. The preceding
75-request pilot does not validate these changes. Source integration does not
update personal installations; reader comprehension and fresh model evaluation
are pending.

## Shorter-core pilot completed; candidate rejected — 2026-10-12

A 762-word candidate (5938 bytes) was compared with the current 1048-word core
(7628 bytes) on `gpt-6.1-sol`, medium effort, default tier. Twelve new RU/EN tasks
plus the four existing cache-cost and detailed-process tasks were repeated twice
per condition: 64 fresh replies in distinct threads. Neither control was reused.
Local instruction sources, other skills and tool use were excluded and verified;
hidden provider instructions and sampling settings remain unavailable. Generation
was interrupted and resumed, so hidden provider state across the pause is unknown.

Eight fresh assessor sessions judged 32 masked pairs before the mapping was
opened. Locked results: 4 candidate preferences, 1 current-core preference and
27 ties; the assessor found one candidate semantic regression. The subsequent
unblinded source audit confirmed it and found the same unsupported author-to-editor
handoff in the second Russian publication reply. A third candidate reply assigned
an unprovided handoff to the request sender. The audit also found an unsupported
return-action actor in one current-core English publication reply. These findings
are separate from the unchanged locked judgments; neither measures human reading.

Candidate input tokens were 202297 versus 212025 (-4.59%); reported output tokens
5142 versus 5697 (-9.74%). RU output -13.53%, EN output -4.68%. Answer characters
fell 10.17%. Each candidate input was 304 tokens smaller. Cached input varied and
is included in input totals; subscription debit, failed-turn usage and native
transport retry consumption were not measured. Savings do not override a meaning
failure or establish that compression caused the errors.

The fixed semantic gate failed: the candidate was rejected and the original core
restored, SHA-256
`e3ad8877c3028afc6d422686a2b46fd166a32a6ee6118d37fa47f5a9fd0185dc`.
The rejected candidate remains recoverable in history and separate evidence,
SHA-256 `74c8fe86b0d083f1799d3d020f71d0ea2429688b4fdbeddbc766027fa5cd548a`.
Installer compatibility, heading-independent tests and the 12 new fixtures remain.

Exactly 75 logical model requests were logged: 64 completed replies, 8 completed
assessor sessions and 3 failed/incomplete operations (stream timeout, capacity,
usage limit), each followed by one authorized retry. Native reconnection attempts
are recorded separately and their provider count/cost is unknown. Two process
launches were blocked by permission-review timeouts; the restricted environment
also refused nested sandbox setup. A narrower reviewed launch succeeded, then
usage-limit recovery was resumed at the owner's request. The total cap did not
change; a send guard refuses request 76. All jobs completed; no further runs.

35 installer/adapter/builder tests and 17 blind-tool tests passed before the live
pilot. The final restored package is verified separately. Runtime hooks, automatic
compaction and reader comprehension were not retested here. Main and personal
installations remain unchanged; raw host logs remain outside the public package.

## Focused Codex follow-up — 2026-10-12

The comparison rule was tested on `gpt-6.1-sol`, medium effort, with six new
RU/EN prompts and three fresh replies per condition. All 18 masked pairs tied;
both cores preserved the requested values. In the 12 full comparisons per core,
the conclusion preceded the table in 10 candidate replies versus 3 controls.
All six candidate choice-only replies retained the requested two-sentence form.

Twenty further candidate replies were compared with saved current-core controls.
The known English seven-plan omission was repaired; one Russian cache explanation
had more avoidable detail. No new semantic regressions were found by the masked
assessor or the subsequent unblinded source audit. Reused controls and unavailable
provider settings limit causal conclusions; this does not establish an overall
compactness improvement or reader comprehension.

Two eight-turn Codex conversations completed actual manual compaction after turn
six. The candidate core was supplied once through developer instructions; it was
not reinjected. Post-compaction replies retained the memo's exact deadline,
timezone, file-size boundary and failed-check prohibition. RU/EN switching and
the one-word override worked. This tests the injected core in a short conversation,
not personal installation, global-instructions loading, plugin hooks or automatic
compaction near the context limit.

In those conversations, the candidate's reported input tokens were 27.1% higher
and output tokens 7.8% higher than the no-skill control. Cached input varied;
subscription debit and separately attributable compaction consumption were not
measured. Loading the core once does not remove its cost in later input contexts.
Candidate core SHA-256:
`e3ad8877c3028afc6d422686a2b46fd166a32a6ee6118d37fa47f5a9fd0185dc`.
Raw host logs and model replies remain outside the public package.

## 0.5.0 installation and verification history

The default installation now adds Palych's runtime rules to Codex or Claude Code
user instructions. This makes the rules available from the first reply without
an explicit skill invocation. See [INSTALL.md](../../INSTALL.md).

The plugin route is an alternative: fresh state defaults to on, saved off states
survive upgrades, and the core is restored at SessionStart boundaries. Ordinary
prompts do not repeat the core. Use one route at a time.

## Local verification

34 installer/adapter/builder tests and 17 blind-tool tests passed. Installer tests
use temporary configuration directories, including both hosts, custom paths,
Codex global overrides, exact preservation of existing bytes, backups, idempotent
updates, removal, refusal of edited/linked instructions and failed atomic writes.
Hook tests cover startup without activation, compact/resume/clear/fork restoration,
saved off overrides, existing off defaults, deduplication and unchanged ordinary
prompts. These tests do not establish live-host event delivery or model behavior.

The offline package checker validated 45 source files: frontmatter, JSON, links
and absence of private machine paths. Both plugin variants are built from the
same source. Core SHA-256: `d1ef198edc671d249b138a3771bd8b6f9be857155b3bf5f7a0ff0109fd717ce1`.

## Still open

- Actual host loading, instruction-size limits and mode retention after real
  compaction. Global instructions shape behavior; they are not enforced settings.
- Reader comprehension testing with the intended audience.
- The complete controlled 20-case, three-repetition comparison with observed
  matching generation settings.
- Actual platform token/usage-limit measurements. Keeping one runtime block and
  avoiding repeated hook injection prevents duplicates; it does not establish
  subscription savings or eliminate repeated input-context costs.

Earlier masked and editorial pilots are described in
[historical observations](../../evals/observations.md). Their limits remain in force.
Static counts in [token-usage.md](../../evals/token-usage.md) describe Clear Replies
0.3.0 before the rename. Historical evidence is unchanged.

Developing and publishing an installer does not install Palych into personal
agent environments. No personal settings were changed for these tests.
