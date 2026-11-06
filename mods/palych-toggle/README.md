# Переключатель Палыча / Palych toggle

![Панель Палыча / The Palych band](../../assets/palych-toggle-band.png)

Мод для Claude Code: над полем ввода стоит панель. Первыми идут надпись
«Палыч» и переключатель, который включает и выключает режим в текущем
разговоре. В приложении это зелёная таблетка в стиле iOS в цветах темы
приложения; в терминале — кнопка `●` (вкл) или `○` (выкл). Дальше идут
показатели usage: 5h и 7d — доля лимита и время до сброса, ctx — сколько
токенов занято в окне контекста. На узкой панели показатели переносятся на
следующую строку, а переключатель остаётся на месте.

A Claude Code mod: a band sits above the prompt. The label «Палыч» and a
switch come first and turn the mode on or off for the current conversation.
The desktop app draws an iOS-style pill in the app theme's colours; the
terminal draws a `●` (on) or `○` (off) button. Usage figures follow: 5h and
7d show the share of the limit used and the time until it resets, ctx the
tokens used in the context window. On a narrow band the figures wrap to the
next line; the switch stays put.

`/palych-tab` скрывает панель, повторный вызов возвращает её; скрытие
действует до конца сессии. / `/palych-tab` hides the band and running it
again brings it back; hiding lasts until the session ends.

## Установка / Install

Мод работает вместе с плагином `palych@palych`: плагин загружает правила,
мод даёт переключатель. Установка по [INSTALL.md](../../INSTALL.md) ставит
оба. / The mod pairs with the `palych@palych` plugin: the plugin loads the
rules, the mod adds the switch. [INSTALL.md](../../INSTALL.md) installs both.
Вручную / By hand:

```sh
claude plugin marketplace add ponomr/palych
claude plugin install palych@palych
claude plugin install palych-toggle@palych
```

Удаление / Remove: `claude plugin uninstall palych-toggle@palych`.

## Как работает / How it works

При старте сессии мод читает сохранённый режим плагина
(`~/.local/state/palych/claude-code/state.json`: выбор этого разговора, иначе
режим по умолчанию) и ставит переключатель так же. Мод не меняет файлы и
настройки. Пока переключатель выключен, к каждому сообщению пользователя
добавляется скрытая для пользователя пометка: Палыч выключен, это явная
просьба пользователя. Правила Палыча уже требуют исполнять такую просьбу.
После включения следующее сообщение один раз получает пометку о включении.

At session start the mod reads the plugin's saved mode (this conversation's
choice, else the default) and sets the switch to match. It edits no files or
settings. While the switch is off, every user message carries a note the user
does not see: Palych is off at the user's explicit request, which Palych's
rules already honour. Switching it back on adds a one-time note to the next
message.

Если в плагине Палыч выключен, его правил в контексте нет, и пометка их не
вернёт. Тогда нажатие не включает переключатель, а показывает подсказку:
написать «Включи Палыча». Эту фразу ловит хук плагина и загружает правила.

With Palych off in the plugin its rules are not in context and a note cannot
bring them. The switch then stays off and a toast asks the user to type
«Включи Палыча»; the plugin's hook catches that phrase and loads the rules.

Фразы управления из `adapters/README.md`, отправленные отдельным сообщением
(«Отключи Палыча», “Turn off palych”), двигают переключатель тоже.

The control phrases from `adapters/README.md`, sent as a whole message, move
the switch too.

Переключатель и определение темы взяты из переключателя auto compact мода
usage-quota (MIT, © 2026 Anant Raghunath). Чтобы узнать тему, мод раз в 2 с
проверяет `userThemeMode` в настройках приложения Claude
(`~/Library/Application Support/Claude/config.json` или
`%APPDATA%/Claude/config.json`), а для «system» спрашивает ОС
(`defaults read -g AppleInterfaceStyle` или реестр Windows).

The switch and the theme detection come from the usage-quota mod's auto
compact switch (MIT, © 2026 Anant Raghunath). To learn the theme, the mod
checks `userThemeMode` in the Claude app's settings every 2 s and, for
"system", asks the OS.

Рисунок показателей перенесён из
[usage-band](https://github.com/JetsonChan/CC-Usage-Band) (коммит 60cd609,
MIT, © 2026 Jetson Chan) без анимации полосок и доли попаданий в кэш.
Обновление показателей сделано по образцу
[usage-line](https://github.com/sundyme/usage-line) (коммит 194c8f7, MIT,
© 2026 sundyme).

The figures' drawing is ported from usage-band (commit 60cd609, MIT, © 2026
Jetson Chan) without its bar animation and cache-hit figure. Keeping the
figures current follows usage-line (commit 194c8f7, MIT, © 2026 sundyme).

## Ограничения / Limits

- Выключение переключателем действует только в этом разговоре и не
  сохраняется в плагине; сохранённый режим меняют фразы управления. / The
  switch's off lasts for this conversation and is not saved in the plugin;
  control phrases change the saved mode.
- Без файла состояния плагина (плагин не ставился или ещё не запускался)
  переключатель начинает с «вкл». / Without the plugin's state file the
  switch starts on.
- Другие формулировки выключения модель поймёт, но переключатель о них не
  узнает. / Other wording reaches the model but does not move the switch.
- Пометка — инструкция модели, а не удаление правил из контекста. В живой
  сессии приложения видно, что пометка доходит до модели; стиль ответов
  систематически не оценивался. / The note is an instruction to the model, not
  removal of the rules from context. A live desktop session shows the note
  reaching the model; reply style was not evaluated systematically.
- Нажатие срабатывает только там, где приложение рисует подпись кнопки,
  поэтому подпись невидимой кнопки — три широких пробела поверх таблетки. /
  The app presses a button only where its label is drawn, so the invisible
  button's label is three em spaces laid over the pill.
- Показатели появляются, когда Claude Code сообщает о лимитах и контексте;
  до этого на панели только переключатель. / The figures appear once Claude
  Code reports limits and context; until then the band holds only the switch.

## Проверка / Checks

```sh
claude plugin validate mods/palych-toggle
claude plugin test mods/palych-toggle
```

Для пробного запуска / To try it in one session:

```sh
claude --plugin-dir mods/palych-toggle
```
