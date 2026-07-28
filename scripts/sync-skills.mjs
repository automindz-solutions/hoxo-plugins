#!/usr/bin/env node
/**
 * Generate THIN STUB skills for the hoxo plugin from the canonical skill-pack.
 *
 * Each stub keeps the skill's frontmatter (name + description, so it stays
 * discoverable / triggerable) but its body just calls `get_skill_instructions`
 * on the Hoxo connector. The real skill body lives server-side (the MCP serves
 * it), so skill logic updates instantly on deploy — no plugin update, no
 * marketplace cache/pinning problem.
 *
 * Run before publishing: node scripts/sync-skills.mjs  (from the marketplace repo root)
 */
import { readdirSync, mkdirSync, rmSync, readFileSync, writeFileSync, existsSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
// The pack lives inside the internal-workflows monorepo, checked out as a sibling of
// this repo. Override with SKILL_PACK=/path/to/hoxo-boardroom-skill-pack to generate
// from a branch or a different layout.
const pack =
  process.env.SKILL_PACK ??
  join(__dirname, "../../internal-workflows/clients/hoxo/hoxo-boardroom-skill-pack");
const src = join(pack, "skills");
const dest = join(__dirname, "../hoxo/skills");

if (!existsSync(src)) {
  console.error(`Skill pack not found at ${src}\nSet SKILL_PACK to the hoxo-boardroom-skill-pack directory.`);
  process.exit(1);
}

rmSync(dest, { recursive: true, force: true });
mkdirSync(dest, { recursive: true });

function stubBody(name) {
  return `# /${name}

Hoxo serves this skill's instructions live so they are always current.

1. Call \`get_skill_instructions\` on the Hoxo connector with \`skill: "${name}"\`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the Hoxo plugin and sign in, then retry.
`;
}

let n = 0;
for (const d of readdirSync(src, { withFileTypes: true })) {
  if (!d.isDirectory() || d.name.startsWith(".")) continue;
  const raw = readFileSync(join(src, d.name, "SKILL.md"), "utf8");
  const fm = (raw.match(/^---\r?\n[\s\S]*?\r?\n---/) || [""])[0];
  if (!fm) {
    console.warn(`! ${d.name}: no frontmatter, skipped`);
    continue;
  }
  mkdirSync(join(dest, d.name), { recursive: true });
  writeFileSync(join(dest, d.name, "SKILL.md"), `${fm}\n\n${stubBody(d.name)}`);
  n++;
}

console.log(`Generated ${n} stub skill(s) → hoxo/skills/`);
