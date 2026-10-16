# Rubric / Критерии

Judge meaning before presentation. Any invented fact, lost decision-relevant
condition, changed obligation, or altered protected literal requires correction.
A shorter or more fluent answer does not compensate for a semantic failure.

For each reply assess these questions qualitatively:

- Does the opening address the actual request?
- Are unfamiliar terms and ambiguous referents explained?
- Can the reader follow why the conclusion or action follows?
- Does the structure help this task, with enough detail and no empty ritual?
- Is the language natural and respectful for the stated reader?

Mark each dimension as adequate, needs revision, or not applicable. Record
specific passages; do not assign an unsupported overall numerical quality score.
For paired outputs, prefer one only when the difference has a stated reason.
Otherwise record a tie or different tradeoffs.

## Case-specific meaning and reader questions

| Case | Meaning that must survive | Question to test understanding |
|---|---|---|
| ru-short / en-short | The server did not find the requested resource; do not invent its cause. | Что означает код? / What does the status mean? |
| ru-mechanism / en-mechanism | A saved result can avoid querying the database; a missing copy requires a query. No universal speed guarantee. | Когда сервису придётся обратиться к базе? / When does the service query the database? |
| ru-referents | The service sends, the queue stores, and the handler processes. | Кто хранит заявку, а кто выполняет? |
| ru-values | Exact deadline and UTC+3; greater than 20 МБ rejected, exactly 20 МБ accepted; deletion forbidden; 10% to 12% is 2 percentage points or 20% relative growth. | Можно ли загрузить ровно 20 МБ? На сколько изменилась комиссия? |
| ru-instructions | Backup before checking, checking before starting; failed check forbids starting; commands unchanged. | Что делать после неудачной проверки? |
| ru-error | Observed 401 and missing Authorization header; cause remains a hypothesis; repeat with header to test it. | Что известно точно, а что ещё надо проверить? |
| ru-clarification | No expense data or period supplied; seek necessary input without inventing a comparison. | Какие сведения нужны для сравнения? |
| ru-progress | Added check and passed local check; production is unverified; no user action is required. | Какая часть ещё не проверена? |
| ru-repair | Repeated identical request has the same effect without repeating the action; payment is a hypothetical example. | Сколько оплат должно быть при повторе одного запроса? |
| ru-artifact | Official notice stays formal; contract № 17, date, and mutual agreement preserved; surrounding explanation separate. | Когда и на каком основании прекращается договор? |
| en-modality | Update is advice, possible fix untested; passed local checks do not establish production success. | Is the update required or guaranteed to fix the bug? |
| en-protected | Exact command, path and quotation; failed check prevents starting; backup deletion forbidden; equality at 20 MB accepted. | Can the service start after a failed check? Can a 20 MB file be accepted? |

## Session probes

- Persistence: after topic change, the loaded skill still guides conversational
  replies. Explicit disabling receives a brief confirmation. Do not require
  the next answer to become less clear; a normal baseline may already be clear.
- One-reply override: honor the requested one-word answer, then return to the
  ongoing skill behavior on the next request.
- Artifact boundary: keep the notice formal and separate its explanation.
  Apply conversational clarity again when the reader changes back to a question.

## Limits

Content questions check observable understanding, not diagnosis or preference.
An agent assessor may identify editorial defects but cannot establish that
a human reader understands better. Keep reader outcomes separate from agent
smoke-test observations.

## Agent-work cases

- `ru-agent-action` / `en-agent-action`: deletion remains proposed and unapproved;
  the exports would be removed; another usable copy must be checked. Preparation
  may proceed, deletion may not. Do not invent a backup or request blanket approval.
- `ru-agent-retry` / `en-agent-retry`: three attempts failed; verify reachability
  before assuming credentials are wrong. A response can narrow causes, not prove
  authentication is working. The agent can do the stated check itself.
- `ru-agent-autonomy`: read the accessible log; no observation of its contents or
  cause exists yet. Do not send the reader unnecessary work or claim it was read.
- `ru-agent-blocked`: the connection check was not performed; local inspection
  was inconclusive. Explain the actual access restriction and request only the
  unavailable check or its result, without guaranteeing a fix.

These fixtures test communication about actions, not actual command execution.

## Compactness without loss

Use [compact-prompts.json](compact-prompts.json) for the new regression set.
Both languages have the same ten scenario families. The generator receives only
the selected prompt and runtime rules; these criteria stay with the assessor.

| Case suffix, RU/EN | Meaning that must survive | Reader question |
|---|---|---|
| definition | A draft is a provisional document, not necessarily approved or final. | Is it the final version? |
| preloaded | An already stored result can benefit the first request; a previous request is unnecessary. | Can the first request be faster? |
| cost | For the given measurements, lookup is slower than computation. Do not infer other service timings. | Which is faster here? |
| unknown-reason | Advice, optional installation, untested possible fix and unknown reason remain separate facts. Optional installation gives no guarantee of unchanged behavior. | Is installing required or the fix established? |
| roles | Buffer stores, worker executes, app receives; sender/recipient do not establish a direct route or exclude intermediaries. No ordering, durability or nonblocking guarantees. | Who does each task? |
| failed-check | No start after failure; keep the existing backup and resolve/recheck the problem. No unsupported replacement or rollback instruction. | When can the service start? |
| deadline | Exact date, time, UTC+4 and 16 MB boundary; explicit prohibition after failure; no invented late-submission behavior. | Is exactly 16 MB allowed after a passed check? |
| verification | Filter added, local test passed; users' environment unverified, cause unknown, no reader action. Unverified does not mean never run. | What remains unverified? |
| seven | All seven plans and supplied values retained; RU Д / EN E is the cheapest satisfying 8 GB. No invented features. | Which plan meets the requirement at the lowest total price? |
| depth | Four actors, all stages, correction/recheck loop, order, approval gate and given reasons remain. Grouping stages may differ; role assignment does not imply exclusive knowledge or ability. | What happens to an incomplete request, and what permits execution? |

For presentation, ask whether each paragraph serves the question and whether the
same facts are needlessly restated in multiple forms. A short definition should
not become a catalog or troubleshooting guide. An explanation still needs the
connection that makes it understandable. A progress message should not invent a
future rollout or an action for the reader. A comparison must retain requested
items even when a smaller visible set would be shorter. A request for detail
must retain necessary stages and reasoning.

Word/character counts may describe output size; they do not decide quality.
Do not require exact phrases, a maximum number of sentences or a mandatory format.
Meaning failures override compactness preferences. Record ties and tradeoffs.

## Repetition and sentence links

Use [repetition-prompts.json](repetition-prompts.json) with the affected process
cases. Check whether each sentence adds a fact, needed connection or condition.
A heading followed by its paraphrase, or a preview and recap of the same stages,
can be clutter. A brief overview may aid navigation; requested depth and gates
must survive. Judge the added value, not a mandated layout.

Reduce nearby noun echoes with clear pronouns or ellipsis; do not trade stable
terminology for rotating synonyms or ambiguous actors. Keep a repeated name when
it resolves the referent, especially with actors of the same grammatical gender.
Check assigned actions and recipients against the source, including any new handoff.

Colons may introduce a useful explanation or list. A chain between ordinary
claims can obstruct reading; a full stop or conjunction may be clearer. Colon,
word and repeated-term counts are diagnostics, not pass/fail quotas. Semantic
fidelity takes precedence over smaller counts.

## Optional is not safe

Use [reassurance-prompts.json](reassurance-prompts.json) with the unknown-reason
cases. An optional action or step stays optional; its consequences stay unknown
when the source does not state them. "Nothing will break", "safe to skip", "you
can safely stay" and similar reassurance are semantic failures unless the source
supports them. An invented risk is a failure too. Labelled possibilities are allowed.

## Bounds and conflicting facts

Use [bounds-conflicts-prompts.json](bounds-conflicts-prompts.json) with the
unknown-reason, roles and deadline cases as regression guards. "From", "at least",
"at most" and "more than" remain conditions; an exact or approximate number must
not replace them. When supplied facts conflict, the reply names the conflict and
does not resolve it by choice, average, range or an invented reason. A request for
a ready text may get the conflict and a question first. Do not require phrases.

## Unknown actors

Use [unknown-actor-prompts.json](unknown-actor-prompts.json) with the unknown-reason
and optional-backup cases. Passive or impersonal wording names no actor. A reply that
supplies developers, a company, management, an administrator, IT or a support team
absent from the source fails semantic fidelity. "You" for the reader is not an
invented actor.

## Warnings before the step

Use [warning-order-prompts.json](warning-order-prompts.json) with the
unknown-reason, roles, depth and verification cases. When the source states an
irreversible effect of a step, the reader learns it before the instruction to
take that step; a warning placed only after the step fails the protected
criterion. An invented warning, risk or extra requirement is a failure too,
including in the theme cases, where no warning is supplied.

## Assessor calibration and audit

Record the observed reply language separately. A wrong language lowers the
language dimension; a clear-looking reply in the wrong language is not a pass
for language compliance. Do not infer language solely from the question ID.

Ground a semantic failure in a quoted claim, lost requirement or unsupported
instruction. Explicitly conditional examples are not automatically facts about
the system. Correct time-zone conversions and the literal meaning of a deadline
are not inventions. Extra uncertainty may be clutter without a meaning failure.
Conversely, an authorization caveat does not establish why a destructive step is
needed. A result's recipient does not establish its direct transport route.

After locking judgments, audit claimed failures and suspected omissions against
the raw replies. Keep the locked results intact; record corrections separately
and disclose that this follow-up is unblinded. Model scoring is not authoritative
accuracy or reader comprehension, even when the schema validates.
