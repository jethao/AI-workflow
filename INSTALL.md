# Installation Guide

Complete installation instructions for the AI Agent Workflow system.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Anthropic API key ([Get one here](https://console.anthropic.com/))

## Quick Install

```bash
# 1. Clone the repository
git clone <repository-url>
cd AI-workflow

# 2. Create virtual environment (recommended)
python -m venv venv

# 3. Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set up environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# 6. Verify installation
python setup_check.py
```

## Detailed Installation Steps

### Step 1: Python Installation

Check if Python is installed:
```bash
python --version
# or
python3 --version
```

If Python is not installed:
- **macOS**: `brew install python3`
- **Ubuntu/Debian**: `sudo apt-get install python3 python3-pip`
- **Windows**: Download from [python.org](https://www.python.org/downloads/)

### Step 2: Virtual Environment (Recommended)

Using a virtual environment keeps dependencies isolated:

```bash
# Create virtual environment
python -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows Command Prompt:
venv\Scripts\activate.bat

# Windows PowerShell:
venv\Scripts\Activate.ps1
```

You'll see `(venv)` in your terminal prompt when activated.

### Step 3: Install Dependencies

#### Option A: Standard Installation
```bash
pip install -r requirements.txt
```

#### Option B: Development Installation (includes testing tools)
```bash
pip install -r requirements-dev.txt
```

#### Option C: Install Specific Versions
```bash
# Core only
pip install anthropic langgraph python-dotenv pydantic

# With testing
pip install anthropic langgraph python-dotenv pydantic pytest
```

### Step 4: Environment Configuration

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your favorite editor
nano .env
# or
vim .env
# or
code .env  # VS Code
```

Add your API key:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

**Getting an API Key:**
1. Go to [https://console.anthropic.com/](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key
5. Copy it to your .env file

### Step 5: Verify Installation

Run the setup check script:
```bash
python setup_check.py
```

This will verify:
- ✓ Python version
- ✓ All dependencies installed
- ✓ Environment configured correctly
- ✓ Project structure
- ✓ Example files present
- ✓ Modules can be imported

## Package Details

### Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| anthropic | >=0.18.0 | Claude API client |
| langgraph | >=0.0.20 | Workflow orchestration |
| langchain-core | >=0.1.0 | LangChain core functionality |
| python-dotenv | >=1.0.0 | Environment variable management |
| pydantic | >=2.5.0 | Data validation and models |
| pytest | >=7.4.0 | Testing framework |
| jinja2 | >=3.1.2 | Template engine |
| typing-extensions | >=4.8.0 | Enhanced type hints |
| orjson | >=3.9.0 | Fast JSON parsing |

### Why Each Package?

- **anthropic**: Official SDK for Claude API - enables AI-powered agents
- **langgraph**: State machine framework for orchestrating multi-agent workflows
- **langchain-core**: Required dependency for langgraph
- **python-dotenv**: Securely loads API keys from .env file
- **pydantic**: Validates data models (PRD, Design, Tickets, PR)
- **pytest**: Runs automated tests in the Debugger agent
- **jinja2**: Template rendering (for future enhancements)
- **typing-extensions**: Better type hints for Python 3.8+
- **orjson**: Fast JSON serialization/deserialization

## Troubleshooting

### Issue: `pip: command not found`

**Solution:**
```bash
# Try pip3 instead
pip3 install -r requirements.txt

# Or use python -m pip
python -m pip install -r requirements.txt
```

### Issue: `ModuleNotFoundError: No module named 'anthropic'`

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: `ANTHROPIC_API_KEY not found`

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check it contains the key
cat .env

# Make sure it's not set to placeholder
grep ANTHROPIC_API_KEY .env
```

### Issue: Import errors with langgraph

**Solution:**
```bash
# Install langchain-core explicitly
pip install langchain-core>=0.1.0

# Or upgrade all packages
pip install --upgrade -r requirements.txt
```

### Issue: Permission denied on Windows

**Solution:**
```powershell
# Run PowerShell as Administrator, then:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate venv again
venv\Scripts\Activate.ps1
```

### Issue: SSL Certificate errors

**Solution:**
```bash
# Update pip and certificates
pip install --upgrade pip certifi

# Retry installation
pip install -r requirements.txt
```

## Upgrading

To upgrade all packages to latest versions:

```bash
# Upgrade pip first
pip install --upgrade pip

# Upgrade all packages
pip install --upgrade -r requirements.txt

# Or upgrade specific package
pip install --upgrade anthropic
```

## Uninstallation

```bash
# Deactivate virtual environment
deactivate

# Remove virtual environment
rm -rf venv

# Or remove all installed packages
pip uninstall -r requirements.txt -y
```

## Docker Installation (Alternative)

If you prefer Docker:

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py", "--prd", "examples/sample_prd.json"]
```

```bash
# Build and run
docker build -t ai-workflow .
docker run --env-file .env -v $(pwd)/workspace:/app/workspace ai-workflow
```

## System Requirements

- **RAM**: 2GB minimum, 4GB recommended
- **Disk**: 500MB for dependencies, 1GB+ for workspace
- **Network**: Internet connection required for Claude API
- **OS**: macOS, Linux, Windows 10+

## Next Steps

After successful installation:

1. **Verify setup**: `python setup_check.py`
2. **Try quickstart**: `python examples/quickstart.py`
3. **Run designer**: `python run_designer.py`
4. **Read usage guide**: `cat USAGE.md`

## Getting Help

If you encounter issues:

1. Check the troubleshooting section above
2. Verify your Python version: `python --version`
3. Check installed packages: `pip list`
4. Run setup check: `python setup_check.py`
5. Open an issue on GitHub with error details

## Additional Resources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
