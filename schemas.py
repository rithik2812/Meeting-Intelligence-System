from typing import List, Optional
from pydantic import BaseModel, Field


class MeetingSummary(BaseModel):
    title: str = Field(description="Short meeting title")
    summary: str = Field(description="Concise meeting summary")
    key_points: List[str] = Field(
        description="Important discussion points"
    )
    decisions: List[str] = Field(
        description="Decisions explicitly made during the meeting"
    )


class ActionItem(BaseModel):
    task: str = Field(description="Specific action to complete")
    owner: Optional[str] = Field(
        default=None,
        description="Person responsible for the task"
    )
    status: str = Field(default="Pending")


class TaskExtraction(BaseModel):
    action_items: List[ActionItem]


class DeadlineItem(BaseModel):
    task: str
    owner: Optional[str] = None
    deadline: Optional[str] = None
    original_reference: str = Field(
        description="Exact deadline phrase from the transcript"
    )
    confidence: str = Field(
        description="High, Medium or Low"
    )


class DeadlineExtraction(BaseModel):
    deadlines: List[DeadlineItem]


class FollowUpEmail(BaseModel):
    subject: str
    body: str
