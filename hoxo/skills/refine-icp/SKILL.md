---
name: refine-icp
description: "Self-serve ICP pressure-test, built for the Boardroom room — one member, 45 minutes. Reads the live ICP, argues with it (not just collects answers), rewrites it, saves it, then offers to re-qualify the existing network against the new version so the member sees the effect before they leave. Use when the user says /refine-icp, 'refine my ICP', 'pressure-test my ICP', 'my ICP is wrong', or wants to rebuild their ideal customer profile."
---

# /refine-icp

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "refine-icp"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo plugin and sign in, then retry.
