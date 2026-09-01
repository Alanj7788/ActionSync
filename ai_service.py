from ollama import chat

from config import OLLAMA_MODEL
from models import MeetingActions


def extract_action_items(meeting_notes):

    prompt = f"""
You are an AI meeting assistant.

Analyze the following meeting notes and extract all actionable items.

For each action item:

1. Identify the task.
2. Identify the responsible person or team.
3. Extract the deadline if mentioned.
4. Extract important follow-up activities.
5. Never invent an owner or deadline.
6. If information is missing, use "Not specified".

Return the result strictly according to the provided JSON schema.

Meeting notes:

{meeting_notes}
"""

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        format=MeetingActions.model_json_schema(),
        options={
            "temperature": 0
        }
    )

    results = MeetingActions.model_validate_json(
        response.message.content
    )

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