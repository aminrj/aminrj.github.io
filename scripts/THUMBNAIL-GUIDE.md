# Thumbnail Generator Guide

## Quick Start

Generate thumbnails with:
```bash
python3 scripts/generate_thumbnail.py <category> "Your Post Title"
```

## Examples

```bash
# Auto-generate filename
python3 scripts/generate_thumbnail.py ai-security "Evaluating AI Agents"

# Custom filename
python3 scripts/generate_thumbnail.py devops "CI/CD Best Practices" cicd-guide.png

# From project root
cd /Users/ARAJI/git/aminrj_com/personal_website_2024
python3 scripts/generate_thumbnail.py k8s "Kubernetes Security Tips"
```

## Available Categories

Each category has its own color scheme:
- `ai` - Purple/blue tones
- `ai-security` - Dark red tones
- `devops` - Blue tones
- `cloud-native` - Cyan tones
- `cybersecurity` - Red tones
- `networking` - Green tones
- `k8s` - Kubernetes blue
- `innovation` - Purple tones
- `iot` - Green tones
- `procurement-ai` - Gray-blue
- `external-secrets` - Purple-gray
- `argocd` - Orange tones
- `kafka-k8s` - Dark gray
- `notes` - Beige tones

## Format Specifications

- **Resolution**: 1200×630 pixels (Open Graph standard)
- **Format**: PNG
- **Features**:
  - Automatic text wrapping for long titles
  - Category-based color gradients
  - Subtle shadow effects
  - "aminrj.com" branding at bottom
  - Optimized file size

## Customization

### Using a Custom Template
If you create `assets/media/template.png` (1200×630), the script will use it as the base instead of generating a gradient.

### Adding New Color Schemes
Edit `scripts/generate_thumbnail.py` and add to the `COLOR_SCHEMES` dictionary:
```python
"my-category": [(R1, G1, B1), (R2, G2, B2)],
```

## Workflow

1. Write your post
2. Generate thumbnail: `python3 scripts/generate_thumbnail.py <category> "Title"`
3. Add to post frontmatter:
   ```yaml
   image:
     path: /assets/media/<category>/<filename>.png
   ```

## Tips

- Keep titles concise (5-10 words work best)
- The script auto-wraps long titles into multiple lines
- Generated files are automatically saved to the correct category folder
- Output path is printed for easy copy-paste
