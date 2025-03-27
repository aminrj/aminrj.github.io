document.addEventListener("DOMContentLoaded", () => {
  const forms = [
    { formId: "subscribe-form", msgId: "subscribe-message" },
    { formId: "subscribe-form-sidebar", msgId: "subscribe-message-sidebar" },
  ];

  forms.forEach(({ formId, msgId }) => {
    const form = document.getElementById(formId);
    const message = document.getElementById(msgId);
    if (!form || !message) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = form.email.value;
      const name = form.name.value;

      try {
        const res = await fetch("https://listmonk.tool.aminrj.com/api/public/subscription", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name,
            email,
            list_uuids: ["280513ac-ca2d-436c-87ff-2b3011845ff2"],
          })
        });

        const text = res.ok
          ? "🎉 You're subscribed!"
          : "⚠️ Subscription failed. Please try again.";
        message.textContent = text;
        message.style.color = res.ok ? "green" : "red";

        if (res.ok) form.reset();
      } catch (err) {
        message.textContent = "❌ Network error.";
        message.style.color = "red";
      }
    });
  });
});
