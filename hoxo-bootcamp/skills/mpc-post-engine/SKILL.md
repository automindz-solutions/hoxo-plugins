---
name: mpc-post-engine
description: "LinkedIn MPC (candidate shop window) post generator for agency recruiters on the Hoxo LinkedIn Revenue Bootcamp. Takes a candidate's CV (plus optional call notes or screening transcript) and writes ONE ready-to-post LinkedIn post that sells the candidate directly to their ideal buyer, in a direct-hard-pitch style (offer in the first line, 3-second readability). The first run saves the recruiter's preferences (niche, location rules, stage exclusions, sign-off); after that they only paste the candidate. MANDATORY TRIGGERS: 'MPC post', 'mpc', 'Bootcamp candidate shop window post', 'CV-anonymised shop window post', 'write a post about/for my candidate', 'post my candidate', 'market my candidate', 'sell my candidate on LinkedIn', 'LinkedIn post for this candidate', 'turn this CV into a post', 'put this candidate out there', or a CV with a request for a post promoting the candidate. Not for a sector-authority piece with no candidate (create-content on Boardroom)."
---

# /mpc-post-engine

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "mpc-post-engine"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo Bootcamp plugin and sign in, then retry.
