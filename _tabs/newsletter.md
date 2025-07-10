---
layout: page
title: Newsletter
icon: fas fa-envelope
order: 3
---

# 📧 Cybersecurity Newsletter

Welcome to my daily cybersecurity newsletter! Here you'll find the latest security insights, threat analysis, and actionable tips.

## Newsletter Archive

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

Want to get these insights delivered to your inbox?

{% if site.newsletter_signup_url %}
<a href="{{ site.newsletter_signup_url }}" class="btn btn-primary btn-lg">
<i class="fas fa-envelope me-2"></i>Subscribe Now
</a>
{% else %}

<p><em>Subscription link coming soon!</em></p>
{% endif %}
