# Hoxo plugin marketplace

One-install distribution of the Hoxo BD engine for Claude (Cowork / Desktop / Code).
Bundles the **Hoxo connector** + all **9 skills** as slash commands — no zip uploads,
no hidden `.cloud` folder.

## Install (client)

1. In Claude → **Customize → Plugins → Add marketplace → Add from a repository**
2. Paste this repo's GitHub URL
3. Install the **Hoxo** plugin → approve the Hoxo connector (OAuth) when prompted
4. Type `/` → `hoxo-system-setup`, `voice-vault`, `monday-report`, `daily-engagement`,
   `write-comment`, `create-content`, `analyse-content`, `podcast-guest`, `bd-outreach`

## Layout

```
.claude-plugin/marketplace.json   # marketplace manifest (1 plugin: hoxo)
hoxo/
├── .claude-plugin/plugin.json    # plugin manifest
├── .mcp.json                     # Hoxo remote connector (HTTP + OAuth auto-discovered)
└── skills/<9 skills>/SKILL.md     # synced from hoxo-boardroom-skill-pack
```

## Maintaining

The plugin's skills are **thin stubs** — each just calls `get_skill_instructions` on the
Hoxo connector and follows what comes back. The real skill bodies live server-side (the
MCP serves them from `hoxo-boardroom-skill-pack`, the canonical source). So:

- **Editing a skill's body** → just deploy the MCP server. Clients get it live, **no plugin
  update needed** (this sidesteps the marketplace cache/pinning that strands updates).
- **Adding/removing a skill, or changing its name/description** → re-stub and republish:
  ```
  node scripts/sync-skills.mjs            # regenerate stubs from the skill-pack
  #   (reads ../internal-workflows/clients/hoxo/hoxo-boardroom-skill-pack;
  #    override with SKILL_PACK=/path/to/hoxo-boardroom-skill-pack)
  # bump hoxo/.claude-plugin/plugin.json "version", then push

  Deploy the MCP server FIRST when adding a skill — the stub is useless until
  `get_skill_instructions` knows the new name.
  ```

The connector URL lives in `hoxo/.mcp.json` (prod, multi-tenant — OAuth identifies the
client, so one URL serves everyone).
