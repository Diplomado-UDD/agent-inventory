# ADK Evaluation Sets Guide

## What Are Eval Sets?

Eval sets are test suites that help you:
- Systematically test your agent's responses
- Ensure consistency across different versions
- Catch regressions when making changes
- Validate agent behavior matches expectations

## Creating an Eval Set

### 1. File Location
Create JSON files in: `inventory_system/eval_sets/`

### 2. Basic Structure

```json
{
  "name": "Your Test Suite Name",
  "description": "What this tests",
  "eval_cases": [
    {
      "id": "unique_test_id",
      "input": "User message to test",
      "expected_output": "Expected text in response (optional)",
      "expected_tools": ["tool_name1", "tool_name2"],
      "expected_behavior": "Description of what should happen",
      "tags": ["category1", "category2"]
    }
  ]
}
```

### 3. Example Test Case

```json
{
  "id": "test_stock_check",
  "input": "How many Laptops do we have?",
  "expected_output": "5",
  "expected_tools": ["check_inventory"],
  "expected_behavior": "Should check inventory and return current stock",
  "tags": ["stock_check", "basic"]
}
```

## Running Eval Sets

### Via Web UI
1. Go to the **Eval** tab in the ADK web interface
2. Click **"Run Evaluation"**
3. Select your eval set
4. View results and metrics

### Via Command Line

```bash
# Run all eval sets
uv run python -m google.adk.cli eval inventory_system

# Run specific eval set
uv run python -m google.adk.cli eval inventory_system --eval-set basic_inventory_tests

# Save results
uv run python -m google.adk.cli eval inventory_system --output results.json
```

## Eval Set Fields

- **id**: Unique identifier for the test case
- **input**: The user message to send to the agent
- **expected_output**: Text that should appear in the response (partial match)
- **expected_tools**: List of tools the agent should call
- **expected_behavior**: Human-readable description of expected behavior
- **tags**: Categories for organizing and filtering tests

## Best Practices

1. **Cover all capabilities**: Test each tool and workflow
2. **Test edge cases**: Empty inputs, off-topic requests, ambiguous queries
3. **Test guard rails**: Verify agent rejects inappropriate requests
4. **Multilingual**: Test different languages if supported
5. **Update regularly**: Add new tests when fixing bugs or adding features

## Example Eval Set

See `inventory_system/eval_sets/basic_inventory_tests.json` for a complete example with:
- Greeting tests
- Stock checking (all products)
- Restocking workflow
- Off-topic rejection
- Multilingual support

## Viewing Results

After running evals, you'll see:
- ✅ **Pass/Fail** for each test
- **Tool calls made** vs expected
- **Response content** vs expected
- **Execution time**
- **Overall metrics** (accuracy, tool precision, etc.)
