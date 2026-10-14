# Hoxo plugin marketplace

One-install distribution of Hoxo for Claude (Cowork / Desktop / Code). Two plugins, one
connector, no zip uploads, no hidden `.cloud` folder:

- **Hoxo**: the Boardroom plugin, all 23 skills.
- **Hoxo Bootcamp**: the LinkedIn Revenue Bootcamp plugin, 12 skills.

## Install (client)

1. In Claude, go to **Customize → Plugins → Add marketplace → Add from a repository**
2. Paste this repo's GitHub URL
3. Install **ONE** plugin: **Hoxo** for Boardroom clients, **Hoxo Bootcamp** for LinkedIn
   Revenue Bootcamp clients. Same connector, same sign-in. Never install both, they
   duplicate skills on one connector.
4. Approve the Hoxo connector (OAuth) when prompted
5. Type `/` to see the skills

### Hoxo (Boardroom, 23 skills)

`hoxo-system-setup`, `voice-vault`, `monday-report`, `daily-engagement`, `write-comment`,
`create-content`, `analyse-content`, `podcast-guest`, `bd-outreach`, `refine-icp`, `buildout-icp-profile`,
`tbr-sync-kpis`, `tbr-sync-pipeline`, plus the LRB set below and `brand-skill-builder`.

### Hoxo Bootcamp (12 skills)

`hoxo-system-setup`, `daily-engagement`, `lrb-onboarding`, `lrb-content-engine`,
`lrb-ideas-bank`, `lrb-job-post`, `lrb-profile-builder`, `lrb-repurpose`,
`lrb-voice-notes`, `mpc-post-engine`, `linkedin-banner-creator`, `brand-skill-builder`.

`brand-skill-builder` needs a client that can run code (Python).

## Layout

```
.claude-plugin/marketplace.json   # marketplace manifest (2 plugins)
hoxo/                             # Boardroom
├── .claude-plugin/plugin.json    # plugin manifest
├── .mcp.json                     # Hoxo remote connector (HTTP + OAuth auto-discovered)
└── skills/<23 skills>/SKILL.md   # synced from hoxo-boardroom-skill-pack
hoxo-bootcamp/                    # Bootcamp
├── .claude-plugin/plugin.json
├── .mcp.json                     # byte-identical to hoxo/.mcp.json
└── skills/<12 skills>/SKILL.md
```

## Maintaining

Skills are **thin stubs**: each calls `get_skill_instructions` on the Hoxo connector and
follows what comes back. The real bodies live server-side (the MCP serves them from
`hoxo-boardroom-skill-pack`, the canonical source). So:

- **Editing a skill's body**: deploy the MCP server. Clients get it live, **no plugin
  update needed**. Except `brand-skill-builder` (below): the MCP never serves it, so a
  deploy ships nothing. Run `node scripts/sync-skills.mjs` and bump `version` in both
  `hoxo/` and `hoxo-bootcamp/` `plugin.json`.
- **Adding/removing a skill, or changing its name/description**: re-sync and republish:
  ```
  node scripts/sync-skills.mjs   # regenerates both plugins' skills from the pack
  #   (reads ../hoxo/hoxo-boardroom-skill-pack;
  #    override with SKILL_PACK=/path/to/hoxo-boardroom-skill-pack)
  ```
  then bump `version` in every plugin whose files changed, and push.
- **A skill changes plan**: edit `BOARDROOM_ONLY_PROMPTS` in `mcp-server/src/plan.ts` in
  the hoxo repo, then re-sync. `sync-skills.mjs` reads that list and gives Bootcamp every
  other pack skill (`brand-skill-builder` included); there is no copy here to update.
- `brand-skill-builder` is the one skill copied whole (body plus scripts, templates,
  references), because it runs local Python the MCP cannot serve.

Deploy the MCP server FIRST when adding a skill, the stub is useless until
`get_skill_instructions` knows the new name.

The connector URL lives in `hoxo/.mcp.json` and `hoxo-bootcamp/.mcp.json` (prod,
multi-tenant, OAuth identifies the client). Keep them identical.
