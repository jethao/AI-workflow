# Usage Guide

Quick reference for running agents individually or as a complete workflow.

## Setup (First Time Only)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Setup environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 3. Verify setup
python setup_check.py
```

## Running Individual Agents

### 1. Designer Agent (PRD → Architecture Design)

**Quick Run:**
```bash
python run_designer.py
```

This will:
- Load the sample PRD from `examples/sample_prd.json`
- Generate an architecture design using Claude
- Save the design to `data/design_output.json`
- Display a summary of the design

**Custom PRD:**
```python
from agents.designer import DesignerAgent
from models.prd import PRD
from utils.claude_client import ClaudeClient

# Initialize
client = ClaudeClient()
designer = DesignerAgent(client)

# Create PRD
prd = PRD(
    title="Your Feature",
    description="Description here",
    level="feature",
    objectives=["Objective 1"],
    user_stories=["As a user..."],
    requirements=["Requirement 1"],
    success_metrics=["Metric 1"],
    constraints=["Constraint 1"]
)

# Generate design
design = designer.design_from_prd(prd)

# Save design
designer.save_design(design, "my_design.json")
```

### 2. Planner Agent (Design → Tickets)

**Quick Run:**
```bash
python run_planner.py
```

This will:
- Load the design from `data/design_output.json`
- Break it down into Epics, Stories, and Tasks
- Save tickets to `data/tickets_output.json`
- Display the ticket hierarchy

**Custom Design:**
```python
from agents.planner import PlannerAgent
from utils.claude_client import ClaudeClient

# Initialize
client = ClaudeClient()
planner = PlannerAgent(client)

# Load design
design = planner.load_design("path/to/design.json")

# Generate tickets
epics = planner.create_tickets_from_design(design)

# Get all tasks
all_tasks = planner.get_all_tasks(epics)

# Save tickets
planner.save_tickets(epics, "my_tickets.json")
```

### 3. Worker Agent (Task → Python Code)

```python
from agents.worker import WorkerAgent
from models.ticket import Task
from utils.claude_client import ClaudeClient

# Initialize
client = ClaudeClient()
worker = WorkerAgent(client, workspace_dir="./workspace")

# Load or create task
task = Task(
    id="TASK-1",
    title="Implement feature",
    description="Feature description",
    feature_requirements="Requirements here",
    test_requirements="Test requirements",
    success_metrics=["Metric 1"],
    pass_fail_criteria=["Criteria 1"]
)

# Implement task
result = worker.implement_and_save(task)
print(f"Files created: {result['files']}")
```

### 4. Debugger Agent (Test + Fix + Create PR)

```python
from agents.debugger import DebuggerAgent
from utils.claude_client import ClaudeClient

# Initialize
client = ClaudeClient()
debugger = DebuggerAgent(client, workspace_dir="./workspace")

# Process task (test, fix, create PR)
pr, success = debugger.process_task(task, files, task_dir)

if success:
    print("All tests passed!")
else:
    print("Some tests failed, PR marked as draft")

# Save PR
debugger.save_pr(pr, f"pr_{task.id}.json")
```

### 5. Reviewer Agent (Code Review)

```python
from agents.reviewer import ReviewerAgent
from utils.claude_client import ClaudeClient

# Initialize
client = ClaudeClient()
reviewer = ReviewerAgent(client)

# Review PR
reviewed_pr = reviewer.review_pr(pr, task, file_contents)

print(f"Status: {reviewed_pr.status}")
print(f"Comments: {len(reviewed_pr.review_comments)}")

# Save review
reviewer.save_review(reviewed_pr, f"pr_{task.id}_reviewed.json")
```

## Complete Workflow

### Option 1: Command Line

```bash
python main.py --prd examples/sample_prd.json
```

With custom workspace:
```bash
python main.py --prd examples/sample_prd.json --workspace ./my-project
```

### Option 2: Python Script

```python
from workflows.main_workflow import AgentWorkflow
from models.prd import PRD

# Create PRD
prd = PRD(
    title="My Feature",
    description="Feature description",
    level="feature",
    objectives=["..."],
    user_stories=["..."],
    requirements=["..."],
    success_metrics=["..."]
)

# Initialize and run workflow
workflow = AgentWorkflow(workspace_dir="./workspace")
final_state = workflow.run(prd)

# Check results
print(f"Status: {final_state['status']}")
print(f"PRs created: {len(final_state['all_prs'])}")
```

### Option 3: From PRD File

```python
from workflows.main_workflow import AgentWorkflow

workflow = AgentWorkflow()
final_state = workflow.run_from_prd_file("examples/sample_prd.json")
```

## Typical Workflow Steps

### Step 1: Create PRD
```bash
# Create your PRD JSON file (see examples/sample_prd.json)
cp examples/sample_prd.json my_prd.json
# Edit my_prd.json with your requirements
```

### Step 2: Generate Design
```bash
python run_designer.py
# Review the output in data/design_output.json
# Edit if needed and set "human_reviewed": true
```

### Step 3: Create Tickets
```bash
python run_planner.py
# Review the tickets in data/tickets_output.json
```

### Step 4: Run Complete Workflow
```bash
python main.py --prd my_prd.json
```

This will:
1. Generate design (if not exists)
2. Create tickets
3. Implement each task
4. Run tests and fix bugs
5. Create PRs
6. Perform code reviews

## Output Structure

```
workspace/
├── design.json                    # Architecture design
├── tickets.json                   # All tickets
├── TASK-1/                        # Task implementation
│   ├── module.py
│   └── tests/
├── pr_TASK-1.json                # PR before review
└── pr_TASK-1_reviewed.json       # PR after review

data/
├── design_output.json            # Designer output
└── tickets_output.json           # Planner output
```

## Quick Examples

### Example 1: Quick Start
```bash
# Run the quick start examples
python examples/quickstart.py
```

### Example 2: Single Agent
```bash
# Just run the designer
python run_designer.py
```

### Example 3: Complete Pipeline
```bash
# Run everything
python main.py --prd examples/sample_prd.json
```

## Troubleshooting

### API Key Not Set
```bash
cp .env.example .env
# Edit .env and add: ANTHROPIC_API_KEY=your_key_here
```

### Module Import Errors
```bash
pip install -r requirements.txt
```

### Design Not Found
```bash
# Run designer first
python run_designer.py
```

### Tests Failing
The Debugger agent will automatically attempt to fix failing tests up to 5 times. If tests still fail, the PR will be created as a draft for manual review.

## Tips

1. **Start Small**: Test with the sample PRD first
2. **Review Designs**: Always review and approve designs before planning
3. **Monitor Progress**: Check the output files in `workspace/` and `data/`
4. **Iterate**: You can re-run individual agents with modified inputs
5. **Save Outputs**: The system saves all intermediate outputs for debugging

## Environment Variables

Required:
- `ANTHROPIC_API_KEY` - Your Anthropic API key

Optional (modify in code):
- Model selection (default: claude-sonnet-4-20250514)
- Workspace directory (default: ./workspace)
- Max debug iterations (default: 5)
