from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PRD(BaseModel):
    """Product Requirement Document model"""

    title: str = Field(..., description="Title of the product or feature")
    description: str = Field(..., description="Detailed description")
    level: str = Field(..., description="Level: 'product' or 'feature'")
    objectives: List[str] = Field(default_factory=list, description="Key objectives")
    user_stories: List[str] = Field(default_factory=list, description="User stories")
    requirements: List[str] = Field(default_factory=list, description="Functional requirements")
    success_metrics: List[str] = Field(default_factory=list, description="Success criteria and metrics")
    constraints: Optional[List[str]] = Field(default_factory=list, description="Technical or business constraints")
    created_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "User Authentication System",
                "description": "Implement a secure user authentication system",
                "level": "feature",
                "objectives": ["Secure user login", "Password management"],
                "user_stories": ["As a user, I want to login securely"],
                "requirements": ["Email/password authentication", "JWT tokens"],
                "success_metrics": ["Login success rate > 99%"],
                "constraints": ["Must use industry-standard encryption"]
            }
        }
