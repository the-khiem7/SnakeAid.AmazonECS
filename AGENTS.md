# AGENTS

## Purpose

This file defines the authoring rules for working with this Hugo repository.
Keep it focused on repository conventions, Hugo usage, content structure, and asset workflow.
Do not use this file to preserve sample content or legacy template structure.

## Content Structure

- Organize content as a Hugo page tree.
- A folder with `_index.md` is a section or branch bundle.
- A regular content page can be either:
  - `name.md`
  - `name/_index.md`
- Prefer folder bundles when a page may later need images or attachments.
- Use stable, lowercase, hyphenated names for folders and files.

## Multilingual Content

- This repository uses paired language files in the same folder:
  - `*.md` for English
  - `*.vi.md` for Vietnamese
- Create both language files together for every new page.
- Keep page purpose, front matter shape, and relative placement aligned across both languages.
- All `*.vi.md` files must use proper Vietnamese with diacritics, not ASCII transliteration.

## Front Matter

Use front matter consistently so sidebar order and rendering stay predictable.

### Section page

```md
---
title: "Section Title"
date: 2026-04-22
weight: 1
chapter: false
pre: " <b> 1. </b> "
---
```

### Regular page

```md
---
title: "Page Title"
date: 2026-04-22
weight: 1
chapter: false
pre: " <b> 1.1. </b> "
---
```

### Conventions

- `title`: displayed page title
- `date`: creation or publication date
- `weight`: sibling ordering
- `chapter`: keep `false` unless a chapter-style layout is explicitly needed
- `pre`: optional HTML prefix for sidebar numbering
- Do not place numbering inside `title`; use `pre` instead.

## Writing Rules

- Use normal Markdown headings.
- Prefer a short introductory paragraph before long sections.
- Store related content in the same bundle when possible.
- If a section should list its child pages, use the `children` shortcode.

Example:

```md
{{% children description="true" /%}}
```

## Assets

- Prefer page-bundled assets for page-specific diagrams, screenshots, and attachments.
- Use `_`-prefixed support folders for page-local assets or tooling, such as `_diagrams/` and `_tools/`.
- Treat folders without publishable content files as support folders, not subpages.
- Keep shared global assets such as favicon, fonts, and site-wide images under `static/`.
- For page-bundled images, use page-relative paths in Markdown.
- Keep asset paths stable after publishing to avoid broken links.
- Keep generator scripts near the page they support when practical.

Example:

```md
![Diagram](_diagrams/example-diagram.png)
```

## Screenshot Workflow

- Store original AWS Console screenshots in `raw/` as PNG files.
- Treat `raw/` as immutable source material, not publishable site assets.
- Derive focused publishable images from `raw/` and place them in the related page bundle, typically under `_diagrams/`.
- Keep PNG for capture and intermediate editing.
- Prefer WebP for cropped screenshots served on the website.
- Use stable, descriptive, lowercase, hyphenated filenames based on what the crop proves, not only the step number.
- One cropped image should support one main point, or at most two tightly related points.
- Remove irrelevant browser chrome, AWS header area, empty whitespace, and unrelated panels unless they are needed for orientation.
- If one screenshot contains multiple important details, split it into multiple focused crops instead of embedding one large full-screen image.
- Reuse the same cropped asset across English and Vietnamese pages when the visual evidence is identical.
- If a crop should be reproducible, store its crop specification in a sibling `_tools/` script or manifest.

## Raw ClickOps Material

- Organize raw blog inputs under `raw/` at the project root.
- Structure:

```text
raw/
├── {operation_number}/
│   ├── {step_letter_or_step_number}/
│   │   ├── *.png
│   │   ├── req.md
│   │   └── res.md
```

- Intended meaning:
  - `*.png`: AWS Console screenshots
  - `req.md`: the prompt or question sent to ChatGPT
  - `res.md`: the answer or guidance returned by ChatGPT

### Authoring flow from raw material

1. Save screenshots and ChatGPT context in the appropriate `raw/` step folder.
2. Read `raw/` for factual context before drafting the article.
3. Create the English and Vietnamese page bundle in `content/`.
4. Derive focused cropped screenshots from raw PNG files.
5. Save final publishable crops as WebP in the page bundle.
6. Place each crop near the paragraph or step it explains, instead of stacking long screenshots ahead of the text.

## Image Tooling

- Preferred CLI tools:
  - `magick`, `identify`, `mogrify` from ImageMagick for inspect, crop, resize, and format conversion
  - `tesseract` for OCR-based inspection of screenshot text
  - `cwebp` for WebP encoding
  - `pngquant` and `optipng` for PNG optimization
- Preferred Python packages:
  - `Pillow` for deterministic crop and export automation
  - `pytesseract` for OCR integration
  - `PyYAML` when storing crop manifests as YAML

## Shortcodes

This repository currently includes or supports these shortcodes:

- `notice`
- `children`
- `tabs`
- `tab`
- `ghcontributors`

Example:

```md
{{% notice info %}}
Important content goes here.
{{% /notice %}}
```

## Page Creation Checklist

1. Create the English page.
2. Create the matching Vietnamese page in the same folder.
3. Add consistent front matter to both files.
4. Set `weight` and `pre` if sidebar ordering matters.
5. Add page-specific assets under `_diagrams/` or another `_`-prefixed support folder if needed.
6. Run Hugo locally and verify both languages.

## Hugo Commands

Run locally:

```bash
hugo server -D
```

Build production output:

```bash
hugo
```

Regenerate bundled diagrams:

```bash
python3 tools/build_diagrams.py
```

Create a new page quickly:

```bash
hugo new some-section/some-page/_index.md
```

After generating a page with the Hugo CLI:

- remove `draft: true` when ready to publish
- add `weight`
- add `pre` only if sidebar numbering is needed
- create the matching `.vi.md` file

## Guardrails

- Keep `AGENTS.md` focused on Hugo usage, authoring rules, and repository workflow.
- Do not encode sample content structure, filler content, or legacy template sections here.
- Update this file when repository conventions change.
