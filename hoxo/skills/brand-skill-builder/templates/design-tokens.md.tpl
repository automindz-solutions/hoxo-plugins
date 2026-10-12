# Design tokens

**Source:** {{source_summary}}

Copy-paste–ready tokens for **Claude Design**, Figma Variables, Tailwind, and CSS. Names use the `{{brand_slug}}-*` prefix to avoid colliding with the host design system.

## Claude Design / Figma Variables (JSON)

```json
{
  "color": {
    "{{brand_slug}}-primary":     { "value": "{{primary_color_hex}}", "type": "color" },
    "{{brand_slug}}-secondary":   { "value": "{{secondary_color_hex}}", "type": "color" },
    "{{brand_slug}}-accent":      { "value": "{{accent_color_hex}}", "type": "color" },
    "{{brand_slug}}-surface":     { "value": "{{surface_color_hex}}", "type": "color" },
    "{{brand_slug}}-surface-alt": { "value": "{{surface_alt_color_hex}}", "type": "color" },
    "{{brand_slug}}-text":        { "value": "{{text_color_hex}}", "type": "color" },
    "{{brand_slug}}-text-on-dark":{ "value": "{{text_on_dark_color_hex}}", "type": "color" }
  },
  "font": {
    "{{brand_slug}}-font-family":          { "value": "{{font_fallback_stack}}", "type": "fontFamilies" },
    "{{brand_slug}}-font-weight-regular":  { "value": 400, "type": "fontWeights" },
    "{{brand_slug}}-font-weight-medium":   { "value": 500, "type": "fontWeights" },
    "{{brand_slug}}-font-weight-bold":     { "value": 700, "type": "fontWeights" }
  },
  "size": {
    "{{brand_slug}}-size-display": { "value": "{{display_size_px}}px", "type": "fontSizes" },
    "{{brand_slug}}-size-h1":      { "value": "{{h1_size_px}}px", "type": "fontSizes" },
    "{{brand_slug}}-size-h2":      { "value": "{{h2_size_px}}px", "type": "fontSizes" },
    "{{brand_slug}}-size-h3":      { "value": "{{h3_size_px}}px", "type": "fontSizes" },
    "{{brand_slug}}-size-body-lg": { "value": "{{body_lg_size_px}}px", "type": "fontSizes" },
    "{{brand_slug}}-size-body":    { "value": "{{body_size_px}}px", "type": "fontSizes" },
    "{{brand_slug}}-size-small":   { "value": "{{small_size_px}}px", "type": "fontSizes" },
    "{{brand_slug}}-size-eyebrow": { "value": "{{eyebrow_size_px}}px", "type": "fontSizes" }
  },
  "radius": {
    "{{brand_slug}}-radius-sm":   { "value": "{{radius_sm_px}}px", "type": "borderRadius" },
    "{{brand_slug}}-radius-md":   { "value": "{{radius_md_px}}px", "type": "borderRadius" },
    "{{brand_slug}}-radius-lg":   { "value": "{{radius_lg_px}}px", "type": "borderRadius" },
    "{{brand_slug}}-radius-pill": { "value": "9999px", "type": "borderRadius" }
  }
}
```

## CSS custom properties

```css
:root {
  /* Brand colours */
  --{{brand_slug}}-primary:     {{primary_color_hex}};
  --{{brand_slug}}-secondary:   {{secondary_color_hex}};
  --{{brand_slug}}-accent:      {{accent_color_hex}};
  --{{brand_slug}}-surface:     {{surface_color_hex}};
  --{{brand_slug}}-surface-alt: {{surface_alt_color_hex}};
  --{{brand_slug}}-text:        {{text_color_hex}};
  --{{brand_slug}}-text-on-dark:{{text_on_dark_color_hex}};

  /* Typography */
  --{{brand_slug}}-font-family: {{font_fallback_stack}};

  --{{brand_slug}}-size-display: clamp({{display_size_min_px}}px, 6vw, {{display_size_px}}px);
  --{{brand_slug}}-size-h1:      {{h1_size_px}}px;
  --{{brand_slug}}-size-h2:      {{h2_size_px}}px;
  --{{brand_slug}}-size-h3:      {{h3_size_px}}px;
  --{{brand_slug}}-size-body-lg: {{body_lg_size_px}}px;
  --{{brand_slug}}-size-body:    {{body_size_px}}px;
  --{{brand_slug}}-size-small:   {{small_size_px}}px;
  --{{brand_slug}}-size-eyebrow: {{eyebrow_size_px}}px;

  --{{brand_slug}}-leading-display: {{display_leading}};
  --{{brand_slug}}-leading-heading: {{display_leading}};
  --{{brand_slug}}-leading-body:    {{body_leading}};

  --{{brand_slug}}-tracking-eyebrow: {{eyebrow_tracking}};

  /* Radius */
  --{{brand_slug}}-radius-sm:   {{radius_sm_px}}px;
  --{{brand_slug}}-radius-md:   {{radius_md_px}}px;
  --{{brand_slug}}-radius-lg:   {{radius_lg_px}}px;
  --{{brand_slug}}-radius-pill: 9999px;
}

html {
  background: var(--{{brand_slug}}-surface);
  color: var(--{{brand_slug}}-text);
  font-family: var(--{{brand_slug}}-font-family);
  font-size: var(--{{brand_slug}}-size-body);
  line-height: var(--{{brand_slug}}-leading-body);
}
```

## Tailwind config snippet

```js
module.exports = {
  theme: {
    extend: {
      colors: {
        '{{brand_slug}}-primary':     '{{primary_color_hex}}',
        '{{brand_slug}}-secondary':   '{{secondary_color_hex}}',
        '{{brand_slug}}-accent':      '{{accent_color_hex}}',
        '{{brand_slug}}-surface':     '{{surface_color_hex}}',
        '{{brand_slug}}-surface-alt': '{{surface_alt_color_hex}}',
        '{{brand_slug}}-text':        '{{text_color_hex}}',
      },
      fontFamily: {
        sans: ['{{typeface_name}}', 'system-ui', '-apple-system', 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'],
      },
      fontSize: {
        '{{brand_slug}}-display': ['{{display_size_px}}px', { lineHeight: '{{display_leading}}' }],
        '{{brand_slug}}-h1':      ['{{h1_size_px}}px', { lineHeight: '{{display_leading}}' }],
        '{{brand_slug}}-h2':      ['{{h2_size_px}}px', { lineHeight: '{{display_leading}}' }],
        '{{brand_slug}}-h3':      ['{{h3_size_px}}px', { lineHeight: '1.2' }],
        '{{brand_slug}}-body-lg': ['{{body_lg_size_px}}px', { lineHeight: '{{body_leading}}' }],
        '{{brand_slug}}-body':    ['{{body_size_px}}px', { lineHeight: '{{body_leading}}' }],
        '{{brand_slug}}-small':   ['{{small_size_px}}px', { lineHeight: '1.5' }],
      },
      borderRadius: {
        '{{brand_slug}}-sm': '{{radius_sm_px}}px',
        '{{brand_slug}}-md': '{{radius_md_px}}px',
        '{{brand_slug}}-lg': '{{radius_lg_px}}px',
      },
    },
  },
};
```

## Style Dictionary input (`tokens.json`)

```json
{
  "color": {
    "brand": {
      "primary":   { "value": "{{primary_color_hex}}" },
      "secondary": { "value": "{{secondary_color_hex}}" },
      "accent":    { "value": "{{accent_color_hex}}" },
      "surface":   { "value": "{{surface_color_hex}}" },
      "text":      { "value": "{{text_color_hex}}" }
    }
  },
  "size": {
    "font": {
      "display": { "value": "{{display_size_px}}" },
      "h1":      { "value": "{{h1_size_px}}" },
      "h2":      { "value": "{{h2_size_px}}" },
      "h3":      { "value": "{{h3_size_px}}" },
      "body-lg": { "value": "{{body_lg_size_px}}" },
      "body":    { "value": "{{body_size_px}}" },
      "small":   { "value": "{{small_size_px}}" }
    },
    "radius": {
      "sm":   { "value": "{{radius_sm_px}}" },
      "md":   { "value": "{{radius_md_px}}" },
      "lg":   { "value": "{{radius_lg_px}}" },
      "pill": { "value": "9999" }
    }
  }
}
```

## Mapping to Claude Design

When wiring this token set into Claude Design:

1. **Create a colour collection called "{{brand_name}}"** and import the colour tokens from the JSON block above.
2. **Add the font family and the size tokens** as typography variables, using the same `{{brand_slug}}-*` names.
3. **Add the radius tokens** as number variables.
4. **Check the primary colour on a button and the body size on a paragraph** before building anything with the set.

If a value above reads `_(not extracted)_`, it was not found on the site or in the brand book. Fill it in by hand rather than guessing.
