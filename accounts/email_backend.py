"""
Custom Django email backend using the Brevo (ex-Sendinblue) Transactional Email API.

No domain ownership required — just verify a sender email address in Brevo.
Uses plain HTTPS (no SMTP ports), so works on Vercel without any issues.
"""

import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

BREVO_API_URL = "https://api.brevo.com/v3/smtp/email"


class BrevoEmailBackend(BaseEmailBackend):
    """Send emails via the Brevo HTTP API (no SMTP port required)."""

    def send_messages(self, email_messages):
        api_key = settings.BREVO_API_KEY
        num_sent = 0

        for message in email_messages:
            try:
                payload = {
                    "sender": {
                        "name": settings.DEFAULT_FROM_NAME,
                        "email": message.from_email,
                    },
                    "to": [{"email": addr} for addr in message.to],
                    "subject": message.subject,
                    "textContent": message.body,
                }

                # Include HTML alternative if present
                for content, mimetype in getattr(message, "alternatives", []):
                    if mimetype == "text/html":
                        payload["htmlContent"] = content
                        break

                response = requests.post(
                    BREVO_API_URL,
                    json=payload,
                    headers={
                        "api-key": api_key,
                        "Content-Type": "application/json",
                    },
                    timeout=10,
                )
                response.raise_for_status()
                num_sent += 1

            except Exception as exc:  # noqa: BLE001
                if not self.fail_silently:
                    raise exc

        return num_sent
