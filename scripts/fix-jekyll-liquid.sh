#!/bin/bash
# Simple sed version for macOS - FIXED
set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() { echo -e "${BLUE}ℹ${NC} $1"; }
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }

INPUT_FILE="$1"

if [ ! -f "$INPUT_FILE" ]; then
  echo "Error: File not found: $INPUT_FILE"
  exit 1
fi

FILENAME=$(basename "$INPUT_FILE")
DIRNAME=$(dirname "$INPUT_FILE")
BASENAME="${FILENAME%.*}"
OUTPUT_FILE="${DIRNAME}/${BASENAME}-fixed.md"
BACKUP_FILE="${INPUT_FILE}.backup-$(date +%Y%m%d-%H%M%S)"

# Backup
cp "$INPUT_FILE" "$BACKUP_FILE"
print_success "Backup: $BACKUP_FILE"

# Check for frontmatter
HAS_FRONTMATTER=false
if head -n 1 "$INPUT_FILE" | grep -q "^---"; then
  HAS_FRONTMATTER=true
  print_info "Frontmatter detected"
fi

# Create a temp file for processing
TEMP_FILE=$(mktemp)

# Use awk instead of sed for more reliable processing on macOS
awk '
BEGIN {
  in_code_block = 0
  in_frontmatter = 0
  frontmatter_count = 0
}

# Track frontmatter
/^---$/ {
  frontmatter_count++
  if (frontmatter_count == 1) in_frontmatter = 1
  else if (frontmatter_count == 2) in_frontmatter = 0
  print
  next
}

# Skip processing inside frontmatter
in_frontmatter == 1 {
  print
  next
}

# Track code blocks
/^```/ {
  in_code_block = !in_code_block
  print
  next
}

# Process regular lines (not in code blocks)
in_code_block == 0 {
  # Remove existing raw tags
  gsub(/{%[[:space:]]*raw[[:space:]]*%}/, "")
  gsub(/{%[[:space:]]*endraw[[:space:]]*%}/, "")

  # Wrap inline n8n expressions
  # Pattern: `{{ $something }}` becomes {% raw %}`{{ $something }}`{% endraw %}
  while (match($0, /`[{][{][[:space:]]*[$][^}]*[}][}]`/)) {
    before = substr($0, 1, RSTART - 1)
    matched = substr($0, RSTART, RLENGTH)
    after = substr($0, RSTART + RLENGTH)
    $0 = before "{% raw %}" matched "{% endraw %}" after
  }

  print
  next
}

# Inside code blocks - print as is
{
  print
}
' "$INPUT_FILE" >"$TEMP_FILE"

# Add frontmatter if missing
if [ "$HAS_FRONTMATTER" = false ]; then
  print_warning "Adding frontmatter"

  DATE=$(echo "$BASENAME" | grep -oE '^[0-9]{4}-[0-9]{2}-[0-9]{2}' || date +%Y-%m-%d)
  TITLE=$(grep -m 1 "^# " "$TEMP_FILE" | sed 's/^# //' | sed 's/[^a-zA-Z0-9 :]//g' || echo "n8n Guide")

  {
    cat <<EOF
---
layout: post
title: "$TITLE"
date: $DATE 10:00:00 +0000
categories: [automation, workflows]
tags: [n8n, automation, tutorial]
toc: true
---

EOF
    cat "$TEMP_FILE"
  } >"$OUTPUT_FILE"
  rm "$TEMP_FILE"
else
  mv "$TEMP_FILE" "$OUTPUT_FILE"
fi

print_success "Fixed: $OUTPUT_FILE"
echo ""
print_info "Next steps:"
echo "  1. Review: head -50 $OUTPUT_FILE"
echo "  2. Test:   jekyll serve --trace"
echo "  3. Apply:  mv $OUTPUT_FILE $INPUT_FILE"
echo ""
print_info "Original backup: $BACKUP_FILE"
