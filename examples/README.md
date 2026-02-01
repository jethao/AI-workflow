# Example PRDs

This directory contains example Product Requirement Documents (PRDs) to test the AI Agent Workflow system.

## Available Examples

### 1. sample_prd.json
**Type:** Feature-level PRD
**Complexity:** Simple
**Topic:** User Authentication System

A straightforward authentication system with email/password login, JWT tokens, and password reset functionality. Good for:
- Testing basic workflow
- Quick demonstration
- Learning how the system works

**Run:**
```bash
python main.py --prd examples/sample_prd.json
python run_designer.py  # Uses this by default
```

### 2. complex_prd.json
**Type:** Product-level PRD
**Complexity:** Advanced
**Topic:** E-Commerce Order Management System

A comprehensive order management system with:
- Complex state machines (order lifecycle)
- Multiple integrations (payment, shipping)
- Real-time inventory management
- Webhook notifications
- Analytics dashboard

This demonstrates:
- **State Machines**: Order states (pending → confirmed → processing → shipped → delivered)
- **Data Paths**: Data flow from order creation through payment to fulfillment
- **Control Paths**: Order processing logic with decision points
- **Call Stacks**: API call sequences for order operations
- **API Design**: RESTful endpoints with detailed specifications
- **Examples**: Multiple usage scenarios

**Run:**
```bash
python main.py --prd examples/complex_prd.json
```

To use this PRD with the designer:
```python
python run_designer.py
# Then modify run_designer.py to load complex_prd.json instead
```

## PRD Structure

All PRDs follow this structure:

```json
{
  "title": "Feature or Product Name",
  "description": "Detailed description",
  "level": "product|feature",
  "objectives": ["List", "of", "objectives"],
  "user_stories": ["As a user, I want..."],
  "requirements": ["Functional", "requirements"],
  "success_metrics": ["Measurable", "metrics"],
  "constraints": ["Technical", "constraints"]
}
```

## Creating Your Own PRD

### Feature-Level PRD Template

```json
{
  "title": "Your Feature Name",
  "description": "What does this feature do?",
  "level": "feature",
  "objectives": [
    "Primary goal 1",
    "Primary goal 2"
  ],
  "user_stories": [
    "As a [role], I want [action] so that [benefit]"
  ],
  "requirements": [
    "Specific requirement 1",
    "Specific requirement 2"
  ],
  "success_metrics": [
    "Metric 1 > threshold",
    "Metric 2 < threshold"
  ],
  "constraints": [
    "Must use technology X",
    "Must support Y concurrent users"
  ]
}
```

### Product-Level PRD Template

Use the same structure but:
- Set `"level": "product"`
- Include broader objectives
- More comprehensive requirements
- Multiple integration points
- Complex workflows and state machines

## Design Output

After running the Designer agent, you'll get:

### For Simple PRDs:
- Basic architecture pattern
- Core components
- Simple APIs
- Basic examples

### For Complex PRDs:
- **State Machines**: State diagrams with transitions
- **Data Paths**: Data flow through the system
- **Control Paths**: Execution flow with decision points
- **Call Stacks**: Function call sequences
- **Detailed APIs**: Full endpoint specifications with examples
- **Multiple Examples**: Various usage scenarios
- **Security & Scalability**: Comprehensive considerations

## Testing Your PRD

1. **Validate JSON:**
   ```bash
   python -m json.tool your_prd.json
   ```

2. **Run Designer:**
   ```bash
   # Edit run_designer.py to load your PRD
   python run_designer.py
   ```

3. **Run Full Workflow:**
   ```bash
   python main.py --prd your_prd.json
   ```

## Tips for Writing Good PRDs

1. **Be Specific**: Vague requirements lead to vague designs
2. **Include Metrics**: Define measurable success criteria
3. **List Constraints**: Technology, performance, compliance requirements
4. **User Stories**: Write from user perspective
5. **Level Appropriate**: Feature-level for components, product-level for systems

## Example Comparison

| Aspect | Simple PRD | Complex PRD |
|--------|-----------|-------------|
| Lines of Code | ~50 | ~100 |
| Components | 2-4 | 8-12 |
| State Machines | 0-1 | 2-4 |
| API Endpoints | 2-5 | 10-20 |
| Examples | 1-2 | 3-5 |
| Design Time | 30-60s | 60-120s |

## Next Steps

After creating your PRD:
1. Run the Designer to generate architecture
2. Review and refine the design
3. Run the Planner to create tickets
4. Execute the full workflow to implement

Happy designing! 🚀
