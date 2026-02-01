import json
import subprocess
from typing import Dict, List, Tuple
from models.ticket import Task
from models.pr import PullRequest, PRStatus
from utils.claude_client import ClaudeClient
from utils.file_handler import FileHandler


class DebuggerAgent:
    """
    Debugger Agent - Deploys code to test environment, runs tests, analyzes logs,
    fixes errors until all tests pass, then creates PR
    """

    def __init__(self, claude_client: ClaudeClient, workspace_dir: str = "./workspace"):
        self.claude = claude_client
        self.file_handler = FileHandler()
        self.workspace_dir = workspace_dir
        self.max_iterations = 5  # Maximum debug iterations

    def run_tests(self, task_dir: str) -> Tuple[bool, str]:
        """
        Run tests for implemented code

        Args:
            task_dir: Directory containing task implementation

        Returns:
            Tuple of (success, output)
        """
        try:
            # Look for test files
            result = subprocess.run(
                ["python", "-m", "pytest", task_dir, "-v"],
                capture_output=True,
                text=True,
                timeout=60
            )

            success = result.returncode == 0
            output = result.stdout + "\n" + result.stderr

            return success, output

        except subprocess.TimeoutExpired:
            return False, "Tests timed out after 60 seconds"
        except Exception as e:
            return False, f"Error running tests: {str(e)}"

    def analyze_and_fix(self, task: Task, files: Dict[str, str], test_output: str) -> Dict[str, str]:
        """
        Analyze test failures and fix code

        Args:
            task: Original task
            files: Current file contents
            test_output: Test execution output

        Returns:
            Updated file contents
        """
        system_prompt = """You are an expert Python debugger. Your task is to analyze test failures and fix the code.

Guidelines:
- Carefully read the error messages and stack traces
- Identify the root cause of failures
- Fix the code without breaking existing functionality
- Ensure all edge cases are handled
- Maintain code quality and style

Respond with a JSON object:
{
  "analysis": "Your analysis of what went wrong",
  "fixes": [
    {
      "file_path": "path/to/file.py",
      "content": "updated file content"
    }
  ]
}"""

        files_section = "\n\n".join([
            f"File: {path}\n```python\n{content}\n```"
            for path, content in files.items()
        ])

        user_prompt = f"""Fix the following test failures:

Task: {task.title}
Requirements: {task.feature_requirements}
Test Requirements: {task.test_requirements}

Current Implementation:
{files_section}

Test Output:
```
{test_output}
```

Please analyze the failures and provide fixed code."""

        response = self.claude.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.2,
            max_tokens=8000
        )

        try:
            fix_data = json.loads(response)

            print(f"Analysis: {fix_data.get('analysis', 'N/A')}")

            fixed_files = {}
            for fix in fix_data.get("fixes", []):
                fixed_files[fix["file_path"]] = fix["content"]

            return fixed_files

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse fix response as JSON: {e}\nResponse: {response}")

    def debug_until_pass(self, task: Task, initial_files: Dict[str, str], task_dir: str) -> Tuple[bool, Dict[str, str], str]:
        """
        Iteratively debug and fix code until tests pass

        Args:
            task: Task being implemented
            initial_files: Initial implementation files
            task_dir: Directory containing implementation

        Returns:
            Tuple of (success, final_files, test_output)
        """
        current_files = initial_files.copy()
        iteration = 0

        while iteration < self.max_iterations:
            iteration += 1
            print(f"Debug iteration {iteration}/{self.max_iterations}")

            # Run tests
            success, test_output = self.run_tests(task_dir)

            if success:
                print("All tests passed!")
                return True, current_files, test_output

            print(f"Tests failed. Analyzing and fixing...")

            # Analyze and fix
            try:
                fixed_files = self.analyze_and_fix(task, current_files, test_output)

                # Update files in workspace
                for file_path, content in fixed_files.items():
                    full_path = f"{task_dir}/{file_path}"
                    self.file_handler.save_text(content, full_path)
                    current_files[file_path] = content

            except Exception as e:
                print(f"Error during fix attempt: {e}")
                return False, current_files, test_output

        print(f"Failed to fix issues after {self.max_iterations} iterations")
        return False, current_files, test_output

    def create_pr(self, task: Task, files: Dict[str, str], test_output: str) -> PullRequest:
        """
        Create a pull request for the implementation

        Args:
            task: Implemented task
            files: Final file contents
            test_output: Test results

        Returns:
            PullRequest object
        """
        pr = PullRequest(
            id=f"PR-{task.id}",
            title=f"Implement {task.title}",
            description=f"""## Task: {task.title}

{task.description}

### Feature Requirements
{task.feature_requirements}

### Test Requirements
{task.test_requirements}

### Success Metrics
{chr(10).join(f"- {metric}" for metric in task.success_metrics)}

### Pass/Fail Criteria
{chr(10).join(f"- {criteria}" for criteria in task.pass_fail_criteria)}
""",
            task_id=task.id,
            branch_name=f"feature/{task.id.lower()}",
            files_changed=list(files.keys()),
            test_results=test_output,
            status=PRStatus.OPEN
        )

        return pr

    def process_task(self, task: Task, initial_files: Dict[str, str], task_dir: str) -> Tuple[PullRequest, bool]:
        """
        Complete debug workflow: test, fix, create PR

        Args:
            task: Task to process
            initial_files: Initial implementation
            task_dir: Task directory

        Returns:
            Tuple of (PullRequest, success)
        """
        print(f"Processing task: {task.id} - {task.title}")

        # Debug until tests pass
        success, final_files, test_output = self.debug_until_pass(task, initial_files, task_dir)

        # Create PR regardless of test status (for review)
        pr = self.create_pr(task, final_files, test_output)

        if not success:
            pr.status = PRStatus.DRAFT
            pr.description += "\n\n**Note:** Some tests are still failing. Review needed.\n"

        return pr, success

    def save_pr(self, pr: PullRequest, output_path: str) -> None:
        """Save PR to file"""
        self.file_handler.save_json(pr.model_dump(), output_path)
