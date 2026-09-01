from pydantic import BaseModel


class ActionItem(BaseModel):
    task: str
    owner: str
    deadline: str
    follow_up: str


class MeetingActions(BaseModel):
    action_items: list[ActionItem]