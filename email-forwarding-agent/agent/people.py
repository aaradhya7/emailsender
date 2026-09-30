
from pathlib import Path

EMAILS_FILE = (
    Path(__file__).resolve().parent.parent
    / "trusted_emails.txt"
)


def get_trusted_senders():
    if not EMAILS_FILE.exists():
        raise FileNotFoundError(
            "trusted_emails.txt file not found!"
        )

    emails = EMAILS_FILE.read_text(
        encoding="utf-8"
    ).splitlines()

    return {
        email.strip().lower()
        for email in emails
        if email.strip() and not email.strip().startswith("#")
    }