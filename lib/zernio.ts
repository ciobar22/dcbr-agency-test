import Zernio, { ZernioApiError } from '@zernio/node'
import type { CreatePostData, SocialAccount } from '@zernio/node'

// Zernio (https://zernio.com) — one API to schedule and publish posts across
// Instagram, TikTok, LinkedIn, X, Facebook, YouTube, Threads, Pinterest, etc.
// Server-only: the client reads ZERNIO_API_KEY from the environment, so never
// import this file from a client component.

export type SocialPostInput = CreatePostData['body']

let zernio: Zernio | null = null

export function isZernioConfigured(): boolean {
  return Boolean(process.env.ZERNIO_API_KEY)
}

export function getZernio(): Zernio {
  if (!zernio) zernio = new Zernio()
  return zernio
}

// ── Accounts ────────────────────────────────────────────────────────

// Social accounts connected in the Zernio dashboard. Each account's `_id` is
// the `accountId` to target when creating a post.
export async function listSocialAccounts(): Promise<SocialAccount[]> {
  const { data } = await getZernio().accounts.listAccounts({
    query: { category: 'social', excludeHidden: true },
  })
  return data?.accounts ?? []
}

// ── Posts ───────────────────────────────────────────────────────────

// Creates a post. With `publishNow` it publishes immediately (HTTP 207 when some
// platforms fail), with `scheduledFor` it is scheduled, and with neither it is
// saved as a draft. Reuse the same idempotencyKey when retrying the same post.
export async function createSocialPost(body: SocialPostInput, idempotencyKey?: string) {
  const { data, response } = await getZernio().posts.createPost({
    body,
    headers: idempotencyKey ? { 'Idempotency-Key': idempotencyKey } : undefined,
  })
  return { data, status: response.status }
}

// ── Errors ──────────────────────────────────────────────────────────

export function zernioErrorResponse(err: unknown): Response {
  if (err instanceof ZernioApiError) {
    if (err.code === 'missing_api_key') {
      return Response.json({ error: 'Zernio is not configured: set ZERNIO_API_KEY' }, { status: 503 })
    }
    return Response.json(
      { error: err.message, code: err.code, param: err.param, details: err.details },
      { status: err.statusCode }
    )
  }
  const message = err instanceof Error ? err.message : 'Zernio request failed'
  return Response.json({ error: message }, { status: 502 })
}
