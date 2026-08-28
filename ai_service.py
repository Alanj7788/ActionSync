from google import genai

from config import GEMINI_MODEL
from models import MeetingActions


def extract_action_items(meeting_notes):

    client = genai.Client()

    prompt = f"""
You are an AI meeting assistant.

Analyze the following meeting notes and extract all actionable items.

For each action item:

1. Identify the task.
2. Identify the responsible person or team.
3. Extract the deadline if mentioned.
4. Identify priority if explicitly mentioned.
5. Extract important follow-up activities.
6. Never invent an owner or deadline.
7. If information is missing, use "Not specified".
8. If a priority is mentioned separately but clearly refers
   to a task, associate that priority with the correct task.

Meeting notes:

{meeting_notes}
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": MeetingActions,
        }
    )

    results = response.parsed

    task_data = []

    for item in results.action_items:

        task_data.append(
            {
                "Task": item.task,
                "Owner": item.owner,
                "Deadline": item.deadline,
                "Priority": item.priority,
                "Follow-up": item.follow_up,
                "Status": "Not Started",
            }
        )

    return task_data