from typing import TypedDict, Annotated, Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from agents import DesignerAgent, PlannerAgent, WorkerAgent, ReviewerAgent, DebuggerAgent
from models.prd import PRD
from models.design import Design
from models.ticket import Epic, Task
from models.pr import PullRequest
from utils.claude_client import ClaudeClient
from utils.file_handler import FileHandler
import os


class WorkflowState(TypedDict):
    """State that flows through the workflow"""
    prd: PRD
    design: Design
    epics: list[Epic]
    current_task_index: int
    current_task: Task
    implementation_files: Dict[str, str]
    pr: PullRequest
    all_prs: list[PullRequest]
    task_dir: str
    error: str
    status: str


class AgentWorkflow:
    """
    Main workflow orchestrating all agents using LangGraph
    """

    def __init__(self, api_key: str = None, workspace_dir: str = "./workspace"):
        """Initialize workflow with all agents"""
        self.claude_client = ClaudeClient(api_key=api_key)
        self.workspace_dir = workspace_dir
        self.file_handler = FileHandler()

        # Initialize agents
        self.designer = DesignerAgent(self.claude_client)
        self.planner = PlannerAgent(self.claude_client)
        self.worker = WorkerAgent(self.claude_client, workspace_dir)
        self.reviewer = ReviewerAgent(self.claude_client)
        self.debugger = DebuggerAgent(self.claude_client, workspace_dir)

        # Build workflow graph
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow"""

        # Create the graph
        workflow = StateGraph(WorkflowState)

        # Add nodes
        workflow.add_node("design", self._design_node)
        workflow.add_node("plan", self._plan_node)
        workflow.add_node("implement", self._implement_node)
        workflow.add_node("debug", self._debug_node)
        workflow.add_node("review", self._review_node)

        # Define edges
        workflow.set_entry_point("design")
        workflow.add_edge("design", "plan")
        workflow.add_edge("plan", "implement")
        workflow.add_edge("implement", "debug")
        workflow.add_edge("debug", "review")

        # Conditional edge: check if more tasks exist
        workflow.add_conditional_edges(
            "review",
            self._should_continue,
            {
                "continue": "implement",
                "end": END
            }
        )

        return workflow.compile()

    def _design_node(self, state: WorkflowState) -> WorkflowState:
        """Design phase: PRD -> Architecture Design"""
        print("\n=== DESIGN PHASE ===")
        try:
            design = self.designer.design_from_prd(state["prd"])

            # Save design for human review
            design_path = os.path.join(self.workspace_dir, "design.json")
            self.designer.save_design(design, design_path)

            print(f"Design created: {design.title}")
            print("Design saved to:", design_path)
            print("\nWaiting for human review...")
            print("Please review the design and set 'human_reviewed' to true, then continue.")

            # In a real system, this would wait for human approval
            # For now, auto-approve
            design.human_reviewed = True

            state["design"] = design
            state["status"] = "design_complete"

        except Exception as e:
            state["error"] = str(e)
            state["status"] = "design_failed"

        return state

    def _plan_node(self, state: WorkflowState) -> WorkflowState:
        """Planning phase: Design -> Tickets (Epic/Story/Task)"""
        print("\n=== PLANNING PHASE ===")
        try:
            epics = self.planner.create_tickets_from_design(state["design"])

            # Save tickets
            tickets_path = os.path.join(self.workspace_dir, "tickets.json")
            self.planner.save_tickets(epics, tickets_path)

            # Get all tasks for iteration
            all_tasks = self.planner.get_all_tasks(epics)

            print(f"Created {len(epics)} epic(s) with {len(all_tasks)} task(s)")
            print("Tickets saved to:", tickets_path)

            state["epics"] = epics
            state["current_task_index"] = 0
            state["all_prs"] = []
            state["status"] = "planning_complete"

        except Exception as e:
            state["error"] = str(e)
            state["status"] = "planning_failed"

        return state

    def _implement_node(self, state: WorkflowState) -> WorkflowState:
        """Implementation phase: Task -> Python Code"""
        print("\n=== IMPLEMENTATION PHASE ===")
        try:
            all_tasks = self.planner.get_all_tasks(state["epics"])
            task_index = state["current_task_index"]

            if task_index >= len(all_tasks):
                state["status"] = "all_tasks_complete"
                return state

            task = all_tasks[task_index]
            print(f"Implementing task {task_index + 1}/{len(all_tasks)}: {task.title}")

            # Implement task
            files = self.worker.implement_task(task)
            saved_paths = self.worker.save_implementation(files, task.id)

            task_dir = os.path.join(self.workspace_dir, task.id)

            state["current_task"] = task
            state["implementation_files"] = files
            state["task_dir"] = task_dir
            state["status"] = "implementation_complete"

            print(f"Implementation saved to: {task_dir}")

        except Exception as e:
            state["error"] = str(e)
            state["status"] = "implementation_failed"

        return state

    def _debug_node(self, state: WorkflowState) -> WorkflowState:
        """Debug phase: Run tests, fix issues, create PR"""
        print("\n=== DEBUG PHASE ===")
        try:
            task = state["current_task"]
            files = state["implementation_files"]
            task_dir = state["task_dir"]

            # Process task (test + fix + create PR)
            pr, success = self.debugger.process_task(task, files, task_dir)

            # Save PR
            pr_path = os.path.join(self.workspace_dir, f"pr_{task.id}.json")
            self.debugger.save_pr(pr, pr_path)

            state["pr"] = pr
            state["status"] = "debug_complete" if success else "debug_failed"

            print(f"PR created: {pr.id}")
            print(f"PR saved to: {pr_path}")

        except Exception as e:
            state["error"] = str(e)
            state["status"] = "debug_failed"

        return state

    def _review_node(self, state: WorkflowState) -> WorkflowState:
        """Review phase: Code review of PR"""
        print("\n=== REVIEW PHASE ===")
        try:
            pr = state["pr"]
            task = state["current_task"]
            files = state["implementation_files"]

            # Review PR
            reviewed_pr = self.reviewer.review_pr(pr, task, files)

            # Save reviewed PR
            pr_path = os.path.join(self.workspace_dir, f"pr_{task.id}_reviewed.json")
            self.reviewer.save_review(reviewed_pr, pr_path)

            # Add to list of all PRs
            if "all_prs" not in state:
                state["all_prs"] = []
            state["all_prs"].append(reviewed_pr)

            print(f"Review complete: {reviewed_pr.status}")
            print(f"Comments: {len(reviewed_pr.review_comments)}")
            print(f"Reviewed PR saved to: {pr_path}")

            state["status"] = "review_complete"

        except Exception as e:
            state["error"] = str(e)
            state["status"] = "review_failed"

        return state

    def _should_continue(self, state: WorkflowState) -> str:
        """Determine if more tasks need to be processed"""
        all_tasks = self.planner.get_all_tasks(state["epics"])
        next_index = state["current_task_index"] + 1

        if next_index < len(all_tasks):
            state["current_task_index"] = next_index
            return "continue"
        else:
            return "end"

    def run(self, prd: PRD) -> Dict[str, Any]:
        """
        Run the complete workflow

        Args:
            prd: Product Requirement Document

        Returns:
            Final workflow state
        """
        print("Starting AI Workflow...")
        print(f"PRD: {prd.title}")

        # Initialize state
        initial_state = {
            "prd": prd,
            "status": "started",
            "current_task_index": 0,
            "all_prs": []
        }

        # Run workflow
        final_state = self.graph.invoke(initial_state)

        print("\n=== WORKFLOW COMPLETE ===")
        print(f"Status: {final_state.get('status')}")
        print(f"PRs created: {len(final_state.get('all_prs', []))}")

        return final_state

    def run_from_prd_file(self, prd_path: str) -> Dict[str, Any]:
        """
        Run workflow from PRD file

        Args:
            prd_path: Path to PRD JSON file

        Returns:
            Final workflow state
        """
        prd_data = self.file_handler.load_json(prd_path)
        prd = PRD(**prd_data)
        return self.run(prd)
