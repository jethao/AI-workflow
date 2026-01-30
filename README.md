# AI Agent Workflow

An automated software development workflow system powered by Claude AI and LangGraph. This system orchestrates multiple specialized agents to take a Product Requirement Document (PRD) and transform it into production-ready code with automated testing and code review.

## Overview

The system consists of 5 specialized agents working together:

1. **Designer Agent** - Reads PRD and designs system architecture
2. **Planner Agent** - Breaks down design into hierarchical tickets (Epic → Story → Task)
3. **Worker Agent** - Implements tasks in Python
4. **Debugger Agent** - Runs tests, analyzes failures, fixes bugs, creates PRs
5. **Reviewer Agent** - Performs code review on PRs

## Architecture

```
PRD → Designer → (Human Review) → Planner → Worker → Debugger → Reviewer
                                      ↓
                                   Tickets (Epic/Story/Task)
                                      ↓
                              [For each Task]
                                      ↓
                            Implementation → Testing → PR
```

## Features

- **Automated Architecture Design**: Generates comprehensive system designs from PRDs
- **Hierarchical Task Breakdown**: Creates Epics, Stories, and Tasks with detailed requirements
- **Python Code Generation**: Implements features with proper structure and documentation
- **Automated Testing & Debugging**: Runs tests, analyzes failures, and fixes bugs iteratively
- **Code Review**: Provides thorough code reviews with actionable feedback
- **LangGraph Orchestration**: Manages workflow state and agent coordination
- **Modular Design**: Each agent is independent and can be used separately

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd AI-workflow
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your Anthropic API key
```

## Usage

### Basic Usage

Run the complete workflow with a PRD:

```bash
python main.py --prd examples/sample_prd.json
```

This will:
1. Generate architecture design
2. Create tickets (saved to `workspace/tickets.json`)
3. Implement each task
4. Run tests and fix issues
5. Create PRs with code review

### Custom Workspace

Specify a custom workspace directory:

```bash
python main.py --prd examples/sample_prd.json --workspace ./my-project
```

### Output Structure

```
workspace/
├── design.json                    # Architecture design
├── tickets.json                   # All tickets (Epics/Stories/Tasks)
├── TASK-1/                        # Task implementation
│   ├── module.py
│   └── tests/
├── pr_TASK-1.json                # PR before review
├── pr_TASK-1_reviewed.json       # PR after review
└── ...
```

## PRD Format

Create a PRD as JSON:

```json
{
  "title": "Feature Name",
  "description": "Detailed description",
  "level": "product|feature",
  "objectives": ["Objective 1", "Objective 2"],
  "user_stories": ["As a user, I want..."],
  "requirements": ["Requirement 1", "Requirement 2"],
  "success_metrics": ["Metric 1", "Metric 2"],
  "constraints": ["Constraint 1"]
}
```

See `examples/sample_prd.json` for a complete example.

## Project Structure

```
AI-workflow/
├── agents/              # Agent implementations
│   ├── designer.py      # Architecture design
│   ├── planner.py       # Task breakdown
│   ├── worker.py        # Code implementation
│   ├── reviewer.py      # Code review
│   └── debugger.py      # Testing & debugging
├── models/              # Data models
│   ├── prd.py          # PRD model
│   ├── design.py       # Design document model
│   ├── ticket.py       # Ticket models (Epic/Story/Task)
│   └── pr.py           # Pull request model
├── workflows/           # LangGraph workflows
│   └── main_workflow.py
├── utils/              # Utilities
│   ├── claude_client.py # Claude API wrapper
│   └── file_handler.py  # File I/O
├── examples/           # Example PRDs
├── tests/             # Test files
├── main.py            # Entry point
└── requirements.txt   # Dependencies
```

## Using Individual Agents

You can use agents independently:

```python
from agents import DesignerAgent, PlannerAgent
from models.prd import PRD
from utils.claude_client import ClaudeClient

# Initialize
client = ClaudeClient()
designer = DesignerAgent(client)

# Create PRD
prd = PRD(
    title="My Feature",
    description="...",
    level="feature",
    objectives=["..."],
    requirements=["..."],
    success_metrics=["..."]
)

# Generate design
design = designer.design_from_prd(prd)
print(design.overview)
```

## Configuration

### Claude API Settings

The system uses Claude Sonnet 4 by default. You can configure the model in `utils/claude_client.py`:

```python
client = ClaudeClient(model="claude-sonnet-4-20250514")
```

### Debugger Settings

Configure debug iterations in `agents/debugger.py`:

```python
self.max_iterations = 5  # Maximum debug attempts
```

## Development

### Adding a New Agent

1. Create a new file in `agents/`
2. Implement the agent class with required methods
3. Add to `agents/__init__.py`
4. Update workflow in `workflows/main_workflow.py`

### Running Tests

```bash
pytest tests/
```

## Limitations & Future Enhancements

### Current Limitations

- Simplified ticket representation (not integrated with real Jira/Linear)
- Python-only implementation
- Basic test execution (pytest only)
- No actual git operations for PR creation

### Planned Enhancements

- [ ] Jira/Linear API integration
- [ ] Support for multiple programming languages
- [ ] Git integration for real PR creation
- [ ] Parallel task execution
- [ ] Human-in-the-loop approval points
- [ ] Cost tracking and optimization
- [ ] Agent performance metrics
- [ ] Web UI for monitoring workflow

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

See LICENSE file for details.

## Support

For issues and questions, please open an issue on GitHub.

## Acknowledgments

- Built with [Claude AI](https://anthropic.com) by Anthropic
- Workflow orchestration by [LangGraph](https://github.com/langchain-ai/langgraph)
