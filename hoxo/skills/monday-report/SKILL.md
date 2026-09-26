---
name: monday-report
description: "The weekly Hoxo standup. Generated on the client's chosen report day by the Hoxo system and stored in your account — this skill retrieves it and presents it. Covers 6 sections: Intelligence Report, Content Pipeline, Podcast Agent, ICP Outreach Packs, Performance Lens, Daily Orchestrator. Use when the user says /monday-report, 'run my standup', 'monday report', or 'weekly standup'."
---

# /monday-report

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "monday-report"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo plugin and sign in, then retry.
