---
name: lrb-onboarding
description: "For the Hoxo Bootcamp plan. LinkedIn Revenue Bootcamp client onboarding assistant. Walks new Bootcamp clients through setting up their Voice Vault by asking questions conversationally, then builds the Voice Vault and saves their writing samples in their Hoxo account. Use when a Bootcamp client says /lrb-onboarding, 'Bootcamp onboarding', 'start the bootcamp', 'LRB onboarding', 'fill in my Bootcamp Voice Vault', 'set up my Voice Vault for the Bootcamp', 'get started with the Bootcamp', or asks what they need to do before Week 1 of the Bootcamp. On Hoxo Boardroom, setup and Voice Vault requests belong to hoxo-system-setup and voice-vault, not here."
---

# /lrb-onboarding

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "lrb-onboarding"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo Bootcamp plugin and sign in, then retry.
