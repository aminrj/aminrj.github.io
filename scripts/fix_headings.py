#!/usr/bin/env python3
"""
Convert Title Case headings to sentence case in markdown files.
Preserves: acronyms, proper nouns, code blocks, frontmatter.
"""
import re
import sys
from pathlib import Path

# Words/terms to always keep as-is (case-sensitive)
PRESERVE = {
    # Acronyms
    "MCP", "LLM", "LLMs", "RAG", "API", "APIs", "AI", "ML", "EU", "UK", "US",
    "OWASP", "CVSS", "CVE", "ASI", "ASI01", "ASI02", "ASI03", "ASI04", "ASI05",
    "ASI06", "ASI07", "ASI08", "ASI09", "ASI10", "CIA", "CISO", "RSAC",
    "SDK", "CLI", "HTTP", "HTTPS", "YAML", "JSON", "REST", "TLS", "SSH",
    "IoT", "SaaS", "PaaS", "IaaS", "CI", "CD", "CICD", "VPN", "DNS", "AWS",
    "GCP", "IBM", "ISO", "SOC", "GDPR", "NIS2", "NIST", "MITRE", "CSA",
    "GitOps", "DevOps", "DevSecOps", "SecOps", "AppSec",
    # Products / proper nouns
    "Docker", "Kubernetes", "GitHub", "GitLab", "ArgoCD", "Argo",
    "Claude", "OpenAI", "Google", "Anthropic", "Microsoft", "Meta",
    "Ollama", "Loki", "Grafana", "Prometheus", "Kafka", "Redis",
    "Terraform", "Helm", "Pydantic", "Python", "JavaScript", "TypeScript",
    "Linux", "macOS", "Windows", "Ubuntu",
    "PostgreSQL", "MySQL", "MongoDB",
    "Obsidian", "Discord", "WhatsApp", "Slack",
    "PyRIT", "OpenClaw", "MetalLB", "Nginx", "Cert-Manager", "ExternalDNS",
    "MicroK8s", "Minikube", "Grafana",
    # Regulatory / frameworks
    "GPAI", "Article", "Annex",
    # Roman numerals / numbered
    "I", "II", "III", "IV", "V",
}

# Patterns that signal the word should stay as written (e.g., all-caps acronyms)
ACRONYM_RE = re.compile(r'^[A-Z]{2,}(?:-[A-Z0-9]+)*$')
NUMBERED_RE = re.compile(r'^\d+$')


def should_preserve(word: str) -> bool:
    """Return True if word should keep its case."""
    # Strip trailing punctuation for lookup
    stripped = word.rstrip('.,;:!?()')
    if stripped in PRESERVE:
        return True
    if ACRONYM_RE.match(stripped):
        return True
    if NUMBERED_RE.match(stripped):
        return True
    return False


def sentence_case_heading(heading: str) -> str:
    """
    Convert a markdown heading to sentence case.
    Preserves the leading # characters and whitespace.
    """
    # Match the heading prefix (##, ###, etc.) and the text
    m = re.match(r'^(#{1,6}\s+)(.*)', heading)
    if not m:
        return heading
    prefix, text = m.group(1), m.group(2)

    words = text.split()
    if not words:
        return heading

    result = []
    for i, word in enumerate(words):
        if i == 0:
            # First word: capitalize first letter, leave rest of word as-is
            if word and word[0].isalpha():
                result.append(word[0].upper() + word[1:])
            else:
                result.append(word)
        elif should_preserve(word):
            result.append(word)
        else:
            # Lowercase the word, but preserve any all-caps acronyms embedded in it
            result.append(word.lower())

    return prefix + ' '.join(result)


def process_file(filepath: Path) -> int:
    """Process a single markdown file. Returns number of headings changed."""
    content = filepath.read_text(encoding='utf-8')
    lines = content.split('\n')

    in_frontmatter = False
    frontmatter_done = False
    in_code_block = False
    changes = 0
    new_lines = []

    for i, line in enumerate(lines):
        # Track frontmatter
        if i == 0 and line.strip() == '---':
            in_frontmatter = True
            new_lines.append(line)
            continue
        if in_frontmatter and line.strip() == '---':
            in_frontmatter = False
            frontmatter_done = True
            new_lines.append(line)
            continue
        if in_frontmatter:
            new_lines.append(line)
            continue

        # Track code blocks (``` or ~~~)
        if re.match(r'^\s*(`{3,}|~{3,})', line):
            in_code_block = not in_code_block
            new_lines.append(line)
            continue

        if in_code_block:
            new_lines.append(line)
            continue

        # Process headings
        if re.match(r'^#{1,6}\s+', line):
            new_line = sentence_case_heading(line)
            if new_line != line:
                changes += 1
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if changes > 0:
        filepath.write_text('\n'.join(new_lines), encoding='utf-8')
        print(f"  {filepath.name}: {changes} headings updated")
    
    return changes


def main():
    posts_dir = Path('/Users/ARAJI/git/aminrj_com/personal_website_2024/_posts')
    
    files = sys.argv[1:] if len(sys.argv) > 1 else []
    if not files:
        # Process all markdown posts
        target_files = sorted(posts_dir.glob('*.md'))
    else:
        target_files = [posts_dir / f for f in files]

    total = 0
    for fp in target_files:
        if fp.name == '.placeholder':
            continue
        n = process_file(fp)
        total += n
    
    print(f"\nTotal headings updated: {total}")


if __name__ == '__main__':
    main()
