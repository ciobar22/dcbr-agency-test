# Skill packs

Third-party Claude skill packs, installed project-local in `.claude/skills/` so
they load automatically in any Claude Code session opened on this repo. Each
pack's licence is kept in its folder here.

| pack | skills | source | commit | licence |
| --- | --- | --- | --- | --- |
| Instagram agent | `/ig-*` (13) | https://github.com/Jakeschincariol/instagram-agent-skill | `d03c56b` | MIT |
| LinkedIn agent | `/li-*` (11) | https://github.com/Jakeschincariol/linkedin-agent-skill | `add2c23` | MIT |
| YouTube agent | `/yt-*` (11) | https://github.com/Jakeschincariol/youtube-agent-skill | `a2feb21` | MIT |
| Replica | `/replica-*` (11) | https://github.com/Jakeschincariol/replica-skill | `77c9436` | MIT |
| Founder | `/founder-*` (11) | https://github.com/Jakeschincariol/founder-skill | `fd9385b` | MIT |
| HyperFrames video | `/hyperframes*`, `/general-video`, `/media-use`, `/product-launch-video`, `/talking-head-recut` (12) | https://github.com/heygen-com/hyperframes (`skills/`) | `b72c3fb` | Apache-2.0 |
| Media router | `/media-router` (1) | https://github.com/Jakeschincariol/video-production-skills | `f80248b` | none stated |

The skill folders are copied unmodified from those commits.

The five Jake Schincariol packs ship standard-library Python tools that make no
network calls.

## HyperFrames video skills

`/hyperframes` is the entry point and routes a video request to the right
workflow. Rendering uses the HyperFrames CLI (`npx hyperframes`, fetched from
npm on first use) and `ffmpeg`. Some `media-use` operations call HeyGen or
other providers with your own credentials.

These 12 were requested from `Jakeschincariol/video-production-skills`, which
is an older copy of HeyGen's skills without their licence. They were installed
from HeyGen's official repo instead. Its other workflows (`faceless-explainer`,
`pr-to-video`, `motion-graphics` and more) are not installed; some upstream
tests expect them.

**Telemetry is off.** `media-use` and the HyperFrames CLI send usage events to
HeyGen's PostHog unless opted out. `.claude/settings.json` sets
`HYPERFRAMES_NO_TELEMETRY=1` for every session on this repo.

`/media-router` is an Arcads skill. It routes image and video generate/edit
requests to the Arcads MCP server only, and stops with a "connect Arcads"
message when that server is not connected.

## Voice profiles

The Instagram, LinkedIn and YouTube skills read a voice profile before writing
anything. Templates:

- `instagram-agent/templates/voice.md` -> `~/.claude/instagram/voice.md`
- `linkedin-agent/templates/voice.md` -> `~/.claude/linkedin/voice.md`
- `youtube-agent/templates/voice.md` -> `~/.claude/youtube/voice.md`

Those skills also keep `log.md`, `plan.md` and `swipe.md` in the same
`~/.claude/<platform>/` folders. In a cloud session the home directory is
discarded when the container is reclaimed, so copy anything worth keeping
into the repo.

The Replica and Founder packs keep their working files in the project instead,
in `replica/` and `founder/` at the repo root. The HyperFrames workflows write
to `videos/<project>/`.

`/founder-consumer` runs one sub-agent per simulated buyer, 100 by default.
Use `--quick` (20 buyers) for a first look.

## Updating

Re-clone the source repo and copy its skill folders over the ones in
`.claude/skills/` (`skills/<name>` in most packs, top-level folders in the
Replica repo), then update the commit column above.
