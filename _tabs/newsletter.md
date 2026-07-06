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
  background-image: url('{{ site.baseurl }}/assets/media/newsletters/newsletter-15-one-character-bypasses-auth-on-millions-of-ai-servers.jpg');
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

<!-- ── Hero: latest issue (issue 18) ─────────────────────────────────── -->
{% assign latest = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-18"' | first %}
<div class="newsletter-hero">
  <a href="{{ site.baseurl }}{{ latest.url }}" class="newsletter-hero-img-wrap" style="background-image:url('{{ site.baseurl }}/assets/media/newsletters/newsletter-18-mcp-goes-stateless-your-gateway-goes-blind.jpg');"></a>
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
<p class="mb-4">Weekly analysis of the threats, vulnerabilities, and defensive innovations shaping AI security. Written for security engineers and CTOs who need signal, not hype.</p>

<!-- ── Recent issues ─────────────────────────────────────────────────── -->
<h3 class="newsletter-section-title">Recent Issues</h3>

{% assign n18 = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-18"' | first %}
{% assign n17 = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-17"' | first %}
{% assign n16 = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-16"' | first %}
{% assign n15 = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-15"' | first %}
{% assign n14 = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-14"' | first %}
{% assign n13 = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-13"' | first %}
{% if n18 or n17 or n16 or n15 or n14 or n13 %}
<div class="newsletter-grid">
{% assign thumb = nil %}{% if n18 %}{% assign thumb = 'newsletter-18-mcp-goes-stateless-your-gateway-goes-blind.jpg' %}{% endif %}
  <a href="{{ n18.url }}" class="newsletter-card">
    <div class="newsletter-card-img"{% if thumb %} style="background-image:url('{{ site.baseurl }}/assets/media/newsletters/{{ thumb }}');background-size:cover;background-position:center;"{% else %} style="background:var(--main-bg);display:flex;align-items:center;justify-content:center;"{% endif %}></div>
    <div class="newsletter-card-body">
      <div class="newsletter-card-issue">Issue #{{ n18.issue }}</div>
      <h4 class="newsletter-card-title">{{ n18.title }}</h4>
      <p class="newsletter-card-preview">{{ n18.preview_text | default: n18.subtitle | strip_html | truncate: 160 }}</p>
      <div class="newsletter-card-meta">{{ n18.date | date: '%B %d, %Y' }}</div>
    </div>
  </a>
{% assign thumb = nil %}{% if n17 %}{% assign thumb = 'newsletter-17-your-agents-have-no-idea-who-they-are.jpg' %}{% endif %}
  <a href="{{ n17.url }}" class="newsletter-card">
    <div class="newsletter-card-img"{% if thumb %} style="background-image:url('{{ site.baseurl }}/assets/media/newsletters/{{ thumb }}');background-size:cover;background-position:center;"{% else %} style="background:var(--main-bg);display:flex;align-items:center;justify-content:center;"{% endif %}></div>
    <div class="newsletter-card-body">
      <div class="newsletter-card-issue">Issue #{{ n17.issue }}</div>
      <h4 class="newsletter-card-title">{{ n17.title }}</h4>
      <p class="newsletter-card-preview">{{ n17.preview_text | default: n17.subtitle | strip_html | truncate: 160 }}</p>
      <div class="newsletter-card-meta">{{ n17.date | date: '%B %d, %Y' }}</div>
    </div>
  </a>
{% assign thumb = nil %}{% if n16 %}{% assign thumb = 'newsletter-16-i-let-an-agent-rewrite-my-code-while-i-slept.jpg' %}{% endif %}
  <a href="{{ n16.url }}" class="newsletter-card">
    <div class="newsletter-card-img"{% if thumb %} style="background-image:url('{{ site.baseurl }}/assets/media/newsletters/{{ thumb }}');background-size:cover;background-position:center;"{% else %} style="background:var(--main-bg);display:flex;align-items:center;justify-content:center;"{% endif %}></div>
    <div class="newsletter-card-body">
      <div class="newsletter-card-issue">Issue #{{ n16.issue }}</div>
      <h4 class="newsletter-card-title">{{ n16.title }}</h4>
      <p class="newsletter-card-preview">{{ n16.preview_text | default: n16.subtitle | strip_html | truncate: 160 }}</p>
      <div class="newsletter-card-meta">{{ n16.date | date: '%B %d, %Y' }}</div>
    </div>
  </a>
{% assign thumb = nil %}{% if n15 %}{% assign thumb = 'newsletter-15-one-character-bypasses-auth-on-millions-of-ai-servers.jpg' %}{% endif %}
  <a href="{{ n15.url }}" class="newsletter-card">
    <div class="newsletter-card-img"{% if thumb %} style="background-image:url('{{ site.baseurl }}/assets/media/newsletters/{{ thumb }}');background-size:cover;background-position:center;"{% else %} style="background:var(--main-bg);display:flex;align-items:center;justify-content:center;"{% endif %}></div>
    <div class="newsletter-card-body">
      <div class="newsletter-card-issue">Issue #{{ n15.issue }}</div>
      <h4 class="newsletter-card-title">{{ n15.title }}</h4>
      <p class="newsletter-card-preview">{{ n15.preview_text | default: n15.subtitle | strip_html | truncate: 160 }}</p>
      <div class="newsletter-card-meta">{{ n15.date | date: '%B %d, %Y' }}</div>
    </div>
  </a>
{% assign thumb = nil %}{% if n14 %}{% assign thumb = 'newsletter-14-your-coding-agents-approval-prompt-is-lying-to-you.jpg' %}{% endif %}
  <a href="{{ n14.url }}" class="newsletter-card">
    <div class="newsletter-card-img"{% if thumb %} style="background-image:url('{{ site.baseurl }}/assets/media/newsletters/{{ thumb }}');background-size:cover;background-position:center;"{% else %} style="background:var(--main-bg);display:flex;align-items:center;justify-content:center;"{% endif %}></div>
    <div class="newsletter-card-body">
      <div class="newsletter-card-issue">Issue #{{ n14.issue }}</div>
      <h4 class="newsletter-card-title">{{ n14.title }}</h4>
      <p class="newsletter-card-preview">{{ n14.preview_text | default: n14.subtitle | strip_html | truncate: 160 }}</p>
      <div class="newsletter-card-meta">{{ n14.date | date: '%B %d, %Y' }}</div>
    </div>
  </a>
{% assign thumb = nil %}{% if n13 %}{% assign thumb = 'newsletter-13-six-governments-agree-your-ai-security-model-was-wrong.jpg' %}{% endif %}
  <a href="{{ n13.url }}" class="newsletter-card">
    <div class="newsletter-card-img"{% if thumb %} style="background-image:url('{{ site.baseurl }}/assets/media/newsletters/{{ thumb }}');background-size:cover;background-position:center;"{% else %} style="background:var(--main-bg);display:flex;align-items:center;justify-content:center;"{% endif %}></div>
    <div class="newsletter-card-body">
      <div class="newsletter-card-issue">Issue #{{ n13.issue }}</div>
      <h4 class="newsletter-card-title">{{ n13.title }}</h4>
      <p class="newsletter-card-preview">{{ n13.preview_text | default: n13.subtitle | strip_html | truncate: 160 }}</p>
      <div class="newsletter-card-meta">{{ n13.date | date: '%B %d, %Y' }}</div>
    </div>
  </a>
</div>
{% endif %}

<!-- ── Archive (Issues 1–12) ─────────────────────────────────────────── -->
<h3 class="newsletter-section-title">Earlier Issues</h3>

{% assign n12 = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-12"' | first %}
{% assign n11 = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-11"' | first %}
{% assign n10 = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-10"' | first %}
{% assign n9  = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-9"'  | first %}
{% assign n8  = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-8"'  | first %}
{% assign n7  = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-7"'  | first %}
{% assign n6  = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-6"'  | first %}
{% assign n5  = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-5"'  | first %}
{% assign n4  = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-4"'  | first %}
{% assign n3  = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-3"'  | first %}
{% assign n2  = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-2"'  | first %}
{% assign n1  = site.newsletters | where_exp:'n','n.url contains "newsletter-issue-1"'  | first %}
<ul class="newsletter-archive-list">
{% if n12 %}
  <li class="newsletter-archive-item">
    <a href="{{ site.baseurl }}{{ n12.url }}" class="newsletter-archive-title">{{ n12.title }}</a>
    <span class="newsletter-archive-date">{{ n12.date | date: '%b %d, %Y' }}</span>
  </li>
{% endif %}
{% if n11 %}
  <li class="newsletter-archive-item">
    <a href="{{ site.baseurl }}{{ n11.url }}" class="newsletter-archive-title">{{ n11.title }}</a>
    <span class="newsletter-archive-date">{{ n11.date | date: '%b %d, %Y' }}</span>
  </li>
{% endif %}
{% if n10 %}
  <li class="newsletter-archive-item">
    <a href="{{ site.baseurl }}{{ n10.url }}" class="newsletter-archive-title">{{ n10.title }}</a>
    <span class="newsletter-archive-date">{{ n10.date | date: '%b %d, %Y' }}</span>
  </li>
{% endif %}
{% if n9 %}
  <li class="newsletter-archive-item">
    <a href="{{ site.baseurl }}{{ n9.url }}" class="newsletter-archive-title">{{ n9.title }}</a>
    <span class="newsletter-archive-date">{{ n9.date | date: '%b %d, %Y' }}</span>
  </li>
{% endif %}
{% if n8 %}
  <li class="newsletter-archive-item">
    <a href="{{ site.baseurl }}{{ n8.url }}" class="newsletter-archive-title">{{ n8.title }}</a>
    <span class="newsletter-archive-date">{{ n8.date | date: '%b %d, %Y' }}</span>
  </li>
{% endif %}
{% if n7 %}
  <li class="newsletter-archive-item">
    <a href="{{ site.baseurl }}{{ n7.url }}" class="newsletter-archive-title">{{ n7.title }}</a>
    <span class="newsletter-archive-date">{{ n7.date | date: '%b %d, %Y' }}</span>
  </li>
{% endif %}
{% if n6 %}
  <li class="newsletter-archive-item">
    <a href="{{ site.baseurl }}{{ n6.url }}" class="newsletter-archive-title">{{ n6.title }}</a>
    <span class="newsletter-archive-date">{{ n6.date | date: '%b %d, %Y' }}</span>
  </li>
{% endif %}
{% if n5 %}
  <li class="newsletter-archive-item">
    <a href="{{ site.baseurl }}{{ n5.url }}" class="newsletter-archive-title">{{ n5.title }}</a>
    <span class="newsletter-archive-date">{{ n5.date | date: '%b %d, %Y' }}</span>
  </li>
{% endif %}
{% if n4 %}
  <li class="newsletter-archive-item">
    <a href="{{ site.baseurl }}{{ n4.url }}" class="newsletter-archive-title">{{ n4.title }}</a>
    <span class="newsletter-archive-date">{{ n4.date | date: '%b %d, %Y' }}</span>
  </li>
{% endif %}
{% if n3 %}
  <li class="newsletter-archive-item">
    <a href="{{ site.baseurl }}{{ n3.url }}" class="newsletter-archive-title">{{ n3.title }}</a>
    <span class="newsletter-archive-date">{{ n3.date | date: '%b %d, %Y' }}</span>
  </li>
{% endif %}
{% if n2 %}
  <li class="newsletter-archive-item">
    <a href="{{ site.baseurl }}{{ n2.url }}" class="newsletter-archive-title">{{ n2.title }}</a>
    <span class="newsletter-archive-date">{{ n2.date | date: '%b %d, %Y' }}</span>
  </li>
{% endif %}
{% if n1 %}
  <li class="newsletter-archive-item">
    <a href="{{ site.baseurl }}{{ n1.url }}" class="newsletter-archive-title">{{ n1.title }}</a>
    <span class="newsletter-archive-date">{{ n1.date | date: '%b %d, %Y' }}</span>
  </li>
{% endif %}
</ul>

<!-- ── Read on Beehiiv ────────────────────────────────────────────────── -->
<div class="text-center my-4">
  <a href="https://newsletter.aminrj.com" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-lg px-5">
    <i class="fas fa-external-link-alt me-2"></i>Read on Beehiiv
  </a>
  <p class="text-muted small mt-2">newsletter.aminrj.com</p>
</div>

<!-- ── Subscribe CTA ─────────────────────────────────────────────────── -->
<div class="mt-5 p-4" style="background:var(--card-bg);border:1px solid var(--main-border-color);border-radius:0.5rem;border-left:4px solid var(--bs-primary,rgba(13,110,253,0.15));">
  <h5 style="margin-bottom:0.5rem;">Subscribe to AI Security Intelligence Digest</h5>
  <p class="text-muted mb-3" style="font-size:0.9rem;">Weekly analysis of AI security threats, vulnerabilities, and defensive innovations — delivered to your inbox.</p>
  <a href="/subscribe/" class="btn btn-primary">
    <i class="fas fa-envelope me-2"></i>Subscribe — it's free
  </a>
</div>
