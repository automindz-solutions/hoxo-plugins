---
name: brand-skill-builder
description: "Build a Claude Design-ready brand skill from just a website URL (and optionally a brand book). Use whenever someone wants to 'create a brand skill', 'set up my brand', 'build a design system from my website', 'make my brand into a Claude Design skill', 'turn our site into a design system', or any equivalent. Trigger especially when a non-technical user wants to give Claude Design something to work from but has no website code or proper design tokens. The output is a packaged .skill file with the same folder structure as the reference Hoxo design system skill (SKILL.md, seven reference markdowns for colours, typography, logo, layouts, motifs, voice and design tokens, and an assets/ folder with the logo and any extracted brand assets). Needs a client that can run code (Python with Pillow) and Claude in Chrome for full fidelity."
---

# Brand Skill Builder

Take a website URL - and, optionally, a brand book or brand-toolkit document - and produce a packaged `.skill` file that the user can upload into Claude Design as their design system.

The output mirrors the reference `Hoxo-Design-System-Skill` produced by hand: `SKILL.md`, `references/{colors,typography,logo,layouts,motifs,voice,design-tokens}.md`, and `assets/` with the logo and motif art. Same shape, generated automatically.

## Audience

Most users running this skill aren't designers or developers. They have a website. Maybe they have a brand book PDF somewhere. They want a design system in Claude Design but Claude Design only accepts website code, which is too technical. This skill bridges that gap.

## The whole workflow at a glance

1. **Ask one question** - the website URL (mandatory) and a drag-drop slot for a brand book (optional).
2. **Detect tools** - Chrome connected? Use it. Not connected? Fall back to `web_fetch` and warn the user about reduced fidelity.
3. **Crawl 3–5 pages** - home + an "about/team" page + a couple of product/service/case-study pages.
4. **Extract** - colours from screenshots, typography from CSS, logo and motif assets from page images, voice samples from page copy, layout patterns from screenshots.
5. **Read brand book if provided** - bias all extraction toward what the brand book explicitly says. Brand book wins ties.
6. **Generate** - fill the seven reference templates, confidence-flagging which sections came from explicit sources vs. inference.
7. **Package** - call the skill-creator's `package_skill.py` to produce `<brand-name>.skill`.
8. **Show a one-screen brand card** - logo, three swatches, typeface, one sample heading and tagline rendered in the brand. Ask "Does this look right?"
9. **Fix and re-package** any quick corrections.
10. **Deliver** - hand over the `.skill` + a single short next-step: *"Upload this into Claude Design as your design system. If you ever rebrand, run this again."*

Don't pad the user with status updates between these steps. Keep it quiet, with one progress line per major phase.

## Step 1 - Ask for inputs

Ask one question in chat (use a question tool only if you have one). Keep the language plain:

> "What's the website you'd like to turn into a brand skill? Paste the URL. If you have a brand book or style guide, drop it in too (optional)."

If a URL was already mentioned in the conversation, offer it as the default: "Use the one you shared earlier?"

If the user shares an upload at the same time (a brand book PDF, a brand toolkit pptx, a docx style guide), accept it and treat it as an explicit-rules source. If they don't, that's fine - proceed without.

Do NOT ask follow-up questions about what the user wants extracted, what design-system tool they're using, what colour formats they want, or whether they want CSS or Tailwind tokens. Generate everything - the templates already cover all formats.

## Step 2 - Tool detection

Run these checks silently:

1. `mcp__Claude_in_Chrome__list_connected_browsers` - if it returns a browser, that's the primary path.
2. If no Chrome, attempt `web_fetch` on the homepage URL. If that succeeds, use it.
3. If neither works, surface a single plain-English ask: *"I need to look at your site to do this. Can you open it in Chrome and try again?"* Then stop.

Tell the user once which path you're using ("Looking at your site through Chrome...") - no more.

## Step 3 - Crawl pages

Build a small page list from the homepage:

- The homepage itself
- An "About", "Team", "Story", or equivalent page (look for these in the navigation)
- A primary product/service page
- A case-study or testimonial page if one exists
- A "Branding" or "Style" page if one exists (rare, but gold when it does)

Aim for 3–5 pages total. More than five wastes time without improving output.

For each page, capture:

- **Screenshot** of the full page (for colour extraction and layout/motif inference). Save under `<workspace>/captures/<page-slug>.png`.
- **Rendered text** of the page (for voice samples). Save under `<workspace>/captures/<page-slug>.txt`.
- **Computed CSS** from the homepage and one inner page - pull `font-family`, `font-weight`, `font-size`, `color`, `background-color`, `border-radius` for the body, headings (h1–h3), buttons, and links. Save under `<workspace>/captures/computed-css.json`.
- **HTML** of the homepage so we can find image, SVG, and `background-image` URLs. Save under `<workspace>/captures/home.html`.

If using Chrome:
- `mcp__Claude_in_Chrome__navigate` to the URL
- `mcp__Claude_in_Chrome__get_page_text` for text
- `mcp__Claude_in_Chrome__javascript_tool` to read computed styles and dump the HTML
- For screenshots, use `mcp__Claude_in_Chrome__computer` to take one (or `gif_creator` for above-fold + scroll if the page is long)

If using `web_fetch`:
- HTML and text only; no screenshots, no computed CSS. Note this limitation in the output's confidence flags.

## Step 4 - Extraction

Read `references/extraction-playbook.md` if you need detailed how-tos. The high-level rules:

### Colours
1. Run `scripts/extract_dominant_colors.py <screenshot>` for each screenshot. The script returns the top 8 colours by pixel coverage, with hex and rough percentage.
2. Cross-reference with the computed CSS - any colour that appears as a CSS custom property or in a `--brand-*` / `--primary-*` named variable is almost certainly a brand colour. Trust those names.
3. Identify roles by frequency and context:
   - Most-frequent saturated colour → primary brand colour
   - Most-frequent dark, low-saturation colour → text default
   - Most-frequent light colour with high coverage → surface default
   - Any other distinct saturated colour at >5% coverage → secondary or accent
4. Filter out near-pure-white and near-pure-black unless they appear in computed CSS for actual text/surface roles.

### Typography
1. From computed CSS, take the `font-family` from `body`, `h1`, and `h2`. The body font is the brand's default typeface. If headings use a different family, that's the display typeface; otherwise it's the same as body (most common case).
2. Capture font sizes for body, h1, h2, h3 and convert proportionally to the type scale used in the template (display/h1/h2/h3/body-lg/body/small).
3. Capture `font-weight` to detect whether the brand leans regular, medium, or bold.
4. Capture `letter-spacing` on uppercase elements to set the eyebrow tracking.

### Logo + assets

**Identifying assets to extract.** From the homepage HTML, list every `<img>` src, every inline `<svg>`, and every `background-image` URL. Filter for images that:
- Appear in the header or near the top of the page (most likely the logo)
- Are small (< 100KB) and have transparent backgrounds (icons, motifs)
- Repeat across multiple pages (logo, hero motifs)

The most-repeated small image with a transparent background is the logo. Skip large photographs (likely licensed stock) and obviously third-party assets (Stripe, social platform logos, trust-badge icons).

**Downloading the assets - this is the tricky bit.** The bash workspace can't fetch from the user's domain directly (network allowlist), and Chrome's `javascript_tool` truncates responses at ~1KB. Naïve `fetch().then(r=>r.text())` doesn't work for files over 1KB; raw base64 trips Chrome's "base64 encoded data" safety filter and gets blocked. Use the **chunked-hex protocol** instead:

1. **Prep the asset on the page** - run this JS once per asset:
   ```javascript
   (async()=>{
     const r=await fetch(URL);
     const ab=await r.arrayBuffer();
     const bytes=new Uint8Array(ab);
     let hex='';
     for(let i=0;i<bytes.length;i++){const h=bytes[i].toString(16);hex+=h.length<2?'0'+h:h}
     const spaced=hex.match(/.{1,32}/g).join(' ');
     window.__assetChunks=[];
     for(let i=0;i<Math.ceil(spaced.length/1000);i++)
       window.__assetChunks.push(spaced.substring(i*1000,(i+1)*1000));
     return JSON.stringify({bytes:bytes.length,num_chunks:window.__assetChunks.length})
   })()
   ```
   The "spaces every 32 hex chars" matters - it breaks the alphanumeric pattern that Chrome's safety filter treats as base64. Without the spaces, every chunk read returns `[BLOCKED: Base64 encoded data]`.

2. **Read all chunks in one round trip** using `browser_batch`. For each chunk index, call `window.__assetChunks[i]`. The `num_chunks` value from step 1 tells you how many to issue.

3. **Save the chunks to a workspace text file.** Concatenate the responses (whitespace doesn't matter) and write to e.g. `<workspace>/captures/<asset-slug>-chunks.txt`.

4. **Decode** with the bundled script:
   ```bash
   python scripts/decode_asset_chunks.py captures/<asset-slug>-chunks.txt assets/<asset-name>.svg
   ```
   The script strips whitespace, filters non-hex characters defensively, and writes the binary.

5. **Validate** the asset is structurally sensible - for SVG, parse it as XML and confirm the root tag and any `fill` colours match what you saw on the page; for PNG, confirm the file starts with `\x89PNG`. If the file is malformed, the chunks were transcribed wrong - re-read them.

Save extracted assets as `assets/logo.svg`, `assets/logo-icon.svg`, `assets/motif-<descriptive>.svg`, etc. Prefer SVG over PNG when the source was vector - vector assets travel better through Claude Design.

**Falling back when an asset is over ~80KB.** If `num_chunks` exceeds about 100, doing one read per chunk gets slow even via `browser_batch`. In that case, render the SVG to a smaller PNG via `<img>` + canvas first (target ~320px wide), then chunk-extract the PNG dataURL - typically 5–15KB regardless of source SVG complexity. Document this fallback as a workflow finding if you use it.

### Voice samples
1. From the rendered text of each page, extract:
   - The hero/H1 headline
   - 2–3 supporting subheads
   - One paragraph of body copy
   - All CTAs (button text)
2. Look for taglines, mission statements, and recurring phrases.

### Layouts and motifs (inferred)
1. Look at the screenshots and describe what you see:
   - Are corners rounded? (look at images, buttons, cards)
   - Are buttons pill-shaped? Square? Outlined? Filled?
   - Is there a recurring shape (speech bubble, blob, arrow, custom illustration)?
   - Is there a decorative motif (squiggles, dots, sticker-style illustrations, photo cut-outs)?
   - What's the typical page composition? Hero with image right, text left? Centred? Split?
2. Express what you see as rules: "Buttons are pill-shaped (border-radius: 9999px)", "Cards use 16px corner radius", "There is a recurring [shape] used on hero sections."
3. Mark these as **inferred** in the output.

### Brand book input (when provided)
1. Read the brand book end-to-end before generating any reference files.
2. Anywhere the brand book makes an explicit rule (colour value, typeface name, layout instruction, do/don't, voice guideline), use that verbatim and mark it **explicit**.
3. Anywhere the brand book contradicts what we extracted from the website, the brand book wins. Note the conflict in the relevant reference file.
4. Pull the colour palette from the brand book's stated palette, not from screenshot extraction, when both exist.

## Step 5 - Generate the reference files

For each of the seven reference files, read its template from `templates/<name>.md.tpl`, fill in the placeholders, and write to `<workspace>/<brand-slug>/references/<name>.md`. Conventions:

- Placeholders look like `{{primary_color_hex}}`, `{{typeface_name}}`, etc.
- Each section has a confidence flag at the top: **Source: extracted from `<url>` on `<date>`** *or* **Source: extracted from `<url>` + brand book `<filename>` on `<date>`**.
- Inline confidence: tag any rule that's inferred (not stated explicitly in source) with `_(inferred)_` at the end of the line. This lets a designer or the user see at a glance what's a guess.

Then fill the top-level `<workspace>/<brand-slug>/SKILL.md` from `templates/SKILL.md.tpl`. The top-level SKILL.md follows the same structure as the Hoxo example - quick-reference summary at the top, pointers into the references below it.

Persist the source URL as a comment in `SKILL.md` so a future re-run can default to the same URL.

### ⚠️ Spec-writing rules to avoid output bugs

When you build the `spec.json` that feeds `scripts/build_skill.py`, follow these conventions or you'll produce broken output files:

- **Font names with spaces:** wrap them in **single quotes**, never double quotes, in the `font_fallback_stack` field. Example: `'DM Sans', system-ui, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif`. Single quotes are valid in both CSS and (when the value is itself wrapped in JSON's double quotes) JSON. Double quotes inside double quotes break the JSON.
- **One value per key, as plain text.** Every `{{placeholder}}` in the templates is a key in `spec.json`. Multi-line values (tables, lists) are strings with `\n` newlines. A key you could not extract is left out: `build_skill.py` fills it with `_(not extracted)_`, which is honest; an invented value is not.
- **Assets** are listed as `"assets": [{"src": "<workspace>/assets/logo.svg", "filename": "logo.svg"}]`. Only list files you actually decoded and validated in Step 4.

## Step 6 - Package

Run the bundled builder:

```bash
python scripts/build_skill.py <workspace>/spec.json templates <workspace>/out
```

It fills every template, bundles the assets, and calls the skill-creator's `package_skill.py` to produce `<workspace>/out/<brand-slug>-brand.skill`. It looks for skill-creator at `$SKILL_CREATOR`, else `~/.claude/skills/skill-creator`, else the copy the skill-creator plugin keeps under `~/.claude/plugins/cache/*/skill-creator/*/skills/skill-creator`. If it cannot find it, it says so and prints the manual command; run that, or deliver the unpackaged folder and say it still needs packaging.

## Step 7 - Show a one-screen brand card

Render a single small card in chat or as an image: the logo, the primary, secondary and accent swatches with their hex values, the typeface name, and one sample heading plus the tagline set in the brand. Ask one question: *"Does this look right?"*

## Step 8 - Fix and re-package

Apply any quick corrections the user gives (a wrong colour role, the wrong logo, a typeface name) to `spec.json`, then re-run Step 6. Do not re-crawl the site for a correction the user has just told you.

## Step 9 - Deliver

Hand over the `.skill` file (attach it, or give its path) with one short next step:

*"Upload this into Claude Design as your design system. If you ever rebrand, run this again."*

Nothing else: no recap of the extraction, no list of what was inferred. The confidence flags are inside the files for anyone who wants them.
