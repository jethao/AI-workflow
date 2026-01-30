from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime


class ComponentDesign(BaseModel):
    """Individual component design"""
    name: str
    purpose: str
    responsibilities: List[str]
    interfaces: List[str]
    dependencies: List[str] = Field(default_factory=list)


class StateTransition(BaseModel):
    """State machine transition"""
    from_state: str
    to_state: str
    trigger: str
    condition: Optional[str] = None
    action: Optional[str] = None


class StateMachine(BaseModel):
    """State machine design"""
    name: str
    description: str
    states: List[str]
    initial_state: str
    final_states: List[str]
    transitions: List[StateTransition]
    example_flow: str


class DataPath(BaseModel):
    """Data flow path through the system"""
    name: str
    description: str
    steps: List[str]
    data_transformations: List[str]
    example: str


class ControlPath(BaseModel):
    """Control flow path through the system"""
    name: str
    description: str
    sequence: List[str]
    decision_points: List[str]
    error_handling: List[str]
    example: str


class CallStackFrame(BaseModel):
    """Call stack frame"""
    function: str
    parameters: Dict[str, str]
    returns: str
    description: str


class CallStack(BaseModel):
    """Call stack design for typical operation"""
    operation: str
    description: str
    stack_frames: List[CallStackFrame]
    example: str


class APIEndpoint(BaseModel):
    """Detailed API endpoint design"""
    method: str
    path: str
    description: str
    request_body: Optional[Dict[str, Any]] = None
    request_params: Optional[Dict[str, str]] = None
    response_success: Dict[str, Any]
    response_error: Dict[str, Any]
    authentication: Optional[str] = None
    example_request: str
    example_response: str


class DesignExample(BaseModel):
    """Design example demonstrating usage"""
    title: str
    description: str
    scenario: str
    code_example: str
    expected_output: str


class Design(BaseModel):
    """Architecture Design Document model"""

    title: str = Field(..., description="Design title")
    overview: str = Field(..., description="High-level overview")
    architecture_pattern: str = Field(..., description="Architectural pattern (e.g., MVC, microservices)")

    # Components
    components: List[ComponentDesign] = Field(default_factory=list, description="System components")

    # State Machines
    state_machines: List[StateMachine] = Field(default_factory=list, description="State machine designs")

    # Data Paths
    data_paths: List[DataPath] = Field(default_factory=list, description="Data flow paths")

    # Control Paths
    control_paths: List[ControlPath] = Field(default_factory=list, description="Control flow paths")

    # Call Stacks
    call_stacks: List[CallStack] = Field(default_factory=list, description="Call stack designs")

    # APIs
    api_endpoints: List[APIEndpoint] = Field(default_factory=list, description="Detailed API endpoints")

    # Data Models
    data_models: List[str] = Field(default_factory=list, description="Data models needed")

    # Examples
    examples: List[DesignExample] = Field(default_factory=list, description="Usage examples")

    # Technical Details
    tech_stack: Dict[str, str] = Field(default_factory=dict, description="Technology stack")
    security_considerations: List[str] = Field(default_factory=list)
    scalability_considerations: List[str] = Field(default_factory=list)

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now)
    human_reviewed: bool = Field(default=False, description="Whether human has reviewed this design")
    review_notes: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "title": "User Authentication System Design",
                "overview": "JWT-based authentication with refresh tokens",
                "architecture_pattern": "Layered Architecture",
                "components": [],
                "state_machines": [],
                "data_paths": [],
                "control_paths": [],
                "call_stacks": [],
                "api_endpoints": [],
                "examples": [],
                "tech_stack": {"backend": "Python/FastAPI", "database": "PostgreSQL"},
                "human_reviewed": True
            }
        }
