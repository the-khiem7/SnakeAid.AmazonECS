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

- Put images and other public assets under `static/`.
- Use root-relative paths in Markdown.

Example:

```md
![Diagram](/images/example/diagram.png)
```

- Keep asset paths stable after publishing to avoid broken links.

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
5. Add related assets under `static/` if needed.
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
