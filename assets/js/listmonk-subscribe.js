/* Newsletter subscription via n8n → beehiiv */
(function () {
  const N8N_WEBHOOK_URL = 'https://n8n.lab.aminrj.com/webhook/subscribe';

  const FORMS = [
    { formId: 'subscribe-form',         msgId: 'subscribe-message' },
    { formId: 'subscribe-form-sidebar', msgId: 'subscribe-message-sidebar' },
    { formId: 'post-subscribe-form',    msgId: 'post-subscribe-message' },
    { formId: 'post-cta-form',          msgId: 'post-cta-message' },
  ];

  function getUTMParams(form) {
    const p = new URLSearchParams(window.location.search);
    // Hidden fields in the form take priority over URL params
    const fromField = (name) => {
      const el = form ? form.querySelector('[name="' + name + '"]') : null;
      return (el && el.type === 'hidden') ? el.value : null;
    };
    return {
      utm_source:   fromField('utm_source')   || p.get('utm_source')   || '',
      utm_medium:   fromField('utm_medium')   || p.get('utm_medium')   || '',
      utm_campaign: fromField('utm_campaign') || p.get('utm_campaign') || '',
    };
  }

  function showMessage(el, text, type) {
    el.textContent = text;
    el.className = 'form-message ' + type;
  }

  function wireForm({ formId, msgId }) {
    const form = document.getElementById(formId);
    const msgEl = document.getElementById(msgId);
    if (!form || !msgEl) return;

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email   = (form.querySelector('[name="email"]')   || {}).value || '';
      const name    = (form.querySelector('[name="name"]')    || {}).value || '';
      const source  = (form.querySelector('[name="source"]')  || {}).value || 'aminrj';
      const submitBtn = form.querySelector('button[type="submit"]');

      submitBtn.disabled = true;
      const origText = submitBtn.textContent;
      submitBtn.textContent = 'Subscribing…';

      try {
        const res = await fetch(N8N_WEBHOOK_URL, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, name, source, ...getUTMParams(form) }),
        });

        const data = await res.json();

        if (data.success) {
          showMessage(msgEl, '✓ Welcome! Check your inbox.', 'success');
          form.reset();
          // Plausible analytics
          if (typeof window.trackNewsletterSignup === 'function') {
            window.trackNewsletterSignup();
          }
        } else {
          showMessage(msgEl, data.message || 'Please try again.', 'error');
        }
      } catch (err) {
        showMessage(msgEl, 'Connection error. Please try again.', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = origText;
      }
    });
  }

  document.addEventListener('DOMContentLoaded', () => {
    FORMS.forEach(wireForm);
  });
}());
