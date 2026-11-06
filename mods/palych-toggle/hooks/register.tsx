import { atom, read, update } from 'claude-code'
import type { EngineInterface, Register } from 'claude-code'

import type { PalychTheme } from '../types'
import { pluginMode } from './palych-state'
import { D, desktopParts, fit, GROUP_GAP, readUsage, registerUsage, startUsage } from './usage'

// Session state: the switch starts where the Palych plugin's saved mode puts
// this conversation, on when there is none (Palych's own default).
const isOn = atom({ plugin: 'palych-toggle', key: 'isOn' } as const, true)
// Set once the switch took the plugin's mode, so a reload keeps the session's.
const synced = atom({ plugin: 'palych-toggle', key: 'synced' } as const, false)
// Set when the switch turns Palych back on; the next prompt tells the model once.
const isOnPending = atom(
  { plugin: 'palych-toggle', key: 'isOnPending' } as const,
  false,
)

// Hidden by /palych-tab for the rest of the session.
const hidden = atom({ plugin: 'palych-toggle', key: 'hidden' } as const, false)

// The desktop app's theme, so the switch matches the band it sits on.
const theme = atom(
  { plugin: 'palych-toggle', key: 'theme' } as const,
  'dark' as PalychTheme,
)

// The switch and its theme handling follow the auto-compact switch of the
// usage-quota mod (MIT, (c) 2026 Anant Raghunath).
const PALETTES = {
  dark: { off: '#4b5163', on: '#4ade80', lit: '#8b919c', muted: '#8b90a0' },
  light: { off: '#b4b9c4', on: '#22c55e', lit: '#c3c7cf', muted: '#5b6070' },
}
// The pill in pixels; the light under the pointer shows in the PAD around it.
const SWITCH_W = 30
const SWITCH_H = 20
const SWITCH_PAD = 3
// Cells the switch's box takes, so the press's tint can't spill onto the label.
const SWITCH_CELLS = 4
// Where the pill sits in its drawing, in px: measured in the app so the pill
// is centred in the light that shows under the pointer.
const SWITCH_SHIFT = { x: -0.75, y: 0 }
// Wider than the pill in any font size the band uses.
const PRESS_LABEL = '\u2003'.repeat(3)
// Fully see-through: the press's own hover tint.
const CLEAR = '#00000000'

const switchSvg = (active: boolean, fill: string): string => {
  const w = SWITCH_W - 2 * SWITCH_PAD
  const tall = SWITCH_H - 2 * SWITCH_PAD
  const p = SWITCH_PAD
  const knob = p + (active ? w - tall / 2 : tall / 2)

  return (
    `<svg xmlns="http://www.w3.org/2000/svg" width="${SWITCH_W}" height="${SWITCH_H}" viewBox="${-SWITCH_SHIFT.x} ${-SWITCH_SHIFT.y} ${SWITCH_W} ${SWITCH_H}">` +
    `<rect x="${p}" y="${p}" width="${w}" height="${tall}" rx="${tall / 2}" fill="${fill}"/>` +
    `<circle cx="${knob}" cy="${p + tall / 2}" r="${tall / 2 - 2}" fill="#ffffff"/></svg>`
  )
}

// Plugins aren't told the app's theme: read it from the app's settings
// (userThemeMode) and, for "system", from the OS.
const THEME_EVERY_MS = 2_000

const desktopConfig = async ($: EngineInterface): Promise<string | undefined> => {
  const appData = await $.env.get('APPDATA')
  if (appData) {
    return `${appData}/Claude/config.json`
  }
  const home = await $.env.get('HOME')

  return home ? `${home}/Library/Application Support/Claude/config.json` : undefined
}

const osTheme = async ($: EngineInterface): Promise<PalychTheme> => {
  try {
    if (await $.env.get('APPDATA')) {
      const { stdout } = await $.process.run(
        ['reg', 'query', 'HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize', '/v', 'AppsUseLightTheme'],
        { timeoutMs: 5_000 },
      )
      return /AppsUseLightTheme\s+REG_DWORD\s+0x1\b/.test(stdout) ? 'light' : 'dark'
    }
    const { stdout } = await $.process.run(
      ['defaults', 'read', '-g', 'AppleInterfaceStyle'],
      { timeoutMs: 5_000 },
    )
    return /dark/i.test(stdout) ? 'dark' : 'light'
  } catch {
    // macOS has no AppleInterfaceStyle in light mode; unknown stays dark.
    return 'dark'
  }
}

// Read the settings file again only when it changed since the last look.
let themeFile: { mtimeMs: number; mode: string | undefined } | undefined

const syncTheme = async ($: EngineInterface): Promise<void> => {
  let mode: string | undefined
  try {
    const path = await desktopConfig($)
    if (!path) {
      return
    }
    const { mtimeMs } = await $.fs.stat(path)
    if (themeFile?.mtimeMs === mtimeMs) {
      mode = themeFile.mode
    } else {
      mode = (JSON.parse(await $.fs.read(path)) as { userThemeMode?: string }).userThemeMode
      themeFile = { mtimeMs, mode }
    }
  } catch {
    return
  }
  const value = mode === 'light' || mode === 'dark' ? mode : await osTheme($)
  if (value !== (await read($, theme))) {
    await update($, theme, () => value)
  }
}

// Whole-message control phrases, the same list the Palych session hook reads.
const PHRASES: Record<string, boolean> = {
  'включи палыча': true,
  'включи палыча для этого разговора': true,
  'включи палыча всегда': true,
  'отключи палыча': false,
  'отключи постоянное включение палыча': false,
  'включи palych': true,
  'включи palych для этого разговора': true,
  'включи palych всегда': true,
  'отключи palych': false,
  'отключи постоянное включение palych': false,
  'enable palych': true,
  'enable palych for this conversation': true,
  'enable palych always': true,
  'turn off palych': false,
  'disable palych always-on': false,
}

const SOURCE =
  'Palych toggle (the user set it with the switch in the app; not typed in this message): '
const OFF_NOTE =
  SOURCE +
  'Palych is OFF for this conversation. Treat this as the user\'s explicit request to turn Palych off: do not apply Palych\'s reply rules until the switch turns it on again.'
const ON_NOTE =
  SOURCE +
  'Palych is ON again for this conversation. Apply Palych\'s reply rules from the instructions.'

// With the plugin's mode off its hook has not loaded the rules, and a note can't
// bring them; a typed phrase makes the hook load them.
const TYPE_TO_TURN_ON = 'Палыч выключен в плагине: напиши «Включи Палыча», и он загрузит правила'

const phraseMode = (text: string): boolean | undefined => {
  const phrase = text.trim().toLowerCase().replace(/\.$/, '')

  return PHRASES[phrase]
}

export const register: Register = on => {
  registerUsage(on)

  on('session.start', async ($, e, next) => {
    const result = await next(e)
    await $.command.register({
      name: 'palych-tab',
      description: 'Show or hide the Palych band above the prompt',
      immediate: true,
    })
    if (!(await read($, synced))) {
      const mode = await pluginMode($)
      if (mode !== undefined) {
        await update($, isOn, () => mode)
      }
      await update($, synced, () => true)
    }
    await syncTheme($)
    $.clock.every(THEME_EVERY_MS, () => void syncTheme($))
    await startUsage($)

    return result
  })

  on('command.run', { command: 'palych-tab' }, async $ => {
    await update($, hidden, value => !value)

    return { text: (await read($, hidden)) ? 'Панель Палыча скрыта' : 'Панель Палыча показана' }
  })

  on('prompt.submit', async ($, e, next) => {
    if (e.command || e.isMeta) {
      return next(e)
    }

    // A typed control phrase speaks for itself; keep the switch in step with it.
    const typed = phraseMode(e.text)
    if (typed !== undefined) {
      await update($, isOn, () => typed)
      await update($, isOnPending, () => false)

      return next(e)
    }

    let note: string | undefined
    if (!(await read($, isOn))) {
      note = OFF_NOTE
    } else if (await read($, isOnPending)) {
      note = ON_NOTE
      await update($, isOnPending, () => false)
    }

    if (note === undefined) {
      return next(e)
    }

    return next({ ...e, context: [...(e.context ?? []), note] })
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    if (e.props.hasSurvey || (await read($, hidden))) {
      return next(e)
    }

    const table = $.ui.resolve(e)
    const { Box, Button, Text } = table
    const Svg = e.surface === 'desktop' && 'Svg' in table ? table.Svg : undefined
    const colors = PALETTES[Svg ? await read($, theme) : 'dark']
    const active = await read($, isOn)

    const toggle = async () => {
      if (!active && (await pluginMode($)) === false) {
        $.ui.toast(TYPE_TO_TURN_ON)
        return
      }
      await update($, isOn, value => !value)
      // Only a switch back on after an off needs a one-time note.
      await update($, isOnPending, () => !active)
    }

    // «Палыч» and the switch come first and never wrap; the figures get the rest.
    const u = await readUsage($)

    let usage = null
    if (Svg) {
      // Each group is its own picture, so on a narrow band the groups wrap, not the switch.
      const parts = desktopParts(u)
      usage = parts.length ? (
        <Box
          key="usage"
          flexDirection="row"
          flexWrap="wrap"
          alignItems="center"
          columnGap={GROUP_GAP}
          flexShrink={1}
          minWidth={0}
        >
          {parts.map(p => (
            <Svg key={p.key} source={p.svg} alt={p.alt} width={p.width} height={D.h} />
          ))}
        </Box>
      ) : null
    } else if (u.m) {
      // Bars, then countdowns, give way first; past that the row wraps.
      // «Палыч», a gap, the switch, and a group gap after it.
      const reserve = 5 + 1 + 1 + GROUP_GAP
      const spans = fit(u, e.props.bodyColumns - reserve)
      usage = (
        <Box key="usage" flexDirection="row" flexWrap="wrap" flexShrink={1} minWidth={0}>
          {spans.map((sp, i) => (
            <Text key={`s${i}`} color={sp.color} dimColor={sp.dim}>
              {sp.text}
            </Text>
          ))}
        </Box>
      )
    }

    return (
      <Box
        flexDirection="row"
        alignItems="center"
        columnGap={GROUP_GAP}
        width="100%"
      >
        <Box key="palych" flexDirection="row" alignItems="center" columnGap={1} flexShrink={0}>
          <Text color={active ? undefined : colors.muted}>Палыч</Text>
          {Svg ? (
            <Box key="switch" width={SWITCH_CELLS} height={1} overflow="hidden">
              {/* Three layers of one size share a centre: the light, the pill, the press. */}
              <Box
                position="absolute"
                top={0}
                left={0}
                width={SWITCH_CELLS}
                height={1}
                borderStyle="round"
                borderColor={colors.lit}
                hover={{ backgroundColor: colors.lit }}
              />
              <Box
                position="absolute"
                top={0}
                left={0}
                width={SWITCH_CELLS}
                height={1}
                alignItems="center"
                justifyContent="center"
              >
                <Svg
                  alt={active ? 'Палыч вкл' : 'Палыч выкл'}
                  source={switchSvg(active, active ? colors.on : colors.off)}
                  width={SWITCH_W}
                  height={SWITCH_H}
                />
              </Box>
              {/* A desktop presses only where the label is drawn, and plain spaces there are
                  narrow and collapse. Em spaces neither collapse nor fall short of the pill.
                  The press gets room for the whole label, or the desktop cuts it to "…";
                  the switch's box clips what runs past the pill. */}
              <Box position="absolute" top={0} left={0} width={2 * SWITCH_CELLS} height={1}>
                <Button
                  key="palych-toggle"
                  label={PRESS_LABEL}
                  plain
                  hover={{ backgroundColor: CLEAR }}
                  onPress={toggle}
                />
              </Box>
            </Box>
          ) : (
            <Button key="palych-toggle" label={active ? '●' : '○'} plain onPress={toggle} />
          )}
        </Box>
        {usage}
      </Box>
    )
  })
}
