# Rapid Prototyping Workflow

## Overview
This workflow enables rapid creation of functional proof-of-concepts and prototypes by maximizing integration of existing resources without error handling or defensive programming.

## Purpose
- Create quick demonstrations of technical feasibility
- Build proof-of-concepts for stakeholder review
- Validate integration approaches without production overhead
- Generate working examples for documentation

## When to Use
- **✅ Use when:**
  - Need quick proof-of-concept
  - Demonstrating integration possibilities
  - Creating examples for documentation
  - Validating technical approaches
  - Building throwaway prototypes

- **❌ Don't use when:**
  - Building production systems
  - Code requires error handling
  - Security is critical
  - Performance optimization needed
  - Edge cases must be handled

## Workflow Steps

### 1. Requirements Analysis
**Agent:** `juvenile-requirements-analyst` (optional)
- Clarify prototype objectives
- Identify available resources
- Define success criteria
- Document assumptions

### 2. Resource Discovery
**Agent:** `juvenile-prototype-integrator`
- Scan for available libraries and tools
- Identify existing utilities in codebase
- Map integration points
- List available APIs and services

### 3. Prototype Implementation
**Agent:** `juvenile-prototype-integrator`
- Create happy-path implementation
- Integrate existing resources directly
- Write minimal glue code
- Assume all operations succeed
- No error handling or validation

### 4. Integration Demonstration
**Agent:** `juvenile-prototype-integrator`
- Execute prototype on sample data
- Generate output artifacts
- Document integration flow
- Show functionality achieved

### 5. Documentation (Optional)
**Agent:** `optimized-document-task-assistant`
- Create usage examples
- Document integration approach
- List resources utilized
- Note prototype limitations

## Key Principles

### Happy-Path Focus
- Assume all inputs are valid
- Assume all services are available
- No try-except blocks
- No validation logic
- Direct method calls without guards

### Resource Maximization
- Use existing libraries over custom code
- Leverage built-in functions
- Integrate available tools directly
- Minimize custom implementation

### Speed Over Robustness
- Prioritize quick delivery
- Focus on demonstrating capability
- Ignore edge cases
- Skip defensive programming
- No performance optimization

## Example Scenarios

### Data Processing Pipeline
```
Input: CSV file with sales data
Resources: pandas, numpy installed
Output: Statistical analysis JSON

Approach:
1. Load CSV directly with pandas
2. Use built-in aggregation functions
3. Generate statistics with numpy
4. Export results to JSON
```

### API Integration Bridge
```
Input: Multiple API endpoints
Resources: requests library, JSON data
Output: Unified dashboard

Approach:
1. Fetch data from APIs directly
2. Merge JSON responses
3. Create combined data structure
4. Output unified result
```

### Database Web Service
```
Input: SQLite database
Resources: Flask, sqlite3
Output: REST API

Approach:
1. Connect to database directly
2. Create Flask endpoints
3. Map queries to JSON
4. Return results without validation
```

## Common Patterns

### Direct File Operations
```python
# Happy path - no checks
data = json.load(open('file.json'))
df = pd.read_csv('data.csv')
results = process(data)
json.dump(results, open('output.json', 'w'))
```

### Straight-Through Processing
```python
# No error handling
def process_data(input_file):
    data = load_data(input_file)
    transformed = transform(data)
    analyzed = analyze(transformed)
    return save_results(analyzed)
```

### Direct Integration
```python
# Assume everything works
api_data = requests.get(api_url).json()
db_data = query_database(connection)
combined = merge_data(api_data, db_data)
publish_results(combined)
```

## Success Criteria

✅ **Prototype is successful when:**
- Core functionality is demonstrated
- Integration between components works
- Output is generated for happy path
- Resources are effectively utilized
- Code is minimal and readable

❌ **Prototype should NOT:**
- Include error handling
- Validate inputs or outputs
- Handle edge cases
- Optimize performance
- Be production-ready

## Output Artifacts

Typical prototype outputs:
- Working script/application
- Sample output data
- Integration demonstration
- Usage example
- Resource utilization report

## Limitations & Warnings

⚠️ **Important:**
- Prototypes are NOT production-ready
- No security considerations
- No error recovery
- Assumes perfect conditions
- May fail with unexpected inputs
- Not suitable for critical systems

## Related Workflows

- **[comprehensive-code-review.md](./comprehensive-code-review.md)** - For converting prototype to production code
- **[testing-automation.md](./testing-automation.md)** - For adding proper testing after prototyping
- **[systematic-debugging.md](./systematic-debugging.md)** - For troubleshooting when prototype evolves

## Key Agents

Primary:
- `juvenile-prototype-integrator` - Core prototyping specialist

Supporting:
- `juvenile-requirements-analyst` - Requirements clarification
- `optimized-document-task-assistant` - Documentation creation
- `consolidated-fullstack-data-engineer` - If prototype needs evolution