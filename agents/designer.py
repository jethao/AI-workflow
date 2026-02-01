import json
from typing import Dict, Any
from models.prd import PRD
from models.design import Design, ComponentDesign
from utils.claude_client import ClaudeClient
from utils.file_handler import FileHandler


class DesignerAgent:
    """
    Designer Agent - Reads PRD and designs architecture for products or features
    """

    def __init__(self, claude_client: ClaudeClient):
        self.claude = claude_client
        self.file_handler = FileHandler()

    def design_from_prd(self, prd: PRD) -> Design:
        """
        Read PRD and create comprehensive architecture design

        Args:
            prd: Product Requirement Document

        Returns:
            Design document with state machines, data paths, control paths, call stacks, APIs, and examples
        """
        system_prompt = """You are an expert software architect. Your task is to read a Product Requirement Document (PRD) and design a comprehensive architecture.

Create a detailed design including:
1. Architecture pattern and component breakdown
2. State machines for stateful components
3. Data flow paths showing how data moves through the system
4. Control flow paths showing execution flow
5. Call stacks for typical operations
6. Detailed API endpoint specifications
7. Practical examples demonstrating usage

Respond with a JSON object matching this structure:
{
  "title": "string",
  "overview": "string",
  "architecture_pattern": "string",
  "components": [
    {
      "name": "string",
      "purpose": "string",
      "responsibilities": ["string"],
      "interfaces": ["string"],
      "dependencies": ["string"]
    }
  ],
  "state_machines": [
    {
      "name": "string",
      "description": "string",
      "states": ["state1", "state2"],
      "initial_state": "state1",
      "final_states": ["state2"],
      "transitions": [
        {
          "from_state": "state1",
          "to_state": "state2",
          "trigger": "event",
          "condition": "optional condition",
          "action": "optional action"
        }
      ],
      "example_flow": "Detailed example of state transitions"
    }
  ],
  "data_paths": [
    {
      "name": "string",
      "description": "string",
      "steps": ["step1", "step2"],
      "data_transformations": ["transformation1"],
      "example": "Example showing data flow"
    }
  ],
  "control_paths": [
    {
      "name": "string",
      "description": "string",
      "sequence": ["step1", "step2"],
      "decision_points": ["decision1"],
      "error_handling": ["error_handler1"],
      "example": "Example showing control flow"
    }
  ],
  "call_stacks": [
    {
      "operation": "string",
      "description": "string",
      "stack_frames": [
        {
          "function": "function_name",
          "parameters": {"param": "type"},
          "returns": "return_type",
          "description": "what this function does"
        }
      ],
      "example": "Example call stack trace"
    }
  ],
  "api_endpoints": [
    {
      "method": "GET|POST|PUT|DELETE",
      "path": "/api/resource",
      "description": "string",
      "request_body": {"field": "type"},
      "request_params": {"param": "description"},
      "response_success": {"field": "value"},
      "response_error": {"error": "message"},
      "authentication": "Bearer token|API key|None",
      "example_request": "curl example or code snippet",
      "example_response": "JSON response example"
    }
  ],
  "data_models": ["model1", "model2"],
  "examples": [
    {
      "title": "string",
      "description": "string",
      "scenario": "string",
      "code_example": "code snippet",
      "expected_output": "output"
    }
  ],
  "tech_stack": {"category": "technology"},
  "security_considerations": ["string"],
  "scalability_considerations": ["string"]
}

IMPORTANT: Include at least 2-3 examples showing real usage scenarios."""

        user_prompt = f"""Design the architecture for the following PRD:

Title: {prd.title}
Level: {prd.level}
Description: {prd.description}

Objectives:
{chr(10).join(f"- {obj}" for obj in prd.objectives)}

User Stories:
{chr(10).join(f"- {story}" for story in prd.user_stories)}

Requirements:
{chr(10).join(f"- {req}" for req in prd.requirements)}

Success Metrics:
{chr(10).join(f"- {metric}" for metric in prd.success_metrics)}

Constraints:
{chr(10).join(f"- {constraint}" for constraint in (prd.constraints or []))}

Please provide a detailed architecture design."""

        response = self.claude.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=4096
        )

        # Parse the JSON response
        try:
            design_data = json.loads(response)

            # Parse components
            components = [
                ComponentDesign(**comp) for comp in design_data.get("components", [])
            ]

            # Parse state machines
            from models.design import StateMachine, StateTransition
            state_machines = []
            for sm_data in design_data.get("state_machines", []):
                transitions = [
                    StateTransition(**trans) for trans in sm_data.get("transitions", [])
                ]
                state_machine = StateMachine(
                    name=sm_data["name"],
                    description=sm_data["description"],
                    states=sm_data["states"],
                    initial_state=sm_data["initial_state"],
                    final_states=sm_data["final_states"],
                    transitions=transitions,
                    example_flow=sm_data["example_flow"]
                )
                state_machines.append(state_machine)

            # Parse data paths
            from models.design import DataPath
            data_paths = [
                DataPath(**dp) for dp in design_data.get("data_paths", [])
            ]

            # Parse control paths
            from models.design import ControlPath
            control_paths = [
                ControlPath(**cp) for cp in design_data.get("control_paths", [])
            ]

            # Parse call stacks
            from models.design import CallStack, CallStackFrame
            call_stacks = []
            for cs_data in design_data.get("call_stacks", []):
                frames = [
                    CallStackFrame(**frame) for frame in cs_data.get("stack_frames", [])
                ]
                call_stack = CallStack(
                    operation=cs_data["operation"],
                    description=cs_data["description"],
                    stack_frames=frames,
                    example=cs_data["example"]
                )
                call_stacks.append(call_stack)

            # Parse API endpoints
            from models.design import APIEndpoint
            api_endpoints = [
                APIEndpoint(**api) for api in design_data.get("api_endpoints", [])
            ]

            # Parse examples
            from models.design import DesignExample
            examples = [
                DesignExample(**ex) for ex in design_data.get("examples", [])
            ]

            design = Design(
                title=design_data["title"],
                overview=design_data["overview"],
                architecture_pattern=design_data["architecture_pattern"],
                components=components,
                state_machines=state_machines,
                data_paths=data_paths,
                control_paths=control_paths,
                call_stacks=call_stacks,
                api_endpoints=api_endpoints,
                data_models=design_data.get("data_models", []),
                examples=examples,
                tech_stack=design_data.get("tech_stack", {}),
                security_considerations=design_data.get("security_considerations", []),
                scalability_considerations=design_data.get("scalability_considerations", [])
            )

            return design
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse design response as JSON: {e}\nResponse: {response}")

    def save_design(self, design: Design, output_path: str) -> None:
        """Save design to file"""
        self.file_handler.save_json(design.model_dump(), output_path)

    def load_design(self, input_path: str) -> Design:
        """Load design from file"""
        data = self.file_handler.load_json(input_path)
        return Design(**data)
