---
name: monday-report
description: "Builds the weekly Monday BD Report in Claude: your posts scored on ICP reach, top Atlas creators, your tracked creators, last week's calls from your notetaker, your CRM, warm leads and pipeline, and hiring signals from Hyreflow. Publishes it as an artifact with this week's 20:10:5 actions and a Start here menu, and saves a copy to the Reports tab in Hoxo. Use when the user says /monday-report, 'run my standup', 'monday report', 'weekly report' or 'weekly standup', or when a scheduled task runs it."
---

# /monday-report

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "monday-report"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo plugin and sign in, then retry.
