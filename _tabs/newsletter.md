---
layout: page
title: Newsletter
icon: fas fa-envelope
order: 3
---

# AI Security Intelligence Digest

<div class="alert alert-info" role="alert">
  <strong>The newsletter is back.</strong> After a hiatus, the AI Security Intelligence Digest returns in weekly format — deeper analysis, less noise.
</div>

Weekly analysis of the threats, vulnerabilities, and defensive innovations shaping AI security. Written for security engineers and CTOs who need signal, not hype. Browse the archive below or [subscribe](/subscribe/) for the latest.

---

## Archive

{% assign newsletters = site.newsletters | sort: 'date' | reverse %}
{% if newsletters.size > 0 %}
{% for newsletter in newsletters %}

  <div class="card mb-3">
    <div class="card-body">
      <h5 class="card-title">
        <a href="{{ newsletter.url }}">{{ newsletter.title }}</a>
      </h5>
      {% if newsletter.subtitle %}
      <p class="card-text text-muted">{{ newsletter.subtitle }}</p>
      {% endif %}
      <div class="d-flex justify-content-between align-items-center">
        <small class="text-muted">
          Issue #{{ newsletter.issue }} • {{ newsletter.date | date: '%B %d, %Y' }}
          {% if newsletter.reading_time %} • {{ newsletter.reading_time }} min read{% endif %}
        </small>
        <a href="{{ newsletter.url }}" class="btn btn-sm btn-primary">Read</a>
      </div>
    </div>
  </div>
  {% endfor %}
{% else %}
  <div class="alert alert-info">
    <h4>Coming Soon!</h4>
    <p>I'm preparing amazing cybersecurity content for you. Check back soon!</p>
  </div>
{% endif %}

---

## Subscribe

AI security analysis in your inbox, every week. No spam.

<a href="/subscribe/" class="btn btn-primary btn-lg">
  <i class="fas fa-envelope me-2"></i>Subscribe — it's free
</a>
