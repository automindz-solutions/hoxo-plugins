---
name: tbr-sync-kpis
description: "Optional. Reads the impressions, reach and audience demographics of your own recent LinkedIn posts from LinkedIn's analytics pages in your Claude browser and saves them to Hoxo, so reports can show who a post actually reached, not only who liked it. Read-only on LinkedIn. Use when the user says /tbr-sync-kpis, 'sync my post KPIs', 'update my impressions', 'pull my post analytics', or 'who did my posts reach'."
---

# /tbr-sync-kpis

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "tbr-sync-kpis"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo plugin and sign in, then retry.
