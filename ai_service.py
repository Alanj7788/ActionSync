from openai import OpenAI

from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_MODEL
)

from models import MeetingActions


client = OpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    base_url=(
        f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}"
        "/openai/v1/"
    )
)


def extract_action_items(meeting_notes):

    completion = client.beta.chat.completions.parse(
        model=AZURE_OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": """
You are an AI meeting assistant.

Your job is to analyze meeting conversations
and extract all actionable items.

For each action item:

1. Identify the task.
2. Identify the responsible person or team.
3. Extract the deadline if mentioned.
4. Extract important follow-up activities.
5. Never invent an owner or deadline.
6. If information is missing, use
   "Not specified".

Return only information supported by
the meeting conversation.
"""
            },
            {
                "role": "user",
                "content": meeting_notes
            }
        ],
        response_format=MeetingActions
    )

    results = completion.choices[
        0
    ].message.parsed

    task_data = []

    for item in results.action_items:

        task_data.append(
            {
                "Task": item.task,
                "Owner": item.owner,
                "Deadline": item.deadline,
                "Follow-up": item.follow_up
            }
        )

    return task_data