
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import json

load_dotenv()

llm = ChatGroq(
    model="qwen/qwen3.8-27b",
    temperature=0.4,
    api_key=os.getenv("GROQ_API_KEY")
)


def write_email(task):
    prompt = f"""
You are a professional email writing assistant.

Read the user's task carefully and write an email
that matches the recipient, purpose, context, and tone.

Rules:
- Be respectful, natural, and professional.
- Create a suitable subject.
- Do not invent facts, qualifications, or achievements.
- Do not send the email.
- Extract the recipient email exactly as provided.
- If the recipient is missing, return an empty string.
- Return ONLY valid JSON, without markdown fences.

Required format:
{{
    "recipient": "email address",
    "subject": "email subject",
    "body": "email body"
}}

User's task:
{task}
"""

    response = llm.invoke(prompt)
    content = response.content.strip()

    # Remove markdown code fences if the model adds them
    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        content = content.rsplit("```", 1)[0].strip()

    # Validate JSON before returning it
    email_data = json.loads(content)

    return email_data