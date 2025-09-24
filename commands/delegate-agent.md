# Agent-First Task Delegation Command

## Command: `/delegate-agent`

**Purpose:** Enforce agent delegation as the primary execution strategy for all tasks.

## Core Principle

**Always delegate to specialized agents instead of direct execution.**

When this command is active, follow this strict hierarchy:
1. **Analyze** - Understand the task domain and requirements
2. **Identify** - Find the most suitable specialized agent(s)
3. **Delegate** - Invoke the appropriate agent(s)
4. **Monitor** - Track execution and results

## Delegation Strategy

### Task Analysis Protocol
For every user request:
1. **Invoke juvenile-agent-task-matcher** to find suitable agent(s)
2. **Handle matcher response**:
   - If "AGENT: [name]" → Delegate to that agent immediately
   - If "NO MATCH" → Proceed to fallback analysis
3. **Fallback for NO MATCH cases**:
   - Decompose task and try matching individual components
   - Consider if multiple agents could collaborate
   - Only execute directly as last resort (with user approval)

### Execution Rules

```yaml
delegation_priorities:
  1: "Specialized agent matching task domain"
  2: "Multiple specialized agents for complex tasks"
  3: "Consolidated agents for cross-domain tasks"
  4: "Direct execution ONLY if no suitable agent exists"

parallel_execution:
  - "Batch independent tasks for concurrent agent execution"
  - "Use Task tool with multiple simultaneous invocations"

quality_control:
  - "Explain agent selection reasoning"
  - "Report any agent limitations encountered"
  - "Suggest improvements when agents fall short"
```

### When to Execute Directly

Only bypass agent delegation when:
1. User explicitly requests "do this yourself without agents"
2. Task is purely conversational with no technical work
3. Task involves reviewing agent outputs
4. No agent exists AND user approves direct execution

### Delegation Benefits

- **Token Conservation**: Specialized agents use optimized prompts
- **Expertise Leverage**: Domain-specific knowledge and best practices
- **Parallel Processing**: Multiple agents can work simultaneously
- **Consistency**: Agents follow standardized approaches
- **Scalability**: Easy to add new capabilities via new agents

## Usage Examples

```markdown
User: "Build a REST API"
Claude: [Invokes juvenile-agent-task-matcher]
Matcher returns: "AGENT: juvenile-api-gateway-architect | Reason: API design expertise"
→ Delegating to juvenile-api-gateway-architect for REST API design.

User: "Analyze error logs"
Claude: [Invokes juvenile-agent-task-matcher]
Matcher returns: "AGENT: juvenile-log-analyzer | Reason: Log analysis specialist"
→ Delegating to juvenile-log-analyzer for error investigation.

User: "Tell me about the weather"
Claude: [Invokes juvenile-agent-task-matcher]
Matcher returns: "NO MATCH | Reason: No agent for weather information"
→ This is an information request with no suitable agent. Would you like me to handle this directly?
```


## Key Reminders

- **Default to delegation** - Direct execution should be the exception
- **Trust agent expertise** - Specialized agents have domain knowledge
- **Batch when possible** - Multiple agents can work in parallel
- **Explain decisions** - Always clarify which agent handles what
- **Adapt dynamically** - Select agents based on task requirements, not fixed mappings

---

**Remember:** The goal is to maximize delegation to specialized agents, leveraging their expertise while conserving tokens. Every task should first be considered for delegation before any direct execution.