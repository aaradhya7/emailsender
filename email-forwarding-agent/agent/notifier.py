
from gmail.sender import send_email


def notify_user(service, analysis, original_subject):
    summary = analysis.get("summary", "")
    actions = analysis.get("action_items", [])
    tech = analysis.get("tech_stack", [])
    deadline = analysis.get("deadline") or "Not specified"
    priority = analysis.get("priority", "Not specified")
    reply = analysis.get("reply_required", False)

    body = f"""
Your AI Email Agent analyzed a new email.

Original subject:
{original_subject}

SUMMARY:
{summary}

ACTION ITEMS:
"""

    if actions:
        for i, action in enumerate(actions, start=1):
            body += f"{i}. {action}\n"
    else:
        body += "No action items identified.\n"

    body += f"""

TECH STACK:
{", ".join(tech) if tech else "Not specified"}

DEADLINE:
{deadline}

PRIORITY:
{priority}

REPLY REQUIRED:
{"Yes" if reply else "Not identified"}
"""

    # Set this to your own Gmail address
    my_email = "arsharma478@gmail.com"

    result = send_email(
        service,
        my_email,
        f"AI Email Summary: {original_subject}",
        body
    )

    return result