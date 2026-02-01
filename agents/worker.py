import os
from typing import Dict, List
from models.ticket import Task
from utils.claude_client import ClaudeClient
from utils.file_handler import FileHandler


class WorkerAgent:
    """
    Worker Agent - Reads tickets and implements in Python
    """

    def __init__(self, claude_client: ClaudeClient, workspace_dir: str = "./workspace"):
        self.claude = claude_client
        self.file_handler = FileHandler()
        self.workspace_dir = workspace_dir
        self.file_handler.ensure_dir(workspace_dir)

    def implement_task(self, task: Task) -> Dict[str, str]:
        """
        Implement a task in Python

        Args:
            task: Task to implement

        Returns:
            Dictionary mapping file paths to their content
        """
        system_prompt = """You are an expert Python developer. Your task is to implement the given feature according to specifications.

Guidelines:
- Write clean, maintainable, and well-documented Python code
- Follow PEP 8 style guidelines
- Include type hints
- Write comprehensive docstrings
- Consider edge cases and error handling
- Make the code production-ready

Respond with a JSON object:
{
  "files": [
    {
      "path": "relative/path/to/file.py",
      "content": "file content here"
    }
  ],
  "implementation_notes": "Any important notes about the implementation"
}"""

        user_prompt = f"""Implement the following task:

Task ID: {task.id}
Title: {task.title}
Description: {task.description}

Feature Requirements:
{task.feature_requirements}

Test Requirements:
{task.test_requirements}

Success Metrics:
{chr(10).join(f"- {metric}" for metric in task.success_metrics)}

Pass/Fail Criteria:
{chr(10).join(f"- {criteria}" for criteria in task.pass_fail_criteria)}

Please provide complete Python implementation with all necessary files."""

        response = self.claude.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=8000
        )

        # Parse the response
        import json
        try:
            impl_data = json.loads(response)
            files = {}

            for file_info in impl_data.get("files", []):
                file_path = file_info["path"]
                content = file_info["content"]
                files[file_path] = content

            return files

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse implementation response as JSON: {e}\nResponse: {response}")

    def save_implementation(self, files: Dict[str, str], task_id: str) -> List[str]:
        """
        Save implemented files to workspace

        Args:
            files: Dictionary mapping file paths to content
            task_id: Task ID for organizing files

        Returns:
            List of saved file paths
        """
        task_dir = os.path.join(self.workspace_dir, task_id)
        self.file_handler.ensure_dir(task_dir)

        saved_paths = []
        for rel_path, content in files.items():
            full_path = os.path.join(task_dir, rel_path)
            self.file_handler.save_text(content, full_path)
            saved_paths.append(full_path)

        return saved_paths

    def implement_and_save(self, task: Task) -> Dict[str, any]:
        """
        Implement task and save to workspace

        Args:
            task: Task to implement

        Returns:
            Dictionary with implementation details
        """
        print(f"Implementing task: {task.id} - {task.title}")

        files = self.implement_task(task)
        saved_paths = self.save_implementation(files, task.id)

        return {
            "task_id": task.id,
            "files": saved_paths,
            "status": "implemented"
        }
