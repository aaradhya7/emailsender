
import time
from pathlib import Path
from datetime import datetime

from agent.reader import read_task
from agent.writer import write_email
from gmail.auth import get_gmail_service
from gmail.sender import send_email

from gmail.monitor import get_new_emails
from gmail.reader import parse_email
from agent.analyzer import analyze_email


BASE_DIR = Path(__file__).resolve().parent
TASK_FILE = BASE_DIR / "task.txt"
SUMMARY_FILE = BASE_DIR / "summarize.txt"

CHECK_INTERVAL = 30


def send_task_email(service):
    """Read task.txt, draft an email, and ask for approval."""

    if not TASK_FILE.exists() or not TASK_FILE.read_text(
        encoding="utf-8"
    ).strip():
        print("\ntask.txt is empty or missing. Skipping outbound email.")
        return

    print("\nReading task.txt...")
    task = read_task()

    print("AI is writing your email...")
    email_data = write_email(task)

    recipient = email_data.get("recipient", "").strip()
    subject = email_data.get("subject", "").strip()
    body = email_data.get("body", "").strip()

    if not recipient or "@" not in recipient:
        print("Invalid or missing recipient. Skipping email.")
        return

    if not subject or not body:
        print("Email subject or body is missing. Skipping email.")
        return

    print("\n" + "=" * 50)
    print("EMAIL DRAFT")
    print("=" * 50)
    print("To:", recipient)
    print("Subject:", subject)
    print("\nBody:\n", body)
    print("=" * 50)

    while True:
        approval = input("\nSend this email? (YES/NO): ").strip().upper()

        if approval in ("YES", "NO"):
            break

        print("Please type YES or NO.")

    if approval == "NO":
        print("Email not sent.")
        return

    result = send_email(service, recipient, subject, body)
    print("Email sent successfully!")
    print("Gmail message ID:", result.get("id", ""))


def save_summary(email, analysis):
    """Append one analyzed email to summarize.txt."""

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    actions = analysis.get("action_items", [])
    if isinstance(actions, list):
        actions_text = "\n".join(f"- {item}" for item in actions)
    else:
        actions_text = str(actions)

    tech_stack = analysis.get("tech_stack", [])
    if isinstance(tech_stack, list):
        tech_text = ", ".join(str(item) for item in tech_stack) or "Not mentioned"
    else:
        tech_text = str(tech_stack) or "Not mentioned"

    deadline = analysis.get("deadline") or "Not mentioned"

    content = f"""
{'=' * 65}
EMAIL RECEIVED: {timestamp}
{'=' * 65}
From: {email.get("sender", "Unknown")}
Subject: {email.get("subject", "No subject")}

SUMMARY:
{analysis.get("summary", "No summary available")}

ACTION ITEMS:
{actions_text or "No action items identified"}

TECH STACK:
{tech_text}

DEADLINE:
{deadline}

PRIORITY:
{analysis.get("priority", "Not specified")}

REPLY REQUIRED:
{analysis.get("reply_required", "Not specified")}

"""

    with SUMMARY_FILE.open("a", encoding="utf-8") as file:
        file.write(content)

    print(f"Summary saved to: {SUMMARY_FILE}")


def monitor_incoming_emails(service):
    """Poll trusted unread emails until Ctrl+C."""

    print("\n" + "=" * 50)
    print("INCOMING EMAIL MONITOR STARTED")
    print(f"Checking every {CHECK_INTERVAL} seconds.")
    print("Press Ctrl+C to stop.")
    print("=" * 50)

    processed_ids = set()

    while True:
        try:
            messages = get_new_emails(service)

            new_messages = [
                msg for msg in messages
                if msg.get("id") not in processed_ids
            ]

            if not new_messages:
                print(
                    f"[{datetime.now().strftime('%H:%M:%S')}] "
                    "No new trusted unread emails."
                )

            for message in new_messages:
                email = parse_email(message)
                email_id = email.get("email_id")

                print("\nNew email found!")
                print("From:", email.get("sender"))
                print("Subject:", email.get("subject"))

                try:
                    analysis = analyze_email(
                        email["sender"],
                        email["subject"],
                        email["body"]
                    )

                    save_summary(email, analysis)
                    processed_ids.add(email_id)

                except Exception as error:
                    print("Could not analyze this email:", error)

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            raise

        except Exception as error:
            print("Monitor error:", error)
            print(f"Retrying in {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)


def main():
    print("=" * 50)
    print("AI EMAIL AGENT")
    print("=" * 50)

    service = get_gmail_service()

    # First: outbound task approval
    try:
        send_task_email(service)
    except Exception as error:
        print("Outbound email error:", error)
        print("Continuing to incoming email monitoring...")

    # Then: continuous incoming email monitoring
    try:
        monitor_incoming_emails(service)
    except KeyboardInterrupt:
        print("\nCtrl+C detected.")
        print("Email monitor stopped. Goodbye!")


if __name__ == "__main__":
    main()