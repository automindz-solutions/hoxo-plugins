---
name: daily-engagement
description: "Builds today's engagement report in Claude from live Hoxo data: ICP-matched people who engaged with your posts since your last report, people to review, follow-ups due, new ICP connections and fresh Dream 100 posts to comment on, with replies drafted in your voice. Publishes it as an artifact and saves a copy to the Reports tab in Hoxo. Works at any time of day. Use when the user says /daily-engagement, 'daily digest', 'daily engagement', 'who engaged yesterday', 'morning digest' or 'warm leads', or when a scheduled task runs it."
---

# /daily-engagement

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "daily-engagement"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo plugin and sign in, then retry.
