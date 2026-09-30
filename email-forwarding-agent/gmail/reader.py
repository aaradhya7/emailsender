
import base64


def get_header(headers, name):
    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", "")
    return ""


def decode_body(data):
    if not data:
        return ""

    decoded = base64.urlsafe_b64decode(
        data + "=" * (-len(data) % 4)
    )
    return decoded.decode("utf-8", errors="replace")


def extract_body(payload):
    mime_type = payload.get("mimeType", "")

    if mime_type == "text/plain":
        data = payload.get("body", {}).get("data")
        return decode_body(data)

    parts = payload.get("parts", [])

    # Prefer plain text parts
    for part in parts:
        if part.get("mimeType") == "text/plain":
            data = part.get("body", {}).get("data")
            if data:
                return decode_body(data)

    # Check nested multipart messages
    for part in parts:
        text = extract_body(part)
        if text:
            return text

    # Fallback to the current payload body
    data = payload.get("body", {}).get("data")
    return decode_body(data)


def parse_email(message):
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    return {
        "email_id": message.get("id", ""),
        "sender": get_header(headers, "From"),
        "subject": get_header(headers, "Subject"),
        "body": extract_body(payload),
    }