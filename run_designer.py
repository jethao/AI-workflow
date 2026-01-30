#!/usr/bin/env python3
"""
Run Designer Agent standalone

This script demonstrates how to use the Designer agent independently
to create architecture designs from PRDs.
"""
import os
import json
from dotenv import load_dotenv
from agents.designer import DesignerAgent
from models.prd import PRD
from utils.claude_client import ClaudeClient

load_dotenv()


def main():
    print("\n" + "="*60)
    print("Designer Agent - Standalone Execution")
    print("="*60 + "\n")

    # Check API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set in .env file")
        print("Please run: cp .env.example .env")
        print("Then edit .env and add your API key")
        return

    # Initialize Claude client and Designer agent
    print("Initializing Designer Agent...")
    claude_client = ClaudeClient()
    designer = DesignerAgent(claude_client)
    print("✓ Designer Agent ready\n")

    # Option 1: Load PRD from file
    print("Loading PRD from examples/sample_prd.json...")
    with open("examples/sample_prd.json", "r") as f:
        prd_data = json.load(f)
    prd = PRD(**prd_data)
    print(f"✓ PRD loaded: {prd.title}\n")

    # Option 2: Create PRD programmatically (commented out)
    """
    prd = PRD(
        title="Your Feature Name",
        description="Detailed description of your feature",
        level="feature",  # or "product"
        objectives=[
            "Objective 1",
            "Objective 2"
        ],
        user_stories=[
            "As a user, I want to...",
            "As a developer, I need to..."
        ],
        requirements=[
            "Requirement 1",
            "Requirement 2"
        ],
        success_metrics=[
            "Metric 1",
            "Metric 2"
        ],
        constraints=[
            "Constraint 1"
        ]
    )
    """

    # Generate architecture design
    print("="*60)
    print("Generating Architecture Design...")
    print("="*60 + "\n")
    print("This may take 30-60 seconds...\n")

    try:
        design = designer.design_from_prd(prd)

        # Display design summary
        print("✓ Design Generated Successfully!\n")
        print("="*60)
        print("DESIGN SUMMARY")
        print("="*60)
        print(f"\nTitle: {design.title}")
        print(f"\nArchitecture Pattern: {design.architecture_pattern}")
        print(f"\nOverview:\n{design.overview}")

        # Components
        print(f"\n\n{'='*60}")
        print(f"COMPONENTS ({len(design.components)})")
        print("="*60)
        for i, comp in enumerate(design.components, 1):
            print(f"\n  {i}. {comp.name}")
            print(f"     Purpose: {comp.purpose}")
            print(f"     Responsibilities: {len(comp.responsibilities)}")
            print(f"     Dependencies: {', '.join(comp.dependencies) if comp.dependencies else 'None'}")

        # State Machines
        if design.state_machines:
            print(f"\n\n{'='*60}")
            print(f"STATE MACHINES ({len(design.state_machines)})")
            print("="*60)
            for i, sm in enumerate(design.state_machines, 1):
                print(f"\n  {i}. {sm.name}")
                print(f"     Description: {sm.description}")
                print(f"     States: {', '.join(sm.states)}")
                print(f"     Initial: {sm.initial_state} → Final: {', '.join(sm.final_states)}")
                print(f"     Transitions: {len(sm.transitions)}")
                for trans in sm.transitions[:3]:  # Show first 3
                    print(f"       • {trans.from_state} → {trans.to_state} (on {trans.trigger})")
                if len(sm.transitions) > 3:
                    print(f"       ... and {len(sm.transitions) - 3} more")

        # Data Paths
        if design.data_paths:
            print(f"\n\n{'='*60}")
            print(f"DATA PATHS ({len(design.data_paths)})")
            print("="*60)
            for i, dp in enumerate(design.data_paths, 1):
                print(f"\n  {i}. {dp.name}")
                print(f"     Description: {dp.description}")
                print(f"     Flow: {' → '.join(dp.steps)}")
                print(f"     Transformations: {len(dp.data_transformations)}")

        # Control Paths
        if design.control_paths:
            print(f"\n\n{'='*60}")
            print(f"CONTROL PATHS ({len(design.control_paths)})")
            print("="*60)
            for i, cp in enumerate(design.control_paths, 1):
                print(f"\n  {i}. {cp.name}")
                print(f"     Description: {cp.description}")
                print(f"     Sequence: {len(cp.sequence)} steps")
                print(f"     Decision Points: {len(cp.decision_points)}")

        # Call Stacks
        if design.call_stacks:
            print(f"\n\n{'='*60}")
            print(f"CALL STACKS ({len(design.call_stacks)})")
            print("="*60)
            for i, cs in enumerate(design.call_stacks, 1):
                print(f"\n  {i}. {cs.operation}")
                print(f"     Description: {cs.description}")
                print(f"     Call Depth: {len(cs.stack_frames)} frames")
                for j, frame in enumerate(cs.stack_frames, 1):
                    print(f"       {j}. {frame.function}()")

        # API Endpoints
        if design.api_endpoints:
            print(f"\n\n{'='*60}")
            print(f"API ENDPOINTS ({len(design.api_endpoints)})")
            print("="*60)
            for i, api in enumerate(design.api_endpoints, 1):
                print(f"\n  {i}. {api.method} {api.path}")
                print(f"     Description: {api.description}")
                print(f"     Auth: {api.authentication or 'None'}")

        # Data Models
        print(f"\n\n{'='*60}")
        print(f"DATA MODELS ({len(design.data_models)})")
        print("="*60)
        for model in design.data_models:
            print(f"  - {model}")

        # Examples
        if design.examples:
            print(f"\n\n{'='*60}")
            print(f"EXAMPLES ({len(design.examples)})")
            print("="*60)
            for i, example in enumerate(design.examples, 1):
                print(f"\n  {i}. {example.title}")
                print(f"     Scenario: {example.scenario}")
                print(f"     Code: {example.code_example[:100]}...")

        # Tech Stack
        print(f"\n\n{'='*60}")
        print("TECH STACK")
        print("="*60)
        for category, tech in design.tech_stack.items():
            print(f"  - {category}: {tech}")

        # Security & Scalability
        print(f"\n\nSecurity Considerations ({len(design.security_considerations)}):")
        for consideration in design.security_considerations[:5]:
            print(f"  - {consideration}")

        print(f"\n\nScalability Considerations ({len(design.scalability_considerations)}):")
        for consideration in design.scalability_considerations[:5]:
            print(f"  - {consideration}")

        # Save design to file
        output_file = "data/design_output.json"
        os.makedirs("data", exist_ok=True)
        designer.save_design(design, output_file)

        print("\n" + "="*60)
        print(f"✓ Design saved to: {output_file}")
        print("="*60)

        print("\n\nNext Steps:")
        print("1. Review the design document")
        print("2. Mark human_reviewed=true in the JSON file")
        print("3. Use PlannerAgent to break it down into tickets")
        print("   Run: python run_planner.py")

    except Exception as e:
        print(f"\n✗ Error generating design: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
