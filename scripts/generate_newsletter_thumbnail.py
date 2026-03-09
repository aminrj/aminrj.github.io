#!/usr/bin/env python3
"""
Newsletter Thumbnail Generator for aminrj.com / Beehiiv
Generates 1200×630 JPEG thumbnails from a background template + issue metadata.

Usage:
    python generate_newsletter_thumbnail.py <issue_number> "<thumbnail_title>"
    python generate_newsletter_thumbnail.py <issue_number> "<thumbnail_title>" [output_path]

Examples:
    python generate_newsletter_thumbnail.py 3 "I Red-Teamed My Own Agent Stack"
    python generate_newsletter_thumbnail.py 7 "MCP Supply Chain Attacks Are Here" ../assets/media/newsletters/issue-7.jpg

Tip: keep thumbnail_title to ONE lead story, max ~50 chars.
     The script will truncate at 60 chars automatically.
"""

import sys
import os
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR   = Path(__file__).parent
REPO_ROOT    = SCRIPT_DIR.parent
BACKGROUND   = REPO_ROOT / "assets" / "media" / "newsletter-thumbnail-template.png"
OUTPUT_DIR   = REPO_ROOT / "assets" / "media" / "newsletters"
FONT_DIR     = SCRIPT_DIR / "fonts"

# ---------------------------------------------------------------------------
# Canvas
# ---------------------------------------------------------------------------
CANVAS_W, CANVAS_H = 1200, 630

# ---------------------------------------------------------------------------
# Typography
# ---------------------------------------------------------------------------
FONT_SIZE    = 72
MAX_CHARS    = 60
WRAP_WIDTH   = 22   # characters per line at FONT_SIZE 72
LINE_SPACING = 1.3  # multiplier on FONT_SIZE
MAX_LINES    = 2     # max lines for title before truncation (with ellipsis)

# Font search order — drop your own .ttf into scripts/fonts/ and it wins
FONT_CANDIDATES = [
    FONT_DIR / "InterBold.ttf",
    FONT_DIR / "IBMPlexSans-Bold.ttf",
    FONT_DIR / "Roboto-Bold.ttf",
    # macOS system
    Path("/Library/Fonts/Inter-Bold.ttf"),
    Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    Path("/System/Library/Fonts/Helvetica.ttc"),
    # Linux
    Path("/usr/share/fonts/truetype/inter/Inter-Bold.ttf"),
    Path("/usr/share/fonts/truetype/ibm-plex/IBMPlexSans-Bold.ttf"),
    Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    Path("/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
]

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
TEXT_COLOR      = (255, 255, 255)       # white title
ACCENT_COLOR    = (0, 200, 150)         # green accent for issue number
OVERLAY_COLOR   = (10, 15, 25)          # near-black navy
OVERLAY_OPACITY = 180                   # 0–255  (~70%)

# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------
TEXT_X       = 160    # left margin for all text
TEXT_Y       = 180   # vertical start for the title block
ISSUE_Y      = 130   # vertical position for the "#N" label


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def resolve_font(size: int) -> ImageFont.FreeTypeFont:
    """Return the first available font from FONT_CANDIDATES, else Pillow default."""
    for path in FONT_CANDIDATES:
        try:
            return ImageFont.truetype(str(path), size)
        except (OSError, IOError):
            continue
    print("⚠  No TrueType font found — using Pillow built-in (low quality).")
    print("   Drop InterBold.ttf or IBMPlexSans-Bold.ttf into scripts/fonts/ for best results.")
    return ImageFont.load_default()


def truncate(title: str, max_chars: int = MAX_CHARS) -> str:
    if len(title) > max_chars:
        return title[:max_chars].rstrip() + "…"
    return title


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def generate_newsletter_thumbnail(
    issue_number: int | str,
    thumbnail_title: str,
    output_path: Path,
) -> Path:
    """
    Composite a newsletter thumbnail and save it as a JPEG.

    Args:
        issue_number:    Issue number shown in the accent colour (e.g. 3).
        thumbnail_title: Short lead-story title (max 60 chars, auto-truncated).
        output_path:     Destination file path (.jpg / .jpeg).

    Returns:
        Resolved output path.
    """
    # --- Background ---
    if not BACKGROUND.exists():
        raise FileNotFoundError(
            f"Background template not found: {BACKGROUND}\n"
            "Place your template at assets/media/newsletter-thumbnail-template.png"
        )
    img = Image.open(BACKGROUND).convert("RGBA").resize((CANVAS_W, CANVAS_H), Image.LANCZOS)

    # --- Dark overlay (bottom 5/6 of the canvas) ---
    overlay = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(
        [(0, 120), (CANVAS_W, CANVAS_H)],
        fill=(*OVERLAY_COLOR, OVERLAY_OPACITY),
    )
    img = Image.alpha_composite(img, overlay)
    draw = ImageDraw.Draw(img)

    # --- Issue number (accent, prominent) ---
    font_small = resolve_font(48)
    draw.text((TEXT_X, ISSUE_Y), f"#{issue_number}", font=font_small, fill=ACCENT_COLOR)

    # --- Title (white, bold, wrapped) ---
    font_title = resolve_font(FONT_SIZE)
    safe_title  = truncate(thumbnail_title)
    lines       = textwrap.wrap(safe_title, width=WRAP_WIDTH)[:3]  # max 3 lines

    y = TEXT_Y
    for line in lines:
        draw.text((TEXT_X, y), line, font=font_title, fill=TEXT_COLOR)
        y += int(FONT_SIZE * LINE_SPACING)

    # --- Save as RGB JPEG (Beehiiv-ready) ---
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(output_path, "JPEG", quality=95)

    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    args = sys.argv[1:]

    if len(args) < 2 or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0 if args and args[0] in ("-h", "--help") else 1)

    issue_number    = args[0]
    thumbnail_title = args[1]

    # Optional explicit output path; otherwise auto-generate
    if len(args) >= 3:
        output_path = Path(args[2])
    else:
        slug = thumbnail_title.lower()
        for ch in " :,/\\\"'":
            slug = slug.replace(ch, "-")
        # collapse repeated dashes
        while "--" in slug:
            slug = slug.replace("--", "-")
        slug = slug.strip("-")[:60]
        output_path = OUTPUT_DIR / f"newsletter-{issue_number}-{slug}.jpg"

    print(f"\n🖼  Generating newsletter thumbnail")
    print(f"   Issue:  #{issue_number}")
    print(f"   Title:  {thumbnail_title[:60]}{'…' if len(thumbnail_title) > 60 else ''}")
    print(f"   Output: {output_path}\n")

    try:
        result = generate_newsletter_thumbnail(issue_number, thumbnail_title, output_path)
        rel = result.relative_to(REPO_ROOT)
        print(f"✓  Saved:  {result}")
        print(f"   Image path for front matter:  /{rel}")
    except FileNotFoundError as exc:
        print(f"✗  {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
