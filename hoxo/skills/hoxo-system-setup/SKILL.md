---
name: hoxo-system-setup
description: "Full Hoxo onboarding — run once. Verifies the connector, builds your Voice Vault, and collects podcast docs, all stored in your Hoxo account (no local files) so the other skills have everything they need on any device. Use when the user says /hoxo-system-setup, 'set up my workspace', 'let's get started', or opens Hoxo in Claude for the first time."
---

# /hoxo-system-setup

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "hoxo-system-setup"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo plugin and sign in, then retry.
