import json
from typing import List
from models.design import Design
from models.ticket import Epic, Story, Task, TicketPriority
from utils.claude_client import ClaudeClient
from utils.file_handler import FileHandler


class PlannerAgent:
    """
    Planner Agent - Reads design and breaks it down into Jira/Linear tickets
    Product -> Epic, Feature -> Story, Story -> Tasks
    """

    def __init__(self, claude_client: ClaudeClient):
        self.claude = claude_client
        self.file_handler = FileHandler()

    def create_tickets_from_design(self, design: Design) -> List[Epic]:
        """
        Break down design into hierarchical tickets

        Args:
            design: Architecture design document (assumed human-reviewed)

        Returns:
            List of Epics with nested Stories and Tasks
        """
        if not design.human_reviewed:
            print("Warning: Design has not been marked as human-reviewed")

        system_prompt = """You are a technical project manager. Your task is to break down an architecture design into detailed implementation tickets.

Structure:
- Epic: Represents the overall product/feature
- Story: Represents a specific feature component
- Task: Represents an implementation unit

Each ticket must include:
- Clear title and description
- Feature requirements
- Test requirements
- Success metrics
- Pass/fail criteria
- Priority level

Respond with a JSON object:
{
  "epics": [
    {
      "id": "EPIC-1",
      "title": "string",
      "description": "string",
      "objectives": ["string"],
      "priority": "high|medium|low",
      "stories": [
        {
          "id": "STORY-1",
          "title": "string",
          "description": "string",
          "acceptance_criteria": ["string"],
          "priority": "high|medium|low",
          "tasks": [
            {
              "id": "TASK-1",
              "title": "string",
              "description": "string",
              "feature_requirements": "string",
              "test_requirements": "string",
              "success_metrics": ["string"],
              "pass_fail_criteria": ["string"],
              "priority": "high|medium|low",
              "estimated_effort": "string"
            }
          ]
        }
      ]
    }
  ]
}"""

        user_prompt = f"""Break down the following architecture design into implementation tickets:

Title: {design.title}
Overview: {design.overview}
Architecture Pattern: {design.architecture_pattern}

Components:
{chr(10).join(f"- {comp.name}: {comp.purpose}" for comp in design.components)}

Data Models:
{chr(10).join(f"- {model}" for model in design.data_models)}

APIs:
{chr(10).join(f"- {api}" for api in design.apis)}

Tech Stack:
{chr(10).join(f"- {k}: {v}" for k, v in design.tech_stack.items())}

Create a comprehensive breakdown with Epics, Stories, and Tasks. Each task should be implementable independently."""

        response = self.claude.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.4,
            max_tokens=8000
        )

        # Parse the JSON response
        try:
            tickets_data = json.loads(response)
            epics = []

            for epic_data in tickets_data.get("epics", []):
                stories = []

                for story_data in epic_data.get("stories", []):
                    tasks = []

                    for task_data in story_data.get("tasks", []):
                        task = Task(
                            id=task_data["id"],
                            title=task_data["title"],
                            description=task_data["description"],
                            feature_requirements=task_data["feature_requirements"],
                            test_requirements=task_data["test_requirements"],
                            success_metrics=task_data["success_metrics"],
                            pass_fail_criteria=task_data["pass_fail_criteria"],
                            priority=TicketPriority(task_data.get("priority", "medium")),
                            story_id=story_data["id"],
                            estimated_effort=task_data.get("estimated_effort")
                        )
                        tasks.append(task)

                    story = Story(
                        id=story_data["id"],
                        title=story_data["title"],
                        description=story_data["description"],
                        acceptance_criteria=story_data["acceptance_criteria"],
                        tasks=tasks,
                        priority=TicketPriority(story_data.get("priority", "medium")),
                        epic_id=epic_data["id"]
                    )
                    stories.append(story)

                epic = Epic(
                    id=epic_data["id"],
                    title=epic_data["title"],
                    description=epic_data["description"],
                    objectives=epic_data["objectives"],
                    stories=stories,
                    priority=TicketPriority(epic_data.get("priority", "high"))
                )
                epics.append(epic)

            return epics

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse tickets response as JSON: {e}\nResponse: {response}")

    def save_tickets(self, epics: List[Epic], output_path: str) -> None:
        """Save tickets to file"""
        data = [epic.model_dump() for epic in epics]
        self.file_handler.save_json(data, output_path)

    def load_tickets(self, input_path: str) -> List[Epic]:
        """Load tickets from file"""
        data = self.file_handler.load_json(input_path)
        return [Epic(**epic_data) for epic_data in data]

    def get_all_tasks(self, epics: List[Epic]) -> List[Task]:
        """Extract all tasks from epics for easy access"""
        tasks = []
        for epic in epics:
            for story in epic.stories:
                tasks.extend(story.tasks)
        return tasks
