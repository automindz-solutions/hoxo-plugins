---
name: tbr-sync-pipeline
description: "Optional. Checks your LinkedIn messages in your Claude browser for the leads in your Hoxo pipeline, sees who you messaged and who replied, and updates each lead's stage and follow-up date so nobody is chased twice or forgotten. Read-only on LinkedIn, it never sends anything. Use when the user says /tbr-sync-pipeline, 'sync my pipeline', 'update my pipeline from LinkedIn', 'who replied', or 'who do I need to follow up with'."
---

# /tbr-sync-pipeline

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "tbr-sync-pipeline"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo plugin and sign in, then retry.
