import { listSocialAccounts, zernioErrorResponse } from '@/lib/zernio'

// GET /api/zernio/accounts — social accounts connected in Zernio.
// Use an account's `_id` as `accountId` when creating a post.
export async function GET() {
  try {
    const accounts = await listSocialAccounts()
    return Response.json({
      accounts: accounts.map(a => ({
        id: a._id,
        platform: a.platform,
        username: a.username ?? null,
        displayName: a.displayName ?? null,
        profilePicture: a.profilePicture ?? null,
        needsReconnection: a.needsReconnection ?? false,
      })),
    })
  } catch (err) {
    return zernioErrorResponse(err)
  }
}
