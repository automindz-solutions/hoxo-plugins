---
name: buildout-icp-profile
description: "Conversational ICP sharpening session, 45 to 60 minutes. Reads the live ICP, takes in real evidence (best clients, placement stories, case studies, call transcripts), turns it into a Hyreflow search spec (who to find, plus the hiring signals that say why now), then calibrates on fresh profiles pulled from Hyreflow in rounds: show five people, get yes / no / why, tighten the search, repeat. Only calls the ICP sharp once five fresh profiles in a row are qualified correctly and confirmed by the member. Saves the ICP with the search spec inside it. Use when the user says /buildout-icp-profile, 'build out my ICP', 'build out my ICP profile', 'sharpen my ICP', 'nail my ICP', 'calibrate my ICP', 'is my ICP still right', or wants to work through their ideal client profile."
---

# /buildout-icp-profile

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "buildout-icp-profile"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo plugin and sign in, then retry.
