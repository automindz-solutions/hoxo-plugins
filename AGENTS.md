# Hoxo plugin — agent instructions

This repo **is** the Claude connector clients install. It is public.

```
hoxo/                            # Boardroom, all pack skills
├── .claude-plugin/plugin.json   # name + version  ← MUST be bumped on every release
├── .mcp.json                    # the MCP endpoint (hardcoded)
└── skills/                      # thin stubs; bodies are served live by the MCP
hoxo-bootcamp/                   # Bootcamp: pack minus hoxo's BOARDROOM_ONLY_PROMPTS; same layout
```

## Releasing — bump the version, always

**Changing `.mcp.json` (or anything else) without bumping `version` in
the plugin's `.claude-plugin/plugin.json` (`hoxo/` and `hoxo-bootcamp/`) ships nothing.** Claude keys its update check on that
version: existing installs see no new version, Update does nothing, and everyone keeps
talking to the old endpoint. It looks exactly like "the change didn't work".

So every release is two edits in one commit:

1. the change itself
2. `version` bumped in every plugin.json whose plugin changed (`hoxo/`, `hoxo-bootcamp/`)

Even with a bump, the third-party Update button has been unreliable. If an install
won't take the update, the fallback is: remove the plugin **and** its connector →
re-add the marketplace → install → re-consent through OAuth.

## The MCP endpoint is a contract

`hoxo/.mcp.json` (and its byte-identical copy `hoxo-bootcamp/.mcp.json`) hardcodes the MCP URL. Changing it forces **every client to reconnect
once** (fresh OAuth consent) — there is no silent migration. Treat the hostname as
permanent and move the server behind it via DNS instead of editing this file.

Current: `https://hoxo-mcp.automindz.app/mcp`

## Skills are stubs

The skill files here are deliberately thin — they call the MCP for their real
instructions. That means skill copy can be updated server-side without shipping a
plugin release. Don't inline skill bodies back into this repo; it re-introduces the
release cycle we removed.

Exception: `brand-skill-builder` ships its full body plus scripts, templates and
references, because it runs local Python the MCP cannot serve. It is the only skill
allowed to; `scripts/sync-skills.mjs` copies it whole because its pack dir holds more
than `SKILL.md`. The MCP never serves it, so a change to it ships only by re-syncing
and bumping both plugins' versions.

## Admin plugin

`hoxo-admin-plugins` is the separate admin-side connector and follows the same rules.
