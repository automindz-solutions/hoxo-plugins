---
name: lrb-job-post
description: "LinkedIn job post writer for the Hoxo LinkedIn Revenue Bootcamp. Turns information about a live vacancy (a full job description, a loose description of the role, a call transcript, job notes or a summary) into a story-driven LinkedIn post advertising the role, not a transactional job ad. Use when the user says 'write a LinkedIn job post', 'job post for this role', 'turn this job into a post', 'write a post for this vacancy', 'I want to advertise this job on LinkedIn', or pastes a job description or notes and wants a LinkedIn post advertising the role. Not for candidate outreach, profile work, or general content ideas."
---

# /lrb-job-post

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "lrb-job-post"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo Bootcamp plugin and sign in, then retry.
