
from agent.people import get_trusted_senders


def get_new_emails(service):
    trusted = get_trusted_senders()

    if not trusted:
        print("No trusted senders configured.")
        return []

    results = service.users().messages().list(
        userId="me",
        q="is:unread",
        maxResults=50
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for message in messages:
        msg = service.users().messages().get(
            userId="me",
            id=message["id"],
            format="full"
        ).execute()

        headers = msg.get("payload", {}).get(
            "headers", []
        )

        sender = ""
        for header in headers:
            if header.get("name", "").lower() == "from":
                sender = header.get("value", "")
                break

        # Match the sender's email address
        import re
        match = re.search(r"<([^>]+)>", sender)
        sender_email = (
            match.group(1) if match else sender
        ).strip().lower()

        if sender_email in trusted:
            msg["sender_email"] = sender_email
            emails.append(msg)

    return emails