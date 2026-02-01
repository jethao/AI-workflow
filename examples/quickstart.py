#!/usr/bin/env python3
"""
Quick start example for AI Agent Workflow

This demonstrates how to use individual agents or run the complete workflow.
"""
from dotenv import load_dotenv
from models.prd import PRD
from workflows.main_workflow import AgentWorkflow
from agents import DesignerAgent, PlannerAgent
from utils.claude_client import ClaudeClient

load_dotenv()


def example_individual_agents():
    """Example of using individual agents"""
    print("="*60)
    print("EXAMPLE 1: Using Individual Agents")
    print("="*60)

    # Initialize Claude client
    client = ClaudeClient()

    # Create a simple PRD
    prd = PRD(
        title="Task Management API",
        description="Build a RESTful API for task management with CRUD operations",
        level="feature",
        objectives=[
            "Create REST API endpoints for tasks",
            "Implement CRUD operations",
            "Add input validation"
        ],
        user_stories=[
            "As a user, I want to create tasks",
            "As a user, I want to list all tasks",
            "As a user, I want to update tasks",
            "As a user, I want to delete tasks"
        ],
        requirements=[
            "GET /tasks - list all tasks",
            "POST /tasks - create task",
            "PUT /tasks/{id} - update task",
            "DELETE /tasks/{id} - delete task",
            "Request/response validation"
        ],
        success_metrics=[
            "API response time < 200ms",
            "100% test coverage"
        ],
        constraints=[
            "Use FastAPI framework",
            "Follow REST best practices"
        ]
    )

    # Use Designer agent
    print("\n1. Creating architecture design...")
    designer = DesignerAgent(client)
    design = designer.design_from_prd(prd)

    print(f"   Title: {design.title}")
    print(f"   Pattern: {design.architecture_pattern}")
    print(f"   Components: {len(design.components)}")

    # Mark as reviewed (in real workflow, human would review)
    design.human_reviewed = True

    # Use Planner agent
    print("\n2. Creating tickets...")
    planner = PlannerAgent(client)
    epics = planner.create_tickets_from_design(design)

    print(f"   Epics: {len(epics)}")
    for epic in epics:
        print(f"   - {epic.title}: {len(epic.stories)} stories")

    print("\n✓ Individual agents example complete!")


def example_full_workflow():
    """Example of running the complete workflow"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Full Workflow")
    print("="*60)

    # Create PRD
    prd = PRD(
        title="Simple Calculator Service",
        description="Create a microservice for basic arithmetic operations",
        level="feature",
        objectives=[
            "Implement basic arithmetic operations",
            "Provide HTTP API interface"
        ],
        user_stories=[
            "As a user, I want to add two numbers",
            "As a user, I want to subtract two numbers"
        ],
        requirements=[
            "Addition endpoint",
            "Subtraction endpoint",
            "Input validation",
            "Unit tests"
        ],
        success_metrics=[
            "100% test pass rate",
            "Response time < 100ms"
        ],
        constraints=[
            "Python implementation",
            "Use standard library only"
        ]
    )

    # Initialize and run workflow
    print("\nRunning complete workflow...")
    workflow = AgentWorkflow(workspace_dir="./workspace_quickstart")

    try:
        final_state = workflow.run(prd)

        print("\n✓ Full workflow complete!")
        print(f"Status: {final_state.get('status')}")

        if final_state.get('all_prs'):
            print(f"PRs created: {len(final_state['all_prs'])}")

    except Exception as e:
        print(f"✗ Error: {e}")


def main():
    """Run examples"""
    print("\n")
    print("╔" + "═"*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "     AI Agent Workflow - Quick Start Examples".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "═"*58 + "╝")
    print("\n")

    try:
        # Example 1: Individual agents
        example_individual_agents()

        # Example 2: Full workflow (commented out to avoid long execution)
        # Uncomment to run:
        # example_full_workflow()

        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("="*60)

    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
