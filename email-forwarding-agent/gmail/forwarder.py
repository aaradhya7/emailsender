
import base64
from email.mime.text import MIMEText

def forward_email(service, recipient, email):
    message = MIMEText(
        f"Forwarded message\n\n"
        f"From: {email['sender']}\n"
        f"Subject: {email['subject']}\n\n"
        f"{email['body']}"
    )

    message["to"] = recipient
    message["subject"] = "Fwd: " + email["subject"]

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    return service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()