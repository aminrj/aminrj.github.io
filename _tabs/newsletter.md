---
layout: page
title: Newsletter
icon: fas fa-envelope
order: 3
---

<!-- ── Newsletter page styles ──────────────────────────────────────────── -->
<style>
/* ── Hero (latest issue) ─────────────────────────────────────────── */
.newsletter-hero {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 2rem;
  background: var(--card-bg);
  border: 1px solid var(--main-border-color);
  border-radius: 0.75rem;
  overflow: hidden;
  margin-bottom: 2.5rem;
  transition: box-shadow 0.2s ease;
}
.newsletter-hero:hover {
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}
.newsletter-hero-img-wrap {
  display: block;
  width: 100%;
  height: 100%;
  min-height: 220px;
  background-size: cover;
  background-position: center;
  background-image: url('{{ site.baseurl }}/assets/media/newsletters/newsletter-11-mcp-servers-just-tripled.jpg');
  text-decoration: none;
}
.newsletter-hero-body {
  padding: 1.75rem 2rem 1.75rem 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.newsletter-hero-label {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--bs-primary, #0d6efd);
  margin-bottom: 0.5rem;
}
.newsletter-hero-title {
  font-size: 1.5rem;
  font-weight: 800;
  line-height: 1.3;
  margin-bottom: 0.5rem;
  color: var(--text-color);
}
.newsletter-hero-title a {
  color: inherit;
  text-decoration: none;
}
.newsletter-hero-title a:hover {
  color: var(--bs-primary, #0d6efd);
}
.newsletter-hero-preview {
  font-size: 0.95rem;
  color: var(--text-muted-color);
  line-height: 1.55;
  margin-bottom: 0.75rem;
}
.newsletter-hero-meta {
  font-size: 0.8rem;
  color: var(--text-muted-color);
}
.newsletter-hero-meta span {
  margin-right: 1rem;
}
.newsletter-hero-cta {
  display: inline-block;
  margin-top: 0.75rem;
  padding: 0.45rem 1.25rem;
  font-size: 0.85rem;
  font-weight: 600;
  color: #fff !important;
  background: var(--bs-primary, #0d6efd);
  border-radius: 0.375rem;
  text-decoration: none;
  transition: background 0.15s ease;
  align-self: flex-start;
}
.newsletter-hero-cta:hover {
  background: #0b5ed7;
  color: #fff !important;
  text-decoration: none;
}
html[data-mode="dark"] .newsletter-hero-cta {
  background: #3d8bfd;
}
html[data-mode="dark"] .newsletter-hero-cta:hover {
  background: #5a9bfd;
}

/* ── Section headings ──────────────────────────────────────────────── */
.newsletter-section-title {
  font-size: 1.1rem;
  font-weight: 700;
  margin-bottom: 1.25rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid var(--main-border-color);
  color: var(--text-color);
}

/* ── Recent issues grid (Beehiiv-style cards) ──────────────────────── */
.newsletter-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 1.25rem;
  margin-bottom: 3rem;
}
.newsletter-card {
  display: flex;
  flex-direction: column;
  background: var(--card-bg);
  border: 1px solid var(--main-border-color);
  border-radius: 0.625rem;
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  transition: box-shadow 0.2s ease, transform 0.15s ease;
}
.newsletter-card:hover {
  box-shadow: 0 4px 20px rgba(0,0,0,0.07);
  transform: translateY(-2px);
}
.newsletter-card-img {
  width: 100%;
  height: 175px;
  display: block;
}
.newsletter-card-body {
  padding: 1.1rem 1.25rem 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}
.newsletter-card-issue {
  font-size: 0.68rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--bs-primary, #0d6efd);
  margin-bottom: 0.35rem;
}
.newsletter-card-title {
  font-size: 1rem;
  font-weight: 700;
  line-height: 1.35;
  margin-bottom: 0.4rem;
}
.newsletter-card-title a {
  color: var(--text-color);
  text-decoration: none;
}
.newsletter-card-title a:hover {
  color: var(--bs-primary, #0d6efd);
}
.newsletter-card-preview {
  font-size: 0.85rem;
  color: var(--text-muted-color);
  line-height: 1.5;
  margin-bottom: 0.65rem;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.newsletter-card-meta {
  font-size: 0.75rem;
  color: var(--text-muted-color);
}

/* ── Archive list ──────────────────────────────────────────────────── */
.newsletter-archive-list {
  list-style: none;
  padding: 0;
  margin: 0;
}
.newsletter-archive-item {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--main-border-color);
}
.newsletter-archive-item:last-child {
  border-bottom: none;
}
.newsletter-archive-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-color);
  text-decoration: none;
}
.newsletter-archive-title:hover {
  color: var(--bs-primary, #0d6efd);
}
.newsletter-archive-date {
  font-size: 0.8rem;
  color: var(--text-muted-color);
  white-space: nowrap;
  margin-left: 1rem;
}

/* ── Responsive ────────────────────────────────────────────────────── */
@media (max-width: 768px) {
  .newsletter-hero {
    grid-template-columns: 1fr;
  }
  .newsletter-hero-img {
    max-height: 200px;
  }
  .newsletter-hero-body {
    padding: 1.25rem;
  }
  .newsletter-grid {
    grid-template-columns: 1fr;
  }
}
</style>

<!-- ── Hero: latest issue (issue 11) ─────────────────────────────────── -->
{% assign latest = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-11"' | first %}
<div class="newsletter-hero">
  <a href="{{ site.baseurl }}{{ latest.url }}" class="newsletter-hero-img-wrap"></a>
  <div class="newsletter-hero-body">
    <div class="newsletter-hero-label">Latest Issue</div>
    <h2 class="newsletter-hero-title">
      <a href="{{ site.baseurl }}{{ latest.url }}">
        {{ latest.title }}
      </a>
    </h2>
    <p class="newsletter-hero-preview">
      {{ latest.preview_text | default: latest.subtitle | default: 'Weekly analysis of AI security threats, vulnerabilities, and defensive innovations.' }}
    </p>
    <div class="newsletter-hero-meta">
      <span>Issue #{{ latest.issue }}</span>
      <span>{{ latest.date | date: '%B %d, %Y' }}</span>
      {% if latest.reading_time %}<span>{{ latest.reading_time }} min read</span>{% endif %}
    </div>
    <a href="{{ site.baseurl }}{{ latest.url }}" class="newsletter-hero-cta">Read Issue →</a>
  </div>
</div>

<!-- ── Intro ─────────────────────────────────────────────────────────── -->
<div class="text-center my-4">
  <a href="https://newsletter.aminrj.com" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-lg px-5">
    <i class="fas fa-external-link-alt me-2"></i>Read on Beehiiv
  </a>
  <p class="text-muted small mt-2">newsletter.aminrj.com</p>
</div>

<p class="mb-4">Weekly analysis of the threats, vulnerabilities, and defensive innovations shaping AI security. Written for security engineers and CTOs who need signal, not hype.</p>

<!-- ── Recent issues ─────────────────────────────────────────────────── -->
<h3 class="newsletter-section-title">Recent Issues</h3>

{% assign n11 = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-11"' | first %}
{% assign n10 = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-10"' | first %}
{% assign n9  = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-9"'  | first %}
{% assign n8  = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-8"'  | first %}
{% if n11 or n10 or n9 or n8 %}
<div class="newsletter-grid">
{% assign thumb = nil %}{% if n11 %}{% assign thumb = 'newsletter-11-mcp-servers-just-tripled.jpg' %}{% endif %}
  <a href="{{ n11.url }}" class="newsletter-card">
    <div class="newsletter-card-img"{% if thumb %} style="background-image:url('{{ site.baseurl }}/assets/media/newsletters/{{ thumb }}');background-size:cover;background-position:center;"{% else %} style="background:var(--main-bg);display:flex;align-items:center;justify-content:center;"{% endif %}></div>
    <div class="newsletter-card-body">
      <div class="newsletter-card-issue">Issue #{{ n11.issue }}</div>
      <h4 class="newsletter-card-title">{{ n11.title }}</h4>
      <p class="newsletter-card-preview">{{ n11.preview_text | default: n11.subtitle | strip_html | truncate: 160 }}</p>
      <div class="newsletter-card-meta">{{ n11.date | date: '%B %d, %Y' }}</div>
    </div>
  </a>
{% assign thumb = nil %}{% if n10 %}{% assign thumb = 'newsletter-10-most-mcp-servers-trust-every-request-by-default.jpg' %}{% endif %}
  <a href="{{ n10.url }}" class="newsletter-card">
    <div class="newsletter-card-img"{% if thumb %} style="background-image:url('{{ site.baseurl }}/assets/media/newsletters/{{ thumb }}');background-size:cover;background-position:center;"{% else %} style="background:var(--main-bg);display:flex;align-items:center;justify-content:center;"{% endif %}></div>
    <div class="newsletter-card-body">
      <div class="newsletter-card-issue">Issue #{{ n10.issue }}</div>
      <h4 class="newsletter-card-title">{{ n10.title }}</h4>
      <p class="newsletter-card-preview">{{ n10.preview_text | default: n10.subtitle | strip_html | truncate: 160 }}</p>
      <div class="newsletter-card-meta">{{ n10.date | date: '%B %d, %Y' }}</div>
    </div>
  </a>
{% assign thumb = nil %}{% if n9 %}{% assign thumb = 'newsletter-9-8-agent-exploits-in-q1.jpg' %}{% endif %}
  <a href="{{ n9.url }}" class="newsletter-card">
    <div class="newsletter-card-img"{% if thumb %} style="background-image:url('{{ site.baseurl }}/assets/media/newsletters/{{ thumb }}');background-size:cover;background-position:center;"{% else %} style="background:var(--main-bg);display:flex;align-items:center;justify-content:center;"{% endif %}></div>
    <div class="newsletter-card-body">
      <div class="newsletter-card-issue">Issue #{{ n9.issue }}</div>
      <h4 class="newsletter-card-title">{{ n9.title }}</h4>
      <p class="newsletter-card-preview">{{ n9.preview_text | default: n9.subtitle | strip_html | truncate: 160 }}</p>
      <div class="newsletter-card-meta">{{ n9.date | date: '%B %d, %Y' }}</div>
    </div>
  </a>
{% assign thumb = nil %}{% if n8 %}{% assign thumb = 'newsletter-8-closed-agent-harness.jpg' %}{% endif %}
  <a href="{{ n8.url }}" class="newsletter-card">
    <div class="newsletter-card-img"{% if thumb %} style="background-image:url('{{ site.baseurl }}/assets/media/newsletters/{{ thumb }}');background-size:cover;background-position:center;"{% else %} style="background:var(--main-bg);display:flex;align-items:center;justify-content:center;"{% endif %}></div>
    <div class="newsletter-card-body">
      <div class="newsletter-card-issue">Issue #{{ n8.issue }}</div>
      <h4 class="newsletter-card-title">{{ n8.title }}</h4>
      <p class="newsletter-card-preview">{{ n8.preview_text | default: n8.subtitle | strip_html | truncate: 160 }}</p>
      <div class="newsletter-card-meta">{{ n8.date | date: '%B %d, %Y' }}</div>
    </div>
  </a>
</div>
{% endif %}

<!-- ── Archive ───────────────────────────────────────────────────────── -->
<h3 class="newsletter-section-title">Archive</h3>

{% assign older = site.newsletters | where_exp:'n','n.url contains "newsletter-2025"' | sort: 'date' | reverse %}
{% if older.size > 0 %}
<ul class="newsletter-archive-list">
{% for newsletter in older %}
  <li class="newsletter-archive-item">
    <a href="{{ newsletter.url }}" class="newsletter-archive-title">
      {% if newsletter.title != "AI Security Intelligence Digest" %}
        {{ newsletter.title }}
      {% else %}
        Issue #{{ newsletter.issue }}
      {% endif %}
    </a>
    <span class="newsletter-archive-date">{{ newsletter.date | date: '%b %d, %Y' }}</span>
  </li>
{% endfor %}
</ul>
{% else %}
<p class="text-muted">No older issues available.</p>
{% endif %}

<!-- ── Subscribe CTA ─────────────────────────────────────────────────── -->
<div class="mt-5 p-4" style="background:var(--card-bg);border:1px solid var(--main-border-color);border-radius:0.5rem;border-left:4px solid var(--bs-primary,rgba(13,110,253,0.15));">
  <h5 style="margin-bottom:0.5rem;">Subscribe to AI Security Intelligence Digest</h5>
  <p class="text-muted mb-3" style="font-size:0.9rem;">Weekly analysis of AI security threats, vulnerabilities, and defensive innovations — delivered to your inbox.</p>
  <a href="/subscribe/" class="btn btn-primary">
    <i class="fas fa-envelope me-2"></i>Subscribe — it's free
  </a>
</div>
