# Skill packs

Four third-party Claude skill packs, installed project-local in `.claude/skills/`
so they load automatically in any Claude Code session opened on this repo.
All four are MIT-licensed by Jake Schincariol; each pack's licence is kept in
its folder here.

| pack | skills | source | commit |
| --- | --- | --- | --- |
| Instagram agent | `/ig-*` (13) | https://github.com/Jakeschincariol/instagram-agent-skill | `d03c56b` |
| LinkedIn agent | `/li-*` (11) | https://github.com/Jakeschincariol/linkedin-agent-skill | `add2c23` |
| YouTube agent | `/yt-*` (11) | https://github.com/Jakeschincariol/youtube-agent-skill | `a2feb21` |
| Replica | `/replica-*` (11) | https://github.com/Jakeschincariol/replica-skill | `77c9436` |

The skill folders are copied unmodified from those commits. The bundled Python
tools are standard-library only and make no network calls.

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

The Replica pack keeps its working files in a `replica/` folder at the project
root instead.

## Updating

Re-clone the source repo and copy its skill folders over the ones in
`.claude/skills/` (`skills/<prefix>-*` for the social packs, `replica-*` at the
root of the Replica repo), then update the commit column above.
