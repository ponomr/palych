import type { EngineInterface } from 'claude-code'

// The Palych plugin's session hook keeps its mode in this file
// (adapters/session_hook.py): { always_on, sessions: { sha256(session id): bool } }.
const STATE = '.local/state/palych/claude-code/state.json'

const K = [
  0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
  0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
  0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
  0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
  0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
  0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
  0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]

const utf8 = (text: string): number[] => {
  const bytes: number[] = []
  for (const part of encodeURIComponent(text).split(/(%[0-9A-F]{2})/i)) {
    if (part.startsWith('%')) {
      bytes.push(parseInt(part.slice(1), 16))
    } else {
      for (const ch of part) {
        bytes.push(ch.charCodeAt(0))
      }
    }
  }
  return bytes
}

// The modules have no crypto API; the hook keys sessions by this hex digest.
export const sha256 = (text: string): string => {
  const bytes = utf8(text)
  const bits = bytes.length * 8
  bytes.push(0x80)
  while (bytes.length % 64 !== 56) {
    bytes.push(0)
  }
  for (let i = 7; i >= 0; i--) {
    bytes.push(i >= 4 ? 0 : (bits >>> (8 * i)) & 0xff)
  }
  const h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
  const w = new Array<number>(64)
  const rotr = (x: number, n: number) => (x >>> n) | (x << (32 - n))
  for (let off = 0; off < bytes.length; off += 64) {
    for (let i = 0; i < 16; i++) {
      const j = off + 4 * i
      w[i] = (bytes[j] << 24) | (bytes[j + 1] << 16) | (bytes[j + 2] << 8) | bytes[j + 3]
    }
    for (let i = 16; i < 64; i++) {
      const s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ (w[i - 15] >>> 3)
      const s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ (w[i - 2] >>> 10)
      w[i] = (w[i - 16] + s0 + w[i - 7] + s1) | 0
    }
    let [a, b, c, d, e, f, g, k] = h
    for (let i = 0; i < 64; i++) {
      const t1 = (k + (rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)) + ((e & f) ^ (~e & g)) + K[i] + w[i]) | 0
      const t2 = ((rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)) + ((a & b) ^ (a & c) ^ (b & c))) | 0
      k = g
      g = f
      f = e
      e = (d + t1) | 0
      d = c
      c = b
      b = a
      a = (t1 + t2) | 0
    }
    const next = [a, b, c, d, e, f, g, k]
    for (let i = 0; i < 8; i++) {
      h[i] = (h[i] + next[i]) | 0
    }
  }
  return h.map(x => (x >>> 0).toString(16).padStart(8, '0')).join('')
}

/**
 * This conversation's mode as the Palych plugin saved it: the session's own
 * choice, else the plugin's default. Undefined when the plugin's state is
 * missing or unreadable, as without the plugin.
 */
export async function pluginMode($: EngineInterface): Promise<boolean | undefined> {
  try {
    const home = (await $.env.get('HOME')) ?? (await $.env.get('USERPROFILE'))
    if (!home) {
      return undefined
    }
    const state = JSON.parse(String(await $.fs.read(`${home}/${STATE}`))) as {
      always_on?: unknown
      sessions?: Record<string, unknown>
    }
    const own = state.sessions?.[sha256(await $.session.id())]
    if (typeof own === 'boolean') {
      return own
    }
    return typeof state.always_on === 'boolean' ? state.always_on : undefined
  } catch {
    return undefined
  }
}
