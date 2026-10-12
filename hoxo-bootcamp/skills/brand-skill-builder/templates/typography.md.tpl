# Typography

**Source:** {{source_summary}}

## The typeface

**{{typeface_name}}** is the primary {{brand_name}} typeface, used for {{typeface_usage}}. Available weights: {{typeface_weights}}.

{{secondary_typeface_clause}}

When {{typeface_name}} can't be loaded, fall back through this stack:

```
{{font_fallback_stack}}
```

Don't substitute a different sans/serif unless explicitly authorised — the typeface is part of the brand's visual feel.

## Type scale

| Role | Size | Weight | Line-height | Notes |
|---|---|---|---|---|
| Display H1 | {{display_size_px}}px | {{display_weight}} | {{display_leading}} | {{display_notes}} |
| H2 | {{h2_size_px}}px | {{h2_weight}} | {{h2_leading}} | |
| H3 | {{h3_size_px}}px | {{h3_weight}} | {{h3_leading}} | |
| Body large | {{body_lg_size_px}}px | {{body_weight}} | {{body_leading}} | |
| Body | {{body_size_px}}px | {{body_weight}} | {{body_leading}} | Default reading size |
| Small | {{small_size_px}}px | {{body_weight}} | 1.5 | Captions, footers |
| Eyebrow / overline | {{eyebrow_size_px}}px | {{eyebrow_weight}} | 1.4 | ALL CAPS, letter-spacing {{eyebrow_tracking}} |

Sizes were captured from computed CSS on {{source_url}} _(extracted)_.

## Casing rules _(inferred)_

- **Section overlines / labels:** ALL CAPS
- **Headings:** {{heading_case}}
- **Body copy:** sentence case
- **Buttons / CTAs:** {{cta_case}}

## Links

- **Inline links:** {{link_treatment}}
- **CTA buttons:** {{cta_treatment}}

## Spacing rules _(inferred from observed line-heights)_

- Body line-height: {{body_leading}}
- Heading line-height: {{display_leading}}
- Paragraph spacing: {{paragraph_spacing_px}}px between blocks

## Captured samples

{{typography_samples_block}}
