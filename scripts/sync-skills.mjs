#!/usr/bin/env node
/**
 * Generate the skills of both plugins (hoxo, hoxo-bootcamp) from the canonical skill-pack.
 *
 * Normal skills become THIN STUBS: the skill's frontmatter (name + description, so it
 * stays discoverable / triggerable) plus a body that calls `get_skill_instructions` on the
 * Hoxo connector. The real body lives server-side (the MCP serves it), so skill logic
 * updates instantly on deploy — no plugin update, no marketplace cache/pinning problem.
 *
 * Exception: a skill whose pack dir holds anything besides SKILL.md (brand-skill-builder:
 * it runs local Python the MCP cannot serve) is copied whole.
 *
 * Run before publishing: node scripts/sync-skills.mjs  (from the marketplace repo root)
 */
import {
  readdirSync, mkdirSync, rmSync, readFileSync, writeFileSync, existsSync, cpSync,
} from "fs";
import { join, dirname, basename } from "path";
import { fileURLToPath } from "url";

const __dirname = dirname(fileURLToPath(import.meta.url));
// The pack lives in the hoxo repo, checked out as a sibling of this repo. Override with
// SKILL_PACK=/path/to/hoxo-boardroom-skill-pack to generate from a branch or other layout.
const pack = process.env.SKILL_PACK ?? join(__dirname, "../../hoxo/hoxo-boardroom-skill-pack");
const src = join(pack, "skills");

if (!existsSync(src)) {
  console.error(`Skill pack not found at ${src}\nSet SKILL_PACK to the hoxo-boardroom-skill-pack directory.`);
  process.exit(1);
}

const all = readdirSync(src, { withFileTypes: true })
  .filter((d) => d.isDirectory() && !d.name.startsWith("."))
  .map((d) => d.name);

// Bootcamp gets every pack skill not in the MCP's BOARDROOM_ONLY_PROMPTS
// (mcp-server/src/plan.ts, next to the pack), brand-skill-builder included: read
// from the source rather than copied, so a new skill can never be left out.
const planTs = join(pack, "../mcp-server/src/plan.ts");
const planSrc = existsSync(planTs) ? readFileSync(planTs, "utf8") : "";
const denyStart = planSrc.indexOf("const BOARDROOM_ONLY_PROMPTS");
if (denyStart === -1) {
  console.error(`BOARDROOM_ONLY_PROMPTS not found in ${planTs}`);
  process.exit(1);
}
const denyOpen = planSrc.indexOf("[", denyStart);
const denyList = planSrc.slice(denyOpen, planSrc.indexOf("]", denyOpen));
const boardroomOnly = new Set([...denyList.matchAll(/"([a-z0-9-]+)"/g)].map((m) => m[1]));
const BOOTCAMP_SKILLS = all.filter((s) => !boardroomOnly.has(s));

const TARGETS = { hoxo: all, "hoxo-bootcamp": BOOTCAMP_SKILLS };
// What a stub tells a user with no connector to install: this plugin, never the other one.
const DISPLAY = { hoxo: "Hoxo", "hoxo-bootcamp": "Hoxo Bootcamp" };

// Finder's .DS_Store and Python's __pycache__ are not part of a skill: they must not
// make a stub skill count as "copied whole", nor be copied with one that is.
const shipped = (f) => f !== "__pycache__" && !f.startsWith(".");

function stubBody(name, plugin) {
  return `# /${name}

Hoxo serves this skill's instructions live so they are always current.

1. Call \`get_skill_instructions\` on the Hoxo connector with \`skill: "${name}"\`.
2. Follow the returned instructions exactly.

If the Hoxo connector is not available, tell the user to install the ${DISPLAY[plugin]} plugin and sign in, then retry.
`;
}

for (const [plugin, skills] of Object.entries(TARGETS)) {
  const dest = join(__dirname, "..", plugin, "skills");
  rmSync(dest, { recursive: true, force: true });
  mkdirSync(dest, { recursive: true });
  let n = 0;
  let whole = 0;
  for (const name of skills) {
    const dir = join(src, name);
    const raw = readFileSync(join(dir, "SKILL.md"), "utf8");
    if (readdirSync(dir).some((f) => f !== "SKILL.md" && shipped(f))) {
      cpSync(dir, join(dest, name), {
        recursive: true,
        filter: (p) => shipped(basename(p)),
      });
      whole++;
      n++;
      continue;
    }
    const fm = (raw.match(/^---\r?\n[\s\S]*?\r?\n---/) || [""])[0];
    if (!fm) {
      console.warn(`! ${name}: no frontmatter, skipped`);
      continue;
    }
    mkdirSync(join(dest, name), { recursive: true });
    writeFileSync(join(dest, name, "SKILL.md"), `${fm}\n\n${stubBody(name, plugin)}`);
    n++;
  }
  console.log(`${plugin}: ${n} skill(s) (${whole} copied whole)`);
}
