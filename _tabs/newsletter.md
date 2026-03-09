---
layout: page
title: Newsletter
icon: fas fa-envelope
order: 3
---

# AI Security Intelligence Digest

<div class="text-center my-4">
  <a href="https://newsletter.aminrj.com" target="_blank" rel="noopener noreferrer" class="btn btn-primary btn-lg px-5">
    <i class="fas fa-external-link-alt me-2"></i>Read Here
  </a>
  <p class="text-muted small mt-2">newsletter.aminrj.com</p>
</div>

Weekly analysis of the threats, vulnerabilities, and defensive innovations shaping AI security. Written for security engineers and CTOs who need signal, not hype. New issues publish every week at [newsletter.aminrj.com](https://newsletter.aminrj.com){:target="_blank"}.

---

## Archive

_Earlier issues published before the move to Beehiiv._

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
