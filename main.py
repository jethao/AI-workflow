#!/usr/bin/env python3
"""
Main entry point for AI Agent Workflow
"""
import argparse
import sys
from dotenv import load_dotenv
from workflows.main_workflow import AgentWorkflow
from models.prd import PRD
from utils.file_handler import FileHandler

load_dotenv()


def main():
    parser = argparse.ArgumentParser(description="AI Agent Workflow for Software Development")
    parser.add_argument(
        "--prd",
        type=str,
        required=True,
        help="Path to PRD JSON file"
    )
    parser.add_argument(
        "--workspace",
        type=str,
        default="./workspace",
        help="Workspace directory for output (default: ./workspace)"
    )

    args = parser.parse_args()

    try:
        # Initialize workflow
        print("Initializing AI Agent Workflow...")
        workflow = AgentWorkflow(workspace_dir=args.workspace)

        # Run workflow
        print(f"Loading PRD from: {args.prd}")
        final_state = workflow.run_from_prd_file(args.prd)

        # Summary
        print("\n" + "="*60)
        print("WORKFLOW SUMMARY")
        print("="*60)
        print(f"Status: {final_state.get('status')}")
        print(f"Workspace: {args.workspace}")

        if final_state.get('design'):
            print(f"\nDesign: {final_state['design'].title}")

        if final_state.get('epics'):
            print(f"\nEpics created: {len(final_state['epics'])}")
            for epic in final_state['epics']:
                print(f"  - {epic.title} ({len(epic.stories)} stories)")

        if final_state.get('all_prs'):
            print(f"\nPull Requests: {len(final_state['all_prs'])}")
            for pr in final_state['all_prs']:
                print(f"  - {pr.id}: {pr.title} [{pr.status}]")

        if final_state.get('error'):
            print(f"\nError: {final_state['error']}")
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
