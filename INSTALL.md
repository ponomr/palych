# Установка / Installation

Палыч ставится как плагин. Его хук начала разговора (`SessionStart`) подаёт
правила в каждый новый разговор, после сжатия контекста и после `/clear`.
Палыч не пишет в общие инструкции агента: `~/.codex/AGENTS.md`,
`~/.claude/CLAUDE.md` и `developer_instructions` не меняются. Отдельный вызов
не нужен. Нужны Python 3 (для хука), Git и macOS/Linux.

Palych installs as a plugin. Its SessionStart hook supplies the rules to every
new conversation, after compaction and after `/clear`. Palych does not write
into the agent's global instructions: `~/.codex/AGENTS.md`, `~/.claude/CLAUDE.md`
and `developer_instructions` stay untouched. No invocation is needed. Requires
Python 3 (for the hook), Git and macOS/Linux.

## Инструкция для агента / Agent instructions

1. Определи используемый агент. Если его нельзя понять из контекста, уточни:
   Codex или Claude Code. Не вставляй правила Палыча в общие инструкции
   агента и не предлагай этого: такой установки больше нет.
2. Если Палыч ставился до 0.10.0 через общие инструкции, убери старый блок
   (раздел «Переход со старой установки»). Иначе правила загрузятся дважды.
3. Поставь плагин командами ниже. В Codex после установки обязательно
   разреши хук через `/hooks`. Для Claude Code по желанию поставь мод панели.
4. Попроси начать новый разговор. Если доступна проверка в хосте, проверь
   загрузку правил с первого сообщения и после сжатия контекста. Не заявляй
   об этой проверке без результата.

Identify the host; ask Codex or Claude Code when the context does not say. Do
not insert Palych's rules into the agent's global instructions or offer to:
that installation no longer exists. If Palych was installed before 0.10.0
through global instructions, remove the old block first (see "Migrating from
the old installation"), or the rules load twice. Install the plugin below; in
Codex, trust its hook in `/hooks`. For Claude Code the band mod is optional.
Start a new conversation. Verify actual host loading and compaction when
possible; file checks alone do not establish it.

## Claude Code

```sh
claude plugin marketplace add ponomr/palych
claude plugin install palych@palych
```

### Мод панели / Band mod

Мод [palych-toggle](mods/palych-toggle/README.md) рисует над полем ввода
переключатель Палыча и показатели usage; `/palych-tab` скрывает и показывает
панель. Переключатель начинает с сохранённого режима плагина.

The [palych-toggle](mods/palych-toggle/README.md) mod draws the Palych switch
and usage figures above the prompt; `/palych-tab` hides or shows the band. The
switch starts at the plugin's saved mode.

```sh
claude plugin install palych-toggle@palych
```

Плагин и мод появятся в новой сессии Claude Code. / The plugin and the mod
appear in a new Claude Code session.

## Codex

```sh
codex plugin marketplace add ponomr/palych
codex plugin add palych@palych
```

Или установи Palych в каталоге плагинов приложения Codex.
Or install Palych from the Codex app's plugin directory.

**Обязательный шаг: разреши хук.** Codex не запускает хуки плагина, пока
пользователь их не проверил и не разрешил. Без этого плагин числится включённым,
но правила не загружаются, и Codex не сообщает об ошибке. После установки открой
в Codex CLI команду `/hooks`, найди хук Палыча и разреши его. Codex запоминает
разрешение для текущего определения хука: если после обновления он снова
попросит открыть `/hooks`, разреши хук ещё раз. Затем начни новый разговор
и проверь, что правила загружены.

**Required: trust the hook.** Codex does not run plugin hooks until the user
reviews and trusts them. Until then the plugin is listed as enabled but loads
no rules, and Codex reports no error. After installing, open `/hooks` in the
Codex CLI, find Palych's hook and trust it. Codex records trust for the current
hook definition: if it asks you to open `/hooks` again after an update, trust
the hook again. Then start a new conversation and check that the rules are loaded.

Обновление: обнови каталог и поставь плагин заново. Update: refresh the
marketplace and add the plugin again:

```sh
codex plugin marketplace upgrade palych
codex plugin add palych@palych
```

Плагины Claude Code и Codex используют хук начала разговора (`SessionStart`)
и хранят состояние режима отдельно. В новой установке режим включён. Сохранённое
выключение переживает обновление. После сжатия правила восстанавливаются, если
хост отправляет событие `compact`. Команды режима — в
[adapters/README.md](adapters/README.md).

The Claude Code and Codex plugins use a SessionStart hook and store mode state
separately. A fresh installation defaults to on; a saved off state survives
updates. Rules return after compaction when the host delivers the compact event.
See [adapters/README.md](adapters/README.md) for mode controls.

## Переход со старой установки / Migrating from the old installation

До 0.10.0 `scripts/install.py` вставлял блок `<!-- palych:start -->…<!-- palych:end -->`
в `~/.codex/AGENTS.md` (или `AGENTS.override.md`) и `~/.claude/CLAUDE.md`. Этот
путь удалён. Пока блок на месте, хук плагина видит его, не добавляет вторую
копию правил и просит убрать блок. Удалить блок:

Before 0.10.0 `scripts/install.py` inserted a `<!-- palych:start -->…<!-- palych:end -->`
block into `~/.codex/AGENTS.md` (or `AGENTS.override.md`) and `~/.claude/CLAUDE.md`.
That route is gone. While the block remains, the plugin's hook detects it,
adds no second copy and asks for its removal. Remove it:

```sh
git clone https://github.com/ponomr/palych.git
cd palych
python3 scripts/remove_global_block.py check --host codex
python3 scripts/remove_global_block.py remove --host codex
python3 scripts/remove_global_block.py check --host claude-code
python3 scripts/remove_global_block.py remove --host claude-code
```

`check` ничего не меняет и завершается с кодом 1, пока блок найден. `remove`
вырезает только нетронутый блок, остальной текст сохраняет байт в байт и
кладёт резервную копию в `.palych-backups/` рядом с файлом. Изменённый вручную
блок и связанный (symlink) файл скрипт не трогает: их правят через тот
процесс, который ими управляет. Каталог настроек берётся из `CODEX_HOME` или
`CLAUDE_CONFIG_DIR`, другой можно задать через `--config-dir`.

`check` changes nothing and exits 1 while a block is found. `remove` cuts only
an intact block, keeps the rest byte for byte and saves a backup under
`.palych-backups/` beside the file. It refuses hand-edited blocks and linked
files: change those through their managing workflow. The configuration
directory comes from `CODEX_HOME` or `CLAUDE_CONFIG_DIR`; `--config-dir`
selects another.

Если общие инструкции генерирует другой репозиторий или установщик, убери
блок в его источнике. / If another repository or installer generates the
global instructions, remove the block at that source.

## Обновление / Update

```sh
claude plugin marketplace update palych
claude plugin update palych@palych
claude plugin update palych-toggle@palych
```

Codex — см. выше. Сохранённый режим переживает обновление. Затем начни новый
разговор. / For Codex see above. A saved mode survives updates. Start a new
conversation afterwards.

## Отключение и удаление / Disable and remove

«Отключи Палыча» / “Turn off palych” — выключить в текущем разговоре.
«Включи Палыча» / “Enable palych” — вернуть в текущем разговоре.
«Отключи постоянное включение Палыча» / “Disable palych always-on” — новые
разговоры начинаются выключенными; хук сохраняет это в своём состоянии.
Все фразы — в [adapters/README.md](adapters/README.md).

Удаление / Remove:

```sh
claude plugin uninstall palych@palych
claude plugin uninstall palych-toggle@palych
codex plugin remove palych@palych
```

Начни новый разговор. / Start a new conversation.

## Другие агенты / Other hosts

Готовые пакеты лежат в `packages/` и собираются из `SKILL.md`.
Ready-made packages live in `packages/` and are generated from `SKILL.md`.

**Hermes:**

```sh
hermes skills install ponomr/palych/skills/palych
```

Путь `packages/hermes/palych` больше не публикуется. Если скилл стоит оттуда,
удалите его и поставьте заново командой выше.
The `packages/hermes/palych` path is no longer published. If the skill was
installed from it, uninstall it and install again with the command above.

Hermes загружает скилл с начала разговора, если запустить его с флагом
(проверено на v0.16.0 и v0.22.0):
Hermes preloads the skill when started with the flag (checked on v0.16.0 and
v0.22.0):

```sh
hermes -s palych
```

В Hermes v0.22.0 есть настройка `skills.auto_load` в `config.yaml` профиля: она
загружает перечисленные скиллы в каждый новый разговор. Мы видели её в коде
Hermes, но с Палычем не проверяли. В v0.16.0 её нет.
Hermes v0.22.0 has a `skills.auto_load` list in the profile's `config.yaml` that
loads the listed skills into every new session. It was seen in the Hermes source
but not tested with Palych; v0.16.0 lacks it:

```yaml
skills:
  auto_load:
    - palych
```

Скилл, поставленный из GitHub, удаляется командой `hermes skills uninstall palych`.
A skill installed from GitHub is removed with `hermes skills uninstall palych`.

**Cursor:** пакет `packages/cursor` — плагин с правилом `rules/palych.mdc`
(`alwaysApply: true`). До публикации в каталоге Cursor поставь его как локальный
плагин для всех проектов (проверено на Cursor 3.24.18):
The `packages/cursor` package is a plugin with an always-applied rule. Until it
is listed in Cursor's marketplace, install it as a local plugin for all projects
(checked on Cursor 3.24.18):

```sh
git clone https://github.com/ponomr/palych.git ~/palych-src
mkdir -p ~/.cursor/plugins/local
cp -R ~/palych-src/packages/cursor ~/.cursor/plugins/local/palych
```

Удаление — `rm -r ~/.cursor/plugins/local/palych`. Для одного проекта можно
вместо плагина скопировать `rules/palych.mdc` в `.cursor/rules/` проекта (этот
путь не проверялся). Remove it with `rm -r ~/.cursor/plugins/local/palych`. For a
single project, copying `rules/palych.mdc` into the project's `.cursor/rules/`
is an alternative (not checked).

**Другие агенты / Other agents:**

```sh
npx skills add ponomr/palych
```

Команда ставит только папку `skills/palych` (`SKILL.md`, примеры, лицензию) как
обычный скилл. Агент вызывает его по описанию, а не в каждом ответе. Удаление —
`npx skills remove palych`.

It installs only the `skills/palych` folder (`SKILL.md`, examples, license) as a
regular skill that the agent invokes by description, not in every reply. Remove it
with `npx skills remove palych`.

В Hermes и Cursor нет хуков Палыча: «Отключи Палыча» действует только
в текущем разговоре. Постоянно отключить — удалить скилл или правило.
Hermes and Cursor have no Palych hooks: “Turn off palych” lasts only
for the current conversation. Remove the skill or rule to disable it
permanently.

## Проверка в агенте / Host verification

В новом разговоре задай обычный вопрос без имени Палыча. Проверь контекст,
который доставил хук: правила Палыча должны быть там. Затем отключи режим,
сожми контекст средствами хоста и проверь, что выключение сохранено в этом
разговоре. В новом разговоре режим должен снова включиться. Стиль одного
ответа сам по себе не доказывает загрузку правил.

In a new conversation, ask an ordinary question without mentioning Palych and
inspect the hook's delivered context for the rules. Turn it off, compact the
conversation and check that off is retained. A new conversation should default
to on again. Reply style alone does not prove that the rules loaded.

[Проверено и не проверено в Палыче](docs/STATUS.md).
