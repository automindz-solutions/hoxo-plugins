---
name: tbr-sync-connections
description: "Optional. Reads the LinkedIn connections you added recently from your own LinkedIn in your Claude browser and adds them to Hoxo, where they are screened against your ICP, so new ICP connections show up in /daily-engagement and on the Network page without exporting a CSV. Read-only on LinkedIn. Use when the user says /tbr-sync-connections, 'sync my connections', 'add my new connections', 'import my new LinkedIn connections', or when a scheduled task runs it."
---

# /tbr-sync-connections

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "tbr-sync-connections"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo plugin and sign in, then retry.
