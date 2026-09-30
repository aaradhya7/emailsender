
import base64

def get_body(payload):
    if "parts" in payload:
        for part in payload["parts"]:
            result = get_body(part)
            if result:
                return result

    if payload.get("mimeType") == "text/plain":
        data = payload.get("body", {}).get("data")
        if data:
            return base64.urlsafe_b64decode(
                data + "=="
            ).decode("utf-8", errors="replace")

    return ""