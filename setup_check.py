#!/usr/bin/env python3
"""
Setup validation script for AI Agent Workflow

Run this to verify your installation is configured correctly.
"""
import os
import sys


def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ✗ Python 3.8+ required")
        return False
    print(f"  ✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    required_packages = [
        "anthropic",
        "langgraph",
        "dotenv",
        "pydantic"
    ]

    all_installed = True
    for package in required_packages:
        try:
            if package == "dotenv":
                __import__("dotenv")
            else:
                __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} not installed")
            all_installed = False

    return all_installed


def check_env_file():
    """Check if .env file exists and has API key"""
    print("\nChecking environment configuration...")

    if not os.path.exists(".env"):
        print("  ✗ .env file not found")
        print("    Run: cp .env.example .env")
        return False

    print("  ✓ .env file exists")

    # Check if API key is set
    from dotenv import load_dotenv
    load_dotenv()

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        print("  ✗ ANTHROPIC_API_KEY not set in .env")
        print("    Edit .env and add your Anthropic API key")
        return False

    print("  ✓ ANTHROPIC_API_KEY is configured")
    return True


def check_project_structure():
    """Check if project structure is correct"""
    print("\nChecking project structure...")

    required_dirs = [
        "agents",
        "models",
        "workflows",
        "utils",
        "examples",
        "tests"
    ]

    all_exist = True
    for directory in required_dirs:
        if os.path.isdir(directory):
            print(f"  ✓ {directory}/")
        else:
            print(f"  ✗ {directory}/ not found")
            all_exist = False

    return all_exist


def check_example_files():
    """Check if example files exist"""
    print("\nChecking example files...")

    example_files = [
        "examples/sample_prd.json",
        "examples/quickstart.py"
    ]

    all_exist = True
    for filepath in example_files:
        if os.path.exists(filepath):
            print(f"  ✓ {filepath}")
        else:
            print(f"  ✗ {filepath} not found")
            all_exist = False

    return all_exist


def test_import():
    """Test importing main modules"""
    print("\nTesting module imports...")

    try:
        from agents import DesignerAgent, PlannerAgent, WorkerAgent, ReviewerAgent, DebuggerAgent
        print("  ✓ All agents import successfully")

        from models import PRD, Design, Epic, Story, Task, PullRequest
        print("  ✓ All models import successfully")

        from utils import ClaudeClient, FileHandler
        print("  ✓ All utils import successfully")

        from workflows import AgentWorkflow
        print("  ✓ Workflow imports successfully")

        return True

    except ImportError as e:
        print(f"  ✗ Import error: {e}")
        return False


def main():
    """Run all checks"""
    print("\n" + "="*60)
    print("AI Agent Workflow - Setup Validation")
    print("="*60 + "\n")

    checks = [
        ("Python version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment", check_env_file),
        ("Project structure", check_project_structure),
        ("Example files", check_example_files),
        ("Module imports", test_import)
    ]

    results = []
    for name, check_func in checks:
        try:
            results.append((name, check_func()))
        except Exception as e:
            print(f"  ✗ Error during check: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "="*60)
    print("Summary")
    print("="*60)

    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False

    print("\n" + "="*60)

    if all_passed:
        print("✓ All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("  1. Review examples/sample_prd.json")
        print("  2. Run: python main.py --prd examples/sample_prd.json")
        print("  3. Or try: python examples/quickstart.py")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("\nInstallation help:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Create .env file: cp .env.example .env")
        print("  3. Add your API key to .env")
        return 1


if __name__ == "__main__":
    sys.exit(main())
