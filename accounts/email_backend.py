"""
Custom Django email backend using the SendGrid Web API.

No domain ownership required — only a verified sender email address.
Uses HTTPS (no SMTP ports), compatible with Vercel.
Free tier: 100 emails/day.
"""

import json
import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend

SENDGRID_API_URL = "https://api.sendgrid.com/v3/mail/send"


class SendGridEmailBackend(BaseEmailBackend):
    """Send emails via the SendGrid Web API (no SMTP port required)."""

    def send_messages(self, email_messages):
        api_key = settings.SENDGRID_API_KEY
        num_sent = 0

        for message in email_messages:
            try:
                payload = {
                    "personalizations": [
                        {"to": [{"email": addr} for addr in message.to]}
                    ],
                    "from": {
                        "email": message.from_email,
                        "name": getattr(settings, "DEFAULT_FROM_NAME", "Koma Zmanî Kurdî"),
                    },
                    "subject": message.subject,
                    "content": [{"type": "text/plain", "value": message.body}],
                }

                # Include HTML alternative if present
                for content, mimetype in getattr(message, "alternatives", []):
                    if mimetype == "text/html":
                        payload["content"].append({"type": "text/html", "value": content})
                        break

                response = requests.post(
                    SENDGRID_API_URL,
                    data=json.dumps(payload),
                    headers={
                        "Authorization": f"Bearer {api_key}",
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
