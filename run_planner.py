#!/usr/bin/env python3
"""
Run Planner Agent standalone

This script demonstrates how to use the Planner agent independently
to break down designs into tickets.
"""
import os
import json
from dotenv import load_dotenv
from agents.planner import PlannerAgent
from models.design import Design
from utils.claude_client import ClaudeClient

load_dotenv()


def main():
    print("\n" + "="*60)
    print("Planner Agent - Standalone Execution")
    print("="*60 + "\n")

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set in .env file")
        return

    # Initialize Claude client and Planner agent
    print("Initializing Planner Agent...")
    claude_client = ClaudeClient()
    planner = PlannerAgent(claude_client)
    print("✓ Planner Agent ready\n")

    # Load design from file
    design_file = "data/design_output.json"
    if not os.path.exists(design_file):
        print(f"Error: Design file not found: {design_file}")
        print("Please run the Designer agent first:")
        print("  python run_designer.py")
        return

    print(f"Loading design from {design_file}...")
    design = planner.load_design(design_file)
    print(f"✓ Design loaded: {design.title}\n")

    # Check if human reviewed
    if not design.human_reviewed:
        print("Warning: Design has not been marked as human-reviewed")
        print("Consider reviewing and setting human_reviewed=true")
        print()

    # Generate tickets
    print("="*60)
    print("Generating Tickets (Epics/Stories/Tasks)...")
    print("="*60 + "\n")
    print("This may take 1-2 minutes...\n")

    try:
        epics = planner.create_tickets_from_design(design)

        # Display ticket summary
        print("✓ Tickets Generated Successfully!\n")
        print("="*60)
        print("TICKET SUMMARY")
        print("="*60)

        all_tasks = planner.get_all_tasks(epics)
        print(f"\nTotal: {len(epics)} Epic(s), {len(all_tasks)} Task(s)\n")

        for epic in epics:
            print(f"\n📦 EPIC: {epic.id} - {epic.title}")
            print(f"   Priority: {epic.priority}")
            print(f"   Stories: {len(epic.stories)}")
            print(f"   Description: {epic.description[:100]}...")

            for story in epic.stories:
                print(f"\n   📋 STORY: {story.id} - {story.title}")
                print(f"      Priority: {story.priority}")
                print(f"      Tasks: {len(story.tasks)}")

                for task in story.tasks:
                    print(f"\n      ✓ TASK: {task.id} - {task.title}")
                    print(f"         Priority: {task.priority}")
                    print(f"         Estimated Effort: {task.estimated_effort or 'Not specified'}")
                    print(f"         Success Metrics: {len(task.success_metrics)}")
                    print(f"         Pass/Fail Criteria: {len(task.pass_fail_criteria)}")

        # Save tickets to file
        output_file = "data/tickets_output.json"
        planner.save_tickets(epics, output_file)

        print("\n" + "="*60)
        print(f"✓ Tickets saved to: {output_file}")
        print("="*60)

        print("\n\nNext Steps:")
        print("1. Review the tickets")
        print("2. Use WorkerAgent to implement tasks")
        print("   Run: python run_worker.py")

    except Exception as e:
        print(f"\n✗ Error generating tickets: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
