export type PalychToggleMode = boolean
export type PalychTheme = 'dark' | 'light'

// Usage figures, as the band keeps them.
export type Limit = { kind: string; percentUsed: number; resetsAt?: string }
export type Ctx = { tokens?: number; window: number; percent?: number }
export type Style = 'nerd' | 'unicode' | 'ascii'

declare module 'claude-code' {
  interface PluginState {
    'palych-toggle': {
      isOn: PalychToggleMode
      isOnPending: boolean
      synced: boolean
      theme: PalychTheme
      hidden: boolean
      now: number
      ctx: Ctx | null
      limits: Limit[]
      style: Style
    }
  }
}
