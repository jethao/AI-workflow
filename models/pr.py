from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class PRStatus(str, Enum):
    DRAFT = "draft"
    OPEN = "open"
    APPROVED = "approved"
    CHANGES_REQUESTED = "changes_requested"
    MERGED = "merged"
    CLOSED = "closed"


class ReviewComment(BaseModel):
    """Code review comment"""
    file_path: str
    line_number: Optional[int] = None
    comment: str
    severity: str = "info"  # info, warning, error


class PullRequest(BaseModel):
    """Pull Request model"""
    id: str
    title: str
    description: str
    task_id: str
    branch_name: str
    files_changed: List[str] = Field(default_factory=list)
    test_results: Optional[str] = None
    status: PRStatus = PRStatus.DRAFT
    review_comments: List[ReviewComment] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
