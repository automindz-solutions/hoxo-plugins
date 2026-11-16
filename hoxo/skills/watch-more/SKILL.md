---
name: watch-more
description: "Find more people for Hoxo to watch, in rounds the member approves. Reads the ICP and the people already watched, proposes candidates five at a time with the reason for each, previews the add, and adds only the ones the member says yes to. Hoxo then checks their posts every Monday and puts the ones worth a comment in Content, Comment on. Use when the user says /watch-more, 'add more people to watch', 'find people to watch', 'grow my watch list', 'who should I be watching', 'fill my Dream 100', or wants more posts to comment on."
---

# /watch-more

Hoxo serves this skill's instructions live so they are always current.

1. Call `get_skill_instructions` on the Hoxo connector with `skill: "watch-more"`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo plugin and sign in, then retry.
