
RECIPIENTS = {
    "hr": "hr@company.com",
    "technical": "devops@company.com",
    "finance": "finance@company.com",
    "business": "sales@company.com"
}

def get_recipient(category, confidence):
    if confidence < 0.90:
        return None

    return RECIPIENTS.get(category)