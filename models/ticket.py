from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class TicketStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    DONE = "done"


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Task(BaseModel):
    """Implementation task"""
    id: str
    title: str
    description: str
    feature_requirements: str
    test_requirements: str
    success_metrics: List[str]
    pass_fail_criteria: List[str]
    status: TicketStatus = TicketStatus.TODO
    priority: TicketPriority = TicketPriority.MEDIUM
    story_id: Optional[str] = None
    estimated_effort: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class Story(BaseModel):
    """Feature story"""
    id: str
    title: str
    description: str
    acceptance_criteria: List[str]
    tasks: List[Task] = Field(default_factory=list)
    status: TicketStatus = TicketStatus.TODO
    priority: TicketPriority = TicketPriority.MEDIUM
    epic_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)


class Epic(BaseModel):
    """Product epic"""
    id: str
    title: str
    description: str
    objectives: List[str]
    stories: List[Story] = Field(default_factory=list)
    status: TicketStatus = TicketStatus.TODO
    priority: TicketPriority = TicketPriority.MEDIUM
    created_at: datetime = Field(default_factory=datetime.now)
