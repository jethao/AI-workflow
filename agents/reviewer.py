import json
from typing import List, Dict
from models.pr import PullRequest, ReviewComment, PRStatus
from models.ticket import Task
from utils.claude_client import ClaudeClient
from utils.file_handler import FileHandler


class ReviewerAgent:
    """
    Reviewer Agent - Reviews pull requests created by Worker/Debugger
    """

    def __init__(self, claude_client: ClaudeClient):
        self.claude = claude_client
        self.file_handler = FileHandler()

    def review_pr(self, pr: PullRequest, task: Task, file_contents: Dict[str, str]) -> PullRequest:
        """
        Review a pull request

        Args:
            pr: Pull request to review
            task: Original task for context
            file_contents: Dictionary mapping file paths to their content

        Returns:
            Updated PR with review comments
        """
        system_prompt = """You are an expert code reviewer. Your task is to review code changes thoroughly.

Review criteria:
- Code quality and maintainability
- Adherence to requirements
- Test coverage
- Security vulnerabilities
- Performance considerations
- Best practices and patterns
- Documentation quality

For each issue found, provide:
- File path and line number (if applicable)
- Severity (info, warning, error)
- Clear description of the issue
- Suggested fix

Respond with a JSON object:
{
  "overall_assessment": "string",
  "recommendation": "approve|request_changes",
  "comments": [
    {
      "file_path": "string",
      "line_number": null or number,
      "comment": "string",
      "severity": "info|warning|error"
    }
  ],
  "positive_aspects": ["string"],
  "areas_for_improvement": ["string"]
}"""

        # Prepare file contents for review
        files_section = "\n\n".join([
            f"File: {path}\n```python\n{content}\n```"
            for path, content in file_contents.items()
        ])

        user_prompt = f"""Review the following pull request:

PR Title: {pr.title}
PR Description: {pr.description}

Original Task:
- Title: {task.title}
- Requirements: {task.feature_requirements}
- Test Requirements: {task.test_requirements}
- Success Metrics: {', '.join(task.success_metrics)}
- Pass/Fail Criteria: {', '.join(task.pass_fail_criteria)}

Changed Files:
{files_section}

Test Results:
{pr.test_results or "No test results available"}

Please provide a thorough code review."""

        response = self.claude.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.3,
            max_tokens=4096
        )

        # Parse the review
        try:
            review_data = json.loads(response)

            comments = [
                ReviewComment(
                    file_path=c["file_path"],
                    line_number=c.get("line_number"),
                    comment=c["comment"],
                    severity=c["severity"]
                )
                for c in review_data.get("comments", [])
            ]

            pr.review_comments = comments

            # Update PR status based on recommendation
            if review_data["recommendation"] == "approve":
                pr.status = PRStatus.APPROVED
            else:
                pr.status = PRStatus.CHANGES_REQUESTED

            # Store additional review info in description
            pr.description += f"\n\n## Review Summary\n\n"
            pr.description += f"**Overall Assessment:** {review_data['overall_assessment']}\n\n"

            if review_data.get("positive_aspects"):
                pr.description += "**Positive Aspects:**\n"
                for aspect in review_data["positive_aspects"]:
                    pr.description += f"- {aspect}\n"
                pr.description += "\n"

            if review_data.get("areas_for_improvement"):
                pr.description += "**Areas for Improvement:**\n"
                for area in review_data["areas_for_improvement"]:
                    pr.description += f"- {area}\n"

            return pr

        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse review response as JSON: {e}\nResponse: {response}")

    def save_review(self, pr: PullRequest, output_path: str) -> None:
        """Save reviewed PR to file"""
        self.file_handler.save_json(pr.model_dump(), output_path)

    def load_pr(self, input_path: str) -> PullRequest:
        """Load PR from file"""
        data = self.file_handler.load_json(input_path)
        return PullRequest(**data)
