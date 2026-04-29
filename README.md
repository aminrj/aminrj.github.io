# aminrj.com — AI Security Blog & Research

Personal blog and research site for [Amine Raji](https://aminrj.com), an AI/LLM security practitioner with 15+ years across banking, defense, and automotive sectors. CISSP, OWASP Agentic Security contributor, currently at Volvo Cars.

## What's Here

- **Blog posts** on agentic AI security, MCP protocol, prompt injection, threat modeling, and EU AI Act compliance
- **Research notes** and lab documentation
- **Newsletter** signup (weekly AI security intelligence briefing)

## Tech Stack

- [Jekyll](https://jekyllrb.com/) + [Chirpy theme](https://github.com/cotes2020/jekyll-theme-chirpy) v7
- Ruby 3.3, Bundler for dependency management
- Goatcounter for analytics (configured in `_includes/custom-head.html`)
- Plausible analytics domain: `aminrj.com`

## Running Locally

```bash
# Install dependencies
bundle install

# Start the dev server with live reload
bundle exec jekyll serve --livereload

# Build for production
bundle exec jekyll build
```

## Writing Posts

Posts live in `_posts/` and use Jekyll's date-based naming convention: `YYYY-MM-DD-slug.md`.

Front matter fields:

```yaml
---
title: "Post Title"
date: YYYY-MM-DD
uuid: YYYYMMDD0000          # unique identifier for the post
draft: true                 # set to false when ready to publish
status: draft               # internal status (draft | review | published)
content-type: article       # article | lab | note
target-audience: advanced   # beginner | intermediate | advanced
categories: [AI Security, Agentic AI]
tags: [MCP, Prompt Injection, OWASP]
description: "Short description for SEO meta tags"
image:
  path: /assets/media/path/to/image.png   # optional social preview image
mermaid: true               # include if the post uses mermaid diagrams
---
```

## Structure

```
aminrj.github.io/
├── _posts/            # blog posts (date-slug.md)
├── _tabs/             # navigation tabs (about, tags, categories, etc.)
├── _layouts/          # custom layouts (overriding Chirpy defaults)
├── _includes/         # custom includes
├── _newsletters/      # newsletter archive
├── assets/            # static assets (images, media, diagrams)
├── _config.yml        # site configuration
├── Gemfile            # Ruby dependencies
└── index.html         # homepage
```

## Contributing

This is a personal site. Issues and PRs are welcome if you spot broken links, formatting issues, or have suggestions for the newsletter format.

## License

Personal content is licensed under [CC BY-NC 4.0](LICENSE). Code (layouts, includes, assets) is MIT unless otherwise noted.
