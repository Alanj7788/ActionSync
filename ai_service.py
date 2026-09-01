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
4. Identify priority if explicitly mentioned.
5. Extract important follow-up activities.
6. Never invent an owner or deadline.
7. If information is missing, use "Not specified".
8. If a priority is mentioned separately but clearly refers
   to a task, associate that priority with the correct task.

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
                "Priority": item.priority,
                "Follow-up": item.follow_up,
                "Status": "Not Started",
            }
        )

    return task_data