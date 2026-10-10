import { NextRequest } from 'next/server'
import { createSocialPost, zernioErrorResponse, type SocialPostInput } from '@/lib/zernio'

// POST /api/zernio/posts — publish, schedule or draft a post through Zernio.
// Body is Zernio's create-post payload plus an optional idempotencyKey, e.g.
// {
//   content: 'Caption with #hashtags',
//   platforms: [{ platform: 'linkedin', accountId: '<id from /api/zernio/accounts>', customContent?: '...' }],
//   mediaItems?: [{ url: 'https://...', type: 'image' }],
//   publishNow?: true, scheduledFor?: '2026-11-01T10:00:00Z', timezone?: 'Europe/Bucharest',
//   idempotencyKey?: '<uuid, reused on retries>'
// }
// Without publishNow or scheduledFor, Zernio saves the post as a draft.
export async function POST(req: NextRequest) {
  let input: unknown
  try {
    input = await req.json()
  } catch {
    return Response.json({ error: 'Invalid JSON body' }, { status: 400 })
  }
  if (!input || typeof input !== 'object' || Array.isArray(input)) {
    return Response.json({ error: 'Body must be a JSON object' }, { status: 400 })
  }

  const { idempotencyKey, ...body } = input as SocialPostInput & { idempotencyKey?: string }

  try {
    const { data, status } = await createSocialPost(body, idempotencyKey)
    return Response.json(data, { status })
  } catch (err) {
    return zernioErrorResponse(err)
  }
}
