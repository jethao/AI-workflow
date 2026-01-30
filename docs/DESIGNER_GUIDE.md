# Designer Agent - Comprehensive Guide

The Designer Agent creates comprehensive architecture designs from Product Requirement Documents (PRDs).

## What the Designer Creates

### 1. Architecture Pattern & Components
Traditional architecture design with component breakdown, responsibilities, and dependencies.

### 2. State Machines
State machines for stateful components showing:
- All possible states
- State transitions with triggers
- Conditions and actions
- Example state flows

**Example:**
```
Order State Machine:
  States: pending → confirmed → processing → shipped → delivered
  Transitions:
    - pending → confirmed (on payment_success)
    - confirmed → processing (on warehouse_pickup)
    - processing → shipped (on carrier_accepted)
    - shipped → delivered (on delivery_confirmed)
```

### 3. Data Paths
How data flows through the system:
- Entry points and exit points
- Transformation steps
- Data format changes
- Validation points

**Example:**
```
Order Creation Data Path:
  1. Client sends order JSON
  2. API validates payload
  3. Check inventory availability
  4. Calculate totals and tax
  5. Create order record in database
  6. Return order confirmation
```

### 4. Control Paths
Execution flow showing:
- Sequence of operations
- Decision points (if/else)
- Loop constructs
- Error handling paths

**Example:**
```
Order Processing Control Path:
  1. Fetch order from queue
  2. Decision: Is payment confirmed?
     - Yes: Continue to step 3
     - No: Send payment reminder, exit
  3. Check inventory
  4. Decision: Items available?
     - Yes: Reserve items, continue
     - No: Backorder, notify customer
  5. Generate shipping label
  6. Update order status
```

### 5. Call Stacks
Function call sequences for typical operations:
- Stack frames showing function calls
- Parameters passed
- Return values
- Call depth visualization

**Example:**
```
Place Order Operation:
  1. api_create_order(user_id, items, address)
     ↓
  2. validate_order_data(order_data)
     ↓
  3. check_inventory(items)
     ↓
  4. reserve_inventory(items)
     ↓
  5. process_payment(user_id, amount)
     ↓
  6. create_order_record(order)
     ↓
  7. send_confirmation_email(user_id, order_id)
```

### 6. Detailed API Design
Comprehensive API specifications:
- HTTP method and path
- Request parameters and body
- Response formats (success and error)
- Authentication requirements
- Example requests and responses

**Example:**
```json
POST /api/orders
Description: Create a new order
Authentication: Bearer token

Request Body:
{
  "user_id": "string",
  "items": [{"product_id": "string", "quantity": number}],
  "shipping_address": {...}
}

Response 200:
{
  "order_id": "string",
  "status": "pending",
  "total": number,
  "estimated_delivery": "ISO date"
}

Response 400:
{
  "error": "Invalid request",
  "details": ["Missing required field: items"]
}

Example Request:
curl -X POST https://api.example.com/api/orders \
  -H "Authorization: Bearer token123" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"user123","items":[{"product_id":"prod456","quantity":2}]}'
```

### 7. Usage Examples
Practical examples demonstrating:
- Common use cases
- Code snippets
- Expected outputs
- Integration examples

**Example:**
```python
# Example: Creating an order
from order_service import OrderAPI

api = OrderAPI(api_key="your_key")

# Create order
order = api.create_order(
    user_id="user123",
    items=[
        {"product_id": "prod456", "quantity": 2}
    ],
    shipping_address={
        "street": "123 Main St",
        "city": "San Francisco",
        "zip": "94102"
    }
)

print(f"Order created: {order.id}")
print(f"Status: {order.status}")
print(f"Total: ${order.total}")

# Expected Output:
# Order created: ord_789xyz
# Status: pending
# Total: $49.99
```

## Design Output Structure

```
Design Document
├── Title & Overview
├── Architecture Pattern
├── Components
│   ├── Component 1 (name, purpose, responsibilities)
│   ├── Component 2
│   └── ...
├── State Machines
│   ├── State Machine 1 (states, transitions, example)
│   └── ...
├── Data Paths
│   ├── Path 1 (steps, transformations, example)
│   └── ...
├── Control Paths
│   ├── Path 1 (sequence, decisions, error handling)
│   └── ...
├── Call Stacks
│   ├── Operation 1 (stack frames, example)
│   └── ...
├── API Endpoints
│   ├── Endpoint 1 (method, path, request/response, example)
│   └── ...
├── Data Models
│   ├── Model 1
│   └── ...
├── Examples
│   ├── Example 1 (scenario, code, output)
│   └── ...
├── Tech Stack
├── Security Considerations
└── Scalability Considerations
```

## Running the Enhanced Designer

### Option 1: Command Line (Default PRD)
```bash
python run_designer.py
```

### Option 2: Custom PRD
Edit `run_designer.py` and change the PRD file:
```python
# Load your custom PRD
with open("examples/complex_prd.json", "r") as f:
    prd_data = json.load(f)
```

### Option 3: Python API
```python
from agents.designer import DesignerAgent
from models.prd import PRD
from utils.claude_client import ClaudeClient

client = ClaudeClient()
designer = DesignerAgent(client)

prd = PRD(
    title="My System",
    description="...",
    level="product",
    objectives=["..."],
    user_stories=["..."],
    requirements=["..."],
    success_metrics=["..."],
    constraints=["..."]
)

design = designer.design_from_prd(prd)

# Access all design elements
print(f"Components: {len(design.components)}")
print(f"State Machines: {len(design.state_machines)}")
print(f"Data Paths: {len(design.data_paths)}")
print(f"Control Paths: {len(design.control_paths)}")
print(f"Call Stacks: {len(design.call_stacks)}")
print(f"API Endpoints: {len(design.api_endpoints)}")
print(f"Examples: {len(design.examples)}")
```

## What Makes a Good PRD for Comprehensive Design

### For State Machines
Include requirements that mention:
- Status tracking
- Lifecycle management
- Workflow processes
- State transitions

### For Data Paths
Include requirements that mention:
- Data flow
- Transformations
- Validation
- Data movement between components

### For Control Paths
Include requirements that mention:
- Business logic
- Decision making
- Conditional processing
- Error handling

### For Call Stacks
Include requirements that mention:
- API operations
- Function interactions
- Service communication
- Operation sequences

### For Detailed APIs
Include requirements that mention:
- REST/GraphQL endpoints
- Request/response formats
- Authentication
- API operations

### For Examples
More complex and realistic PRDs naturally lead to better examples

## Design Quality Tips

### 1. Be Specific in PRD
❌ "The system should handle orders"
✅ "The system should process orders through states: pending → confirmed → processing → shipped → delivered"

### 2. Include Success Metrics
❌ "Fast response time"
✅ "API response time < 500ms for 95th percentile"

### 3. Specify Integrations
❌ "Payment processing"
✅ "Payment gateway integration with Stripe/PayPal, including webhook handling for async confirmations"

### 4. Define Constraints
❌ "Scalable system"
✅ "Must support 10,000 concurrent orders, use Redis for queuing, implement circuit breakers"

## Output Files

The Designer creates:
- `data/design_output.json` - Complete design in JSON format
- Console output - Formatted summary for quick review

## Design Review Checklist

Before marking `human_reviewed: true`:

- [ ] Architecture pattern is appropriate
- [ ] All components have clear responsibilities
- [ ] State machines cover all states and transitions
- [ ] Data paths show complete flow
- [ ] Control paths handle errors
- [ ] Call stacks are logical
- [ ] API endpoints are RESTful
- [ ] Examples are practical
- [ ] Security is addressed
- [ ] Scalability is addressed

## Next Steps After Design

1. **Review the Design**
   ```bash
   cat data/design_output.json | python -m json.tool
   ```

2. **Mark as Reviewed**
   Edit `data/design_output.json`:
   ```json
   {
     "human_reviewed": true,
     "review_notes": "Approved with minor suggestions..."
   }
   ```

3. **Run Planner**
   ```bash
   python run_planner.py
   ```

4. **Run Full Workflow**
   ```bash
   python main.py --prd examples/complex_prd.json
   ```

## Troubleshooting

### Issue: Missing State Machines
**Cause:** PRD doesn't mention states or workflows
**Solution:** Add requirements about status tracking or lifecycle management

### Issue: No API Details
**Cause:** PRD doesn't specify endpoints
**Solution:** Include specific API requirements (GET /users, POST /orders, etc.)

### Issue: Generic Examples
**Cause:** PRD is too simple or vague
**Solution:** Use more complex, realistic PRDs with specific scenarios

### Issue: Design Too Simple
**Cause:** Feature-level PRD instead of product-level
**Solution:** Use product-level PRD for comprehensive designs

## Examples

### Simple Feature PRD → Basic Design
- 2-3 components
- 0-1 state machines
- Simple APIs
- 1-2 examples

### Complex Product PRD → Comprehensive Design
- 8-12 components
- 2-4 state machines
- Detailed data/control paths
- Multiple call stacks
- 10-20 API endpoints
- 3-5 practical examples

## Performance

- Simple PRD: ~30-60 seconds
- Complex PRD: ~60-120 seconds
- Uses Claude Sonnet 4.5 (balanced speed/quality)
- Output size: 50-200KB JSON

## Cost Estimation

Based on Anthropic pricing:
- Input: ~2K tokens (PRD)
- Output: ~4-8K tokens (design)
- Cost: ~$0.06-0.12 per design

For 100 designs: ~$6-12

## Best Practices

1. **Start Simple**: Test with `sample_prd.json` first
2. **Iterate**: Review and refine the PRD based on design output
3. **Be Specific**: More detailed PRDs = better designs
4. **Include Metrics**: Quantifiable success criteria
5. **Define Constraints**: Technical limitations upfront
6. **Review Thoroughly**: Always human-review before planning

## Related Documentation

- [USAGE.md](../USAGE.md) - General usage guide
- [examples/README.md](../examples/README.md) - PRD examples
- [INSTALL.md](../INSTALL.md) - Installation guide
