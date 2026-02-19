#!/usr/bin/env python3
"""
Thumbnail Generator for aminrj.com
Generates 1200x630 PNG thumbnails with gradients and text overlay
"""

import sys
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap

# Configuration
THUMBNAIL_WIDTH = 1200
THUMBNAIL_HEIGHT = 630
TEMPLATE_PATH = Path(__file__).parent.parent / "assets" / "media" / "template.png"
OUTPUT_BASE = Path(__file__).parent.parent / "assets" / "media"

# Color schemes by category
COLOR_SCHEMES = {
    "ai": [(20, 20, 40), (80, 40, 120)],
    "ai-security": [(40, 20, 20), (120, 40, 60)],
    "devops": [(20, 40, 60), (40, 80, 120)],
    "cloud-native": [(20, 50, 70), (60, 120, 160)],
    "cybersecurity": [(60, 20, 20), (140, 40, 40)],
    "networking": [(20, 60, 40), (40, 120, 80)],
    "k8s": [(50, 100, 180), (30, 60, 120)],
    "innovation": [(100, 40, 120), (140, 80, 160)],
    "iot": [(40, 100, 60), (80, 140, 100)],
    "procurement-ai": [(60, 80, 100), (100, 120, 140)],
    "external-secrets": [(80, 60, 100), (120, 100, 140)],
    "argocd": [(220, 100, 40), (180, 60, 20)],
    "kafka-k8s": [(40, 40, 40), (80, 80, 80)],
    "notes": [(100, 100, 80), (140, 140, 120)],
    "default": [(30, 40, 50), (70, 90, 110)],
}


def create_gradient(width, height, color1, color2):
    """Creates a vertical gradient image"""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    for y in range(height):
        mask_data.extend([int(255 * (y / height))] * width)
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base


def get_font(size):
    """Try to get a good font, fall back to default"""
    font_paths = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]
    
    for font_path in font_paths:
        try:
            return ImageFont.truetype(font_path, size)
        except:
            continue
    
    return ImageFont.load_default()


def wrap_text(text, font, max_width):
    """Wrap text to fit within max_width"""
    lines = []
    words = text.split()
    
    while words:
        line = ''
        while words:
            test_line = line + words[0] + ' '
            bbox = font.getbbox(test_line)
            width = bbox[2] - bbox[0]
            if width <= max_width:
                line = test_line
                words.pop(0)
            else:
                break
        
        if not line:
            line = words.pop(0) + ' '
        
        lines.append(line.strip())
    
    return lines


def generate_thumbnail(title, category, output_filename):
    """Generate a thumbnail with title and category-based color scheme"""
    
    # Check if template exists
    if TEMPLATE_PATH.exists():
        img = Image.open(TEMPLATE_PATH).convert('RGB')
        if img.size != (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT):
            img = img.resize((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), Image.LANCZOS)
    else:
        # Create gradient background
        colors = COLOR_SCHEMES.get(category, COLOR_SCHEMES["default"])
        img = create_gradient(THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT, colors[0], colors[1])
    
    draw = ImageDraw.Draw(img)
    
    # Add subtle overlay
    overlay = Image.new('RGBA', (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), (0, 0, 0, 60))
    img.paste(overlay, (0, 0), overlay)
    
    # Add title text
    title_font = get_font(72)
    max_width = THUMBNAIL_WIDTH - 120  # 60px padding on each side
    
    # Wrap text
    lines = wrap_text(title, title_font, max_width)
    
    # Calculate total height
    line_heights = [title_font.getbbox(line)[3] - title_font.getbbox(line)[1] for line in lines]
    total_height = sum(line_heights) + (len(lines) - 1) * 20  # 20px spacing
    
    # Start position (centered vertically)
    y = (THUMBNAIL_HEIGHT - total_height) // 2
    
    # Draw each line
    for line, line_height in zip(lines, line_heights):
        bbox = title_font.getbbox(line)
        text_width = bbox[2] - bbox[0]
        x = (THUMBNAIL_WIDTH - text_width) // 2
        
        # Draw shadow
        draw.text((x + 3, y + 3), line, font=title_font, fill=(0, 0, 0, 180))
        # Draw text
        draw.text((x, y), line, font=title_font, fill=(255, 255, 255))
        
        y += line_height + 20
    
    # Add subtle branding at bottom
    brand_font = get_font(24)
    brand_text = "aminrj.com"
    bbox = brand_font.getbbox(brand_text)
    brand_width = bbox[2] - bbox[0]
    draw.text(
        (THUMBNAIL_WIDTH - brand_width - 30, THUMBNAIL_HEIGHT - 40),
        brand_text,
        font=brand_font,
        fill=(255, 255, 255, 200)
    )
    
    # Save
    output_dir = OUTPUT_BASE / category
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_filename
    
    img.save(output_path, 'PNG', optimize=True)
    print(f"✓ Thumbnail saved: {output_path}")
    print(f"  Use in post: /assets/media/{category}/{output_filename}")
    
    return output_path


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_thumbnail.py <category> <title> [output-filename]")
        print("\nExamples:")
        print('  python generate_thumbnail.py ai-security "Evaluating AI Agents" evaluating-ai-agents.png')
        print('  python generate_thumbnail.py devops "CI/CD Best Practices"')
        print("\nAvailable categories:")
        print("  " + ", ".join(sorted(COLOR_SCHEMES.keys())))
        sys.exit(1)
    
    category = sys.argv[1]
    title = sys.argv[2]
    
    # Generate filename if not provided
    if len(sys.argv) >= 4:
        output_filename = sys.argv[3]
    else:
        output_filename = title.lower().replace(' ', '-').replace(',', '').replace(':', '') + '.png'
    
    if not output_filename.endswith('.png'):
        output_filename += '.png'
    
    generate_thumbnail(title, category, output_filename)


if __name__ == "__main__":
    main()
