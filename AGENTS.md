# AGENTS

## Purpose

This file defines general authoring rules for working with this Hugo site.
It should describe how to use Hugo in this repository, not how to reproduce any original sample template content.

## Core Hugo Rules

- Organize content as a Hugo page tree.
- A folder with `_index.md` is a section or branch bundle.
- A regular content page can be either:
  - `name.md`
  - `name/_index.md`
- Prefer folder bundles when a page may later need images or attachments.
- Use stable, lowercase, hyphenated slugs for folder and file names.

## Multilingual Rules

- This repository uses paired language files:
  - `*.md` for English
  - `*.vi.md` for Vietnamese
- All `*.vi.md` content must be written in proper Vietnamese with diacritics (dau), not ASCII-only transliteration.
- Keep both language files in the same folder.
- When creating a new page, create both language files together.
- Keep the page purpose, front matter shape, and relative placement aligned across languages.

## Front Matter Conventions

Use front matter consistently so menu ordering and rendering stay predictable.

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

### Field meanings

- `title`: displayed page title
- `date`: creation or publication date
- `weight`: sibling ordering
- `chapter`: keep `false` unless a chapter-style layout is explicitly needed
- `pre`: optional HTML prefix for sidebar numbering

## Content Authoring Rules

- Do not put numbering inside `title`; use `pre` for sidebar numbering.
- Use headings in normal Markdown form.
- Prefer short introductory paragraphs before long sections.
- Store related content in the same bundle when possible.
- If a section should list its child pages, use the `children` shortcode.

Example:

```md
{{% children description="true" /%}}
```

## Static Assets

- Prefer page-bundled assets for page-specific diagrams, screenshots, and attachments.
- Use a folder prefixed with `_` for page-local assets or tooling, such as `_diagrams/` and `_tools/`.
- Treat folders without `index.md`, `_index.md`, or other publishable content files as support folders, not subpages.
- Keep shared global assets such as favicon, fonts, and site-wide images under `static/`.
- For page-bundled images, use page-relative paths in Markdown.

Example:

```md
![Diagram](_diagrams/example-diagram.png)
```

- Keep asset paths stable after publishing to avoid broken links.
- Keep generator scripts near the page they support by placing them in a sibling `_tools/` folder when practical.

## Screenshot Asset Workflow

- Store original AWS Console screenshots in `raw/` as PNG files.
- Treat files in `raw/` as immutable source material for authoring, not publishable site assets.
- For pages built from ClickOps screenshots, create cropped publishable assets inside the related page bundle, typically under `_diagrams/`.
- Prefer WebP for publishable cropped screenshots that are rendered on the website.
- Keep PNG as the working or source format during capture, review, and intermediate editing.
- Use stable, descriptive, lowercase, hyphenated filenames for cropped assets, based on what the crop proves, not only the step number.
- One cropped image should support one main point, or at most two tightly related points.
- Remove irrelevant browser chrome, AWS header area, empty whitespace, and unrelated panels when cropping unless they are required for reader orientation.
- If one screenshot contains multiple important details, split it into multiple focused crops instead of embedding one very large image.
- Keep the same cropped asset usable across English and Vietnamese pages when the visual evidence is identical.
- If a crop needs reproducibility, store its crop specification in a sibling `_tools/` script or manifest rather than relying on manual editing only.

## Image Tooling

- Preferred CLI tools for screenshot workflows in this repository:
  - `magick`, `identify`, `mogrify` from ImageMagick for inspect, crop, resize, and format conversion
  - `tesseract` for OCR-based inspection of screenshot text
  - `cwebp` for WebP encoding
  - `pngquant` and `optipng` for PNG optimization
- Preferred Python packages for scripted image workflows:
  - `Pillow` for deterministic crop and export automation
  - `pytesseract` for OCR integration
  - `PyYAML` when a crop manifest is stored as YAML

## Shortcodes Available

This repository currently includes or supports these shortcodes:

- `notice`
- `children`
- `tabs`
- `tab`
- `ghcontributors`

Example notice:

```md
{{% notice info %}}
Important content goes here.
{{% /notice %}}
```

## Page Creation Workflow

1. Create the English page.
2. Create the matching Vietnamese page in the same folder.
3. Add consistent front matter to both files.
4. Set `weight` and `pre` if menu ordering matters.
5. Add related page-specific assets under `_diagrams/` or another `_`-prefixed support folder if needed.
6. Run Hugo locally and verify both languages.

## AI Drivent Blog Writing from ClickOps Raw Data

- Organize raw data for blog content in a `raw/` folder at the project root.
- Structure:
  ```
  raw/
  ├── {operation_number}/  # e.g., 1/, 2/
  │   ├── {step_letter}/   # e.g., a/, b/
  │   │   ├── *.png        # Screenshot from AWS console
  │   │   ├── req.md       # mean for `request` my question to ChatGPT
  │   │   └── res.md       # mean for `response` the answer or guidance from ChatGPT to my question
  ```
- Workflow:
  # Click Ops with ChatGPT
  - Screenshot AWS console to ask ChatGPT.
  - ChatGPT responds with guidance.
  # Writing blogs
  - Save screenshots and ChatGPT responses to the appropriate raw/ step folder.
  - Read raw/ for context to write blogs, creating page bundles in `content/` with assets in `_diagrams/` or similar.
  - Derive publishable crops from raw PNG screenshots and save the final page assets as focused WebP images in the page bundle.
  - Place each cropped image near the paragraph or step that it explains, instead of stacking long full-screen screenshots before the text.

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

After generating a page with Hugo CLI:

- remove `draft: true` when ready to publish
- add `weight`
- add `pre` only if sidebar numbering is needed
- create the matching `.vi.md` file

## Guardrails

- Keep `AGENTS.md` focused on Hugo usage rules only.
- Do not encode sample content structure, legacy template sections, or project-specific filler content here.
- Update this file when Hugo authoring conventions change.
