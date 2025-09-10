# Finite State Machine Command

## Command: `/agent-state-machine --session [start/end] --mode [orchestrator/interactive/response] --path [directory_path]`

**Purpose:** Implement a finite state machine where agents are states and transitions follow agent descriptions.

## Command Parameters

```yaml
--session:
  start: "Initialize state machine session"
  end: "Terminate state machine session, return to normal operation"

--mode:
  orchestrator: "Agents return to MAIN after completion (implemented)"
  interactive: "Agents can transition to other agents directly (planned)"
  response: "No MAIN state, agents respond to messages in directory (planned)"

--path [directory_path]:
  structure:
    [directory_path]/main/: "MAIN state temporary files"
    [directory_path]/[agent]/: "Agent workspace and messages"
    [directory_path]/state.jsonl: "State history and current state"
```

## State Definitions

```yaml
MAIN:
  capabilities:
    write: ["*.md", "*.txt", 'any un-excutable files']
    read: ["any file", "system info (ls, pwd, git status)", "any get info function"]
    execute: ["planning", "coordinate", "pattern matching", "conversation"]
  restrictions:
    cannot_write: ["*.py", "*.js", "*.sh", "configs", 'any executable files']
    cannot_execute: ["modifying commands", "code execution", "system changes"]
    
AGENT_STATES:
  entry: "Agent description defines entry patterns"
  capabilities: "Full execution within specialization"
  exit:
    orchestrator: "Always → MAIN"
    interactive: "Can → another agent or MAIN"
    response: "No mandatory exit"
```

## Transition Function δ

### Core Insight: Agent Descriptions ARE Transition Functions

Each agent's description IS the condition for entering that state. No manual transition tables needed.

```yaml
example:
  agent: "juvenile-database-architect"
  description: "Use for database design, query optimization"
  # This description automatically becomes the transition condition!
```

### Mode Behaviors

#### Orchestrator Mode
```
MAIN → [input matches agent description] → Agent → [complete] → MAIN
```

#### Interactive Mode  
```
MAIN → Agent_i → [needs help] → Agent_j → Agent_k → MAIN
```

#### Response Mode
```
Queue → [message matches description] → Agent → Result → Queue
```

## State Persistence

First entry in `[directory_path]/state.jsonl` MUST be initialization:

```jsonl
{"timestamp": "2024-01-01T10:00:00", "type": "session_init", "state": "MAIN", "parameters": {"mode": "orchestrator", "path": "[directory_path]"}, "agent_descriptions": "/root/.claude/data/AGENT_DIRECTORY.md", "permissions": {"can_write": ["*.md", "*.txt", "*.log", "*.json", "*.csv"], "cannot_write": ["*.py", "*.js", "*.ts", "*.sh", "*.go", "*.rs", "*.c", "*.cpp", "*.java", "package.json", "requirements.txt", "Dockerfile", "Makefile", "any executable file"], "can_execute": ["read", "list", "search", "analyze", "and get info function"],"cannot_execute": ["run", "exec", "eval", "compile", "build"]}}
{"timestamp": "2024-01-01T10:00:15", "type": "transition", "state": "[agent-name]", "trigger": "[match-agent-description]", "previous": "MAIN", "permissions": {"can_write": ["*"], "can_execute": ["*"]}}
{"timestamp": "2024-01-01T10:02:00", "type": "transition", "state": "MAIN", "trigger": "task completed", "previous": "[agent-name]", "permissions": {"can_write": ["*.md", "*.txt", "*.log", "*.json", "*.csv"], "cannot_write": ["*.py", "*.js", "*.ts", "*.sh", "*.go", "*.rs", "*.c", "*.cpp", "*.java", "package.json", "requirements.txt", "Dockerfile", "Makefile", "any executable file"], "can_execute": ["read", "list", "search", "analyze", "and get info function"],"cannot_execute": ["run", "exec", "eval", "compile", "build"]}}
```

Required fields:
- `state`: Current state ("MAIN" or agent name)
- `type`: "session_init" or "transition"
- `parameters`: (first entry only) mode, path
- `agent_descriptions`: (first entry only) path to AGENT_DIRECTORY.md
- `permissions`: Current state permissions
  - `can_write`: File patterns this state can write
  - `cannot_write`: File patterns this state MUST NOT write (overrides can_write)
  - `can_execute`: Operations this state can perform
  - `cannot_execute`: Operations this state MUST NOT perform (overrides can_execute)

## Initialization Process

When executing `/agent-state-machine --session start --mode [mode] --path [directory_path]`:

1. **Generate Agent List**: Run `/root/.claude/scripts/generate-agent-list.py` to get latest agent descriptions

2. **Create Directory Structure** based on mode:
   - **orchestrator mode**: 
     - Create `[directory_path]/main/` for MAIN state workspace
   - **interactive mode**: 
     - Create `[directory_path]/main/` for MAIN state workspace
     - Create `[directory_path]/[agent-name]/` for each agent workspace
   - **response mode**: 
     - Create `[directory_path]/response/` for message queue
     - Create `[directory_path]/[agent-name]/` for each agent workspace

3. **Initialize state.jsonl** with:
   - Session parameters (mode, path)
   - Agent descriptions file location (`/root/.claude/data/AGENT_DIRECTORY.md`)
   - Initial state: "MAIN" (except response mode)

## Execution Flow

1. **Initialize**: Load parameters and agent descriptions from state.jsonl
2. **Match**: Check input against all agent descriptions
   - Match found → go to step 3
   - No match → stay in MAIN (no state.jsonl update needed)
3. **Transition**: Only when state changes, append to state.jsonl:
   ```json
   {"timestamp": "[ISO_TIME]", "type": "transition", "state": "[NEW_STATE]", "trigger": "[MATCH_REASON]", "previous": "[OLD_STATE]"}
   ```
   And display: `[OLD_STATE → NEW_STATE]`
4. **Execute**: Invoke agent or handle in MAIN (MAIN cannot write executable files)
5. **Return**: When agent completes and transitions back to MAIN (or another state), append new transition entry to state.jsonl

## Example Usage

```bash
/agent-state-machine --session start --mode orchestrator --path /root/.claude/agent-state-machine/20250910

# System initializes:
# 1. Runs generate-agent-list.py
# 2. Creates directory structure
# 3. Initializes state.jsonl with parameters and agent descriptions path
# [State: MAIN]

User: "Hello, what can you help with?"
# No agent match, stays in MAIN
[State: MAIN] I can help with planning, coordination, and various technical tasks...

User: "Write a hello world Python script"
[MAIN → FULLSTACK_ENGINEER]  # Matched: "write" + "Python"
# MAIN cannot write *.py files, must delegate
[FULLSTACK_ENGINEER → MAIN]  # Task completed

User: "Thanks!"
[State: MAIN] You're welcome!
```

## Implementation Protocol

```markdown
You operate as a finite state machine with strict state enforcement:

### State Initialization
- Parameters: [Read from state.jsonl first entry]
- Current state: [Read from state.jsonl latest entry]
- Transitions: Agent descriptions define entry conditions

### MAIN State Tool Restrictions
When current_state == "MAIN", STRICTLY ENFORCE:

ALLOWED Tools:
- Read: Any files, system info
- Write: ONLY *.md, *.txt, non-executable files
- Glob, Grep, WebSearch, WebFetch: Information gathering
- TodoWrite: Task management
- Task: Delegate to agents (PRIMARY ACTION for restricted operations)

BLOCKED Tools (MUST delegate to agent):
- Bash: Code execution commands (python, node, npm, etc.)
- Write/Edit: Executable files (*.py, *.js, *.sh, configs)
- MultiEdit: On executable files
- NotebookEdit: Jupyter notebook modifications

### Violation Handling Protocol
If user requests blocked action in MAIN state:
1. RECOGNIZE: "This requires [capability], which MAIN cannot perform"
2. TRANSITION: Match to appropriate agent OR suggest agent creation
3. DELEGATE: Use Task tool to invoke agent
4. LOG: Record state transition in state.jsonl

### State Transition Display
Show all transitions: [STATE_A → STATE_B]
Log all transitions to state.jsonl with trigger reason
```

---

**Key Point:** Agent descriptions automatically define state transitions - no manual configuration needed.