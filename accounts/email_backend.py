"""
Custom Django email backend using the Resend API.

Drop-in replacement for Django's SMTP backend. All existing calls to
`send_mail()` / `EmailMessage.send()` work without any changes in views.
"""

import resend
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class ResendEmailBackend(BaseEmailBackend):
    """Send emails via the Resend HTTP API (no SMTP port required)."""

    def send_messages(self, email_messages):
        resend.api_key = settings.RESEND_API_KEY
        num_sent = 0

        for message in email_messages:
            try:
                payload = {
                    "from": message.from_email,
                    "to": list(message.to),
                    "subject": message.subject,
                    "text": message.body,
                }

                # Include HTML alternative if present
                for content, mimetype in getattr(message, "alternatives", []):
                    if mimetype == "text/html":
                        payload["html"] = content
                        break

                resend.Emails.send(payload)
                num_sent += 1

            except Exception as exc:  # noqa: BLE001
                if not self.fail_silently:
                    raise exc

        return num_sent
