![Anton Chekhov with a fountain pen at his desk — Palych banner](assets/chekhov-banner.jpg)

# Palych — a Claude Code skill for concise, plain-language AI agent replies

Named in honor of A. P. Chekhov (А. П. Чехов).

Palych helps an agent answer compactly and clearly: the main point first, followed
by the explanation the reader needs. It's a Claude Code skill and a Codex skill
that gives you concise AI agent replies in plain language. Russian is the primary
language; English is also supported. After installation, the rules apply to every
reply, question and progress update. No separate skill invocation is needed.

[Русский](README.md)

## Why use it

Claude Code is often too verbose: it restates the question, opens with a preamble,
repeats the conclusion and uses jargon without explaining it. The usual fix is
typing “shorter” in every message or adding CLAUDE.md instructions for shorter
answers. Palych does this for every reply.

Palych doesn't cut text down to a telegraphic style. It removes filler but keeps
what matters: numbers, negations, limits, conditions and uncertainty. The result
is a plain-language AI agent, not a shortened copy of the same verbose answer.

## Install

Paste this message into your agent's chat:

```text
Install Palych from https://github.com/ponomr/palych using INSTALL.md.
Enable it for all replies without a separate invocation. Preserve my other instructions.
```

The agent will choose the route for its host: a plugin with a hook for Codex
and Claude Code, a skill for Hermes or a rule for Cursor. Palych does not write
into the agent's global instructions. In Claude Code the agent can also add the
[band above the prompt](#band-above-the-prompt). Start a new conversation afterward. Manual installation, updates and removal are in
[INSTALL.md](INSTALL.md).

## Main principles

- Follow the question's language; Russian remains the development priority.
- Lead with the answer. Keep conditions that change the conclusion nearby.
- Match the form to the question: definition, explanation, instructions, comparison or progress.
- Explain each point once. Add reference material or diagnostics when the task needs them.
- Use familiar words and concrete actions. Explain necessary terms at first use.
- Preserve connections between ideas; keep unknown causes unknown.
- Use the same name for the same concept. Replace ambiguous pronouns with names.
- Preserve exact meaning: numbers, negations, limits and uncertainty.
- Choose structure for the task. No mandatory word limit, next action or repeated status.

For agent work, Palych separates completed work from verified results and explains
errors without inventing a cause. Documents such as emails and reports follow
the user's requested style.

## Controls

“Turn off palych” disables it for this conversation. “Enable palych” turns it back
on. To disable the default for new conversations, remove the installer block as
described in [INSTALL.md](INSTALL.md). The plugin has separate
[persistent mode controls](adapters/README.md).

Palych adapts selected Easy-to-read guidance for chat. It assumes no reader
diagnosis and makes no claim of compliance with the full methodology.

[Sources](skills/palych/references/sources.md) · [Checks and limits](docs/STATUS.md) ·
[Development](docs/DEVELOPMENT.md). License: [MIT](LICENSE).

## Band above the prompt

![The Palych band above the prompt: the switch and usage figures](assets/palych-toggle-band.png)

The [palych-toggle](mods/palych-toggle/README.md) mod for Claude Code adds a
band above the prompt. It holds the Palych switch for the current conversation
and usage figures: the 5-hour (5h) and 7-day (7d) limits with the time until
they reset, and how full the context is (ctx). The terminal shows a text band.

`/palych-tab` hides the band; running it again brings it back. Hiding lasts
until the session ends.

The mod pairs with the `palych@palych` plugin and starts at its saved mode.
To install by hand:

```sh
claude plugin marketplace add ponomr/palych
claude plugin install palych@palych
claude plugin install palych-toggle@palych
```

## Example

**Question:** “Why does caching sometimes make a response faster and sometimes not?”

In this example, the cache stores completed results. If a result is missing,
the service computes it again.

**Without Palych:**

> Caching reduces latency on a cache hit. A cache miss triggers computation.
> Check TTL, eviction policy, hit rate and the invalidation mechanism.

**With Palych:**

> A cache can make a response faster when the result is already stored and
> retrieving it takes less time than computing it again.
>
> If the result is missing, the computation still happens, with the cache lookup
> adding extra time. That request can therefore be slightly slower.

This is an illustrative edit written for the package. It does not prove that a
particular model will always answer this way or that readers understand it better.

## Sample skill test results

Blind comparison on 13 October 2026: `claude-sonnet-5-5` replies without Palych and
with Palych from `main` 466fb77. 30 tasks in Russian and English, 3 replies per task,
90 pairs. The same model judged the pairs without knowing which reply was which.

| Measure | Without Palych | With Palych |
|---|---:|---:|
| Pair wins | 1 | 86 |
| Ties | 3 | 3 |
| Meaning errors | 45 | 3 |
| Output tokens | 38,284 | 20,918 (−45%) |
| Reply characters | 98,562 | 51,390 (−48%) |
| Input tokens per request | ~690 | ~3,300 |

A meaning error is an invented guarantee, picking one of conflicting facts or another
distortion of the task. Input tokens grow because the core is sent with every request,
so Palych reduces output tokens in Claude Code, not input tokens. This table is an
exploratory pilot, not a test of reader comprehension. Details are in
[STATUS.md](docs/STATUS.md).

## FAQ

**How do I reduce verbose AI responses without losing meaning?**\
Install Palych. It applies the same rules to every reply, so you don't have to
ask for “shorter” each time or write a separate prompt.

**Is it the same as “bottom line up front”?**\
Partly. Palych also puts the answer first and drops preambles, repetition and
empty caveats. It doesn't shorten for its own sake: the needed explanation,
conditions and uncertainty stay in the reply.

**How is it different from Claude Code's Concise output style?**\
Both shorten replies. Palych is a skill, so it also works in Codex, and it adds
rules for keeping exact meaning: numbers, conflicting facts, unknown causes and
the difference between done and verified.

**Is Palych a Caveman skill alternative?**\
Yes, with a different goal. Caveman makes replies terse and telegraphic. Palych
keeps full sentences and plain language and removes only what doesn't help the reader.

**How does Palych differ from other Claude Code skills?**\
Many agent skills give the agent new tasks. Palych changes how the agent writes
its replies and works all the time, without a separate invocation.

## Author

Alexey Ponomar\
Follow me on [X](https://x.com/ponomar) and [Telegram](https://t.me/ponomaround).
