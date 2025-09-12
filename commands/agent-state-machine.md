# Finite State Machine Command

## Command: `/agent-state-machine [--session start/end] [--mode orchestrator/interactive/response] [--path directory_path]`

**Purpose:** Implement a finite state machine where agents are states and transitions follow agent descriptions.

## Default Values

```yaml
defaults:
  --session: start  # If omitted, defaults to "start"
  --mode: orchestrator  # If omitted, defaults to "orchestrator"
  --path: ./.claude/agent-state-machine/[YYYYMMDD_HHMMSS]  # If omitted, uses current directory with timestamp
```

## Command Parameters

```yaml
--session: (optional, default: start)
  start: "Initialize state machine session"
  end: "Terminate state machine session, return to normal operation"

--mode: (optional, default: orchestrator)
  orchestrator: "Agents return to MAIN after completion (implemented)"
  interactive: "Agents can transition to other agents directly (planned)"
  response: "No MAIN state, agents respond to messages in directory (planned)"

--path: (optional, default: ./.claude/agent-state-machine/[timestamp])
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
  workspace: "[directory_path]/main/"
    primary: "All generated files MUST be in main's workspace"
    exceptions: "User's explicit project paths take precedence"
    temp_files: "Use workspace for all temporary/intermediate files"
    
AGENT_STATES:
  entry: "Agent description defines entry patterns"
  capabilities: "Full execution within specialization"
  workspace: "[directory_path]/agent/[agent-name]/"
  workspace_rules:
    primary: "All generated files MUST be in agent's workspace"
    exceptions: "User's explicit project paths take precedence"
    temp_files: "Use workspace for all temporary/intermediate files"
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
{"timestamp": "[CURRENT_ISO_TIMESTAMP]", "type": "session_init", "state": "MAIN", "parameters": {"mode": "orchestrator", "path": "[directory_path]"}, "agent_descriptions": "/root/.claude/data/AGENT_DIRECTORY.md", "agent_list": "[directory_path]/agent-list.txt", "workspace": "[directory_path]/main/", "permissions": {"can_write": ["*.md", "*.txt", "*.log", "*.json", "*.csv", "non-executable files"], "cannot_write": ["*.py", "*.js", "*.ts", "*.sh", "*.go", "*.rs", "*.c", "*.cpp", "*.java", "package.json", "requirements.txt", "Dockerfile", "Makefile", "any executable file"], "can_execute": ["read", "list", "search", "analyze", "and get info function"],"cannot_execute": ["run", "exec", "eval", "compile", "build"]}}
{"timestamp": "[CURRENT_ISO_TIMESTAMP]", "type": "transition", "state": "[agent-name]", "trigger": "[match-agent-description]", "previous": "MAIN", "workspace": "[directory_path]/agent/[agent-name]/", "permissions": {"can_write": ["*"], "can_execute": ["*"]}}
{"timestamp": "[CURRENT_ISO_TIMESTAMP]", "type": "transition", "state": "MAIN", "trigger": "task completed", "previous": "[agent-name]", "workspace": "[directory_path]/main/", "permissions": {"can_write": ["*.md", "*.txt", "*.log", "*.json", "*.csv", "non-executable files"], "cannot_write": ["*.py", "*.js", "*.ts", "*.sh", "*.go", "*.rs", "*.c", "*.cpp", "*.java", "package.json", "requirements.txt", "Dockerfile", "Makefile", "any executable file"], "can_execute": ["read", "list", "search", "analyze", "and get info function"],"cannot_execute": ["run", "exec", "eval", "compile", "build"]}}
```

**Note:** `[CURRENT_ISO_TIMESTAMP]` should be the actual current time in ISO format (e.g., "2025-01-12T09:15:30"), generated dynamically using `date +"%Y-%m-%dT%H:%M:%S"`

Required fields:
- `state`: Current state ("MAIN" or agent name)
- `type`: "session_init" or "transition"
- `parameters`: (first entry only) mode, path
- `agent_descriptions`: (first entry only) path to AGENT_DIRECTORY.md
- `workspace`: Current state's workspace directory
- `permissions`: Current state permissions
  - `can_write`: File patterns this state can write
  - `cannot_write`: File patterns this state MUST NOT write (overrides can_write)
  - `can_execute`: Operations this state can perform
  - `cannot_execute`: Operations this state MUST NOT perform (overrides can_execute)

## Initialization Process

When executing `/agent-state-machine` (uses defaults) or with explicit parameters:

0. **Apply Default Values** (if parameters not provided):
   - `--session`: If not specified → use `start`
   - `--mode`: If not specified → use `orchestrator`
   - `--path`: If not specified → generate `./.claude/agent-state-machine/[YYYYMMDD_HHMMSS]` based on current timestamp (first get system's current time)

1. **Generate Agent List**: Run `python3 /root/.claude/scripts/generate-agent-list.py [directory_path]` to generate agent list at `[directory_path]/agent-list.txt` and agent descriptions at `[directory_path]/AGENT_DIRECTORY.md`

2. **Create Directory Structure**:
  - Create `[directory_path]/main/` for MAIN state and AGENT state workspace
  - Create `[directory_path]/message_deque/` for message queue
  - Method: Parse agent names from `[directory_path]/agent-list.txt` and create directories directly:
    ```bash
    mkdir -p [directory_path]/main
    mkdir -p [directory_path]/message_deque
    mkdir -p [directory_path]/agent/[agent_name1] [directory_path]/agent/[agent_name2] ... # all agent names
    ```

3. **Initialize state.jsonl** with:
   - Session parameters (mode, path)
   - Agent descriptions file location (`/root/.claude/data/AGENT_DIRECTORY.md`)
   - Agent list file location (`/root/.claude/data/agent-list.txt`)
   - Initial state: "MAIN" (except response mode)

4. **Display Initialization Status**:
   ```yaml
   🚀 Agent State Machine Initialized

   [State: MAIN]

   Session Parameters:
     Mode: [orchestrator/interactive/response]
     Path: [directory_path]
     Session: start
     
   Available Agents: [N] agents loaded
     ✓ State persistence: [directory_path]/state.jsonl
     ✓ Agent descriptions: [directory_path]/AGENT_DIRECTORY.md
     ✓ MAIN Workspace: [directory_path]/main/
     ✓ Agent Workspaces: [directory_path]/agent/[agent-name]/

   MAIN State Permissions:
     Can Write: [permissions.can_write from state.jsonl]
     Cannot Write: [permissions.cannot_write from state.jsonl]
     Can Execute: [permissions.can_execute from state.jsonl]
     Cannot Execute: [permissions.cannot_execute from state.jsonl]
   ```

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
# Using all defaults (most common)
/agent-state-machine
# Equivalent to: /agent-state-machine --session start --mode orchestrator --path ./.claude/agent-state-machine/20250912_143022

# Using defaults with custom path
/agent-state-machine --path /custom/path

# Explicit parameters
/agent-state-machine --session start --mode orchestrator --path /root/.claude/agent-state-machine/20250910

# System initializes:
# 1. Runs python3 /root/.claude/scripts/generate-agent-list.py [directory_path]
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

### Workspace Enforcement Protocol
For ALL states (MAIN and AGENT):

#### MAIN State Workspace Rules:
1. DEFAULT WORKSPACE: [directory_path]/main/
2. FILE CREATION: All MAIN-generated files go to workspace → [directory_path]/main/[file_name]
3. TEMP FILES: Always use main workspace
4. EXCEPTIONS: Only when user provides explicit paths

#### AGENT State Workspace Rules:
1. DEFAULT WORKSPACE: [directory_path]/agent/[agent-name]/
2. FILE CREATION: All Agent-generated files go to workspace → [directory_path]/agent/[agent-name]
3. TEMP FILES: Always use agent workspace
4. EXCEPTIONS: Only when user provides explicit paths

#### WORKSPACE ORGANIZATION:
```
[directory_path]/main/           # MAIN workspace
└── [any files MAIN creates]    # Whatever MAIN needs to write

[directory_path]/agent/[agent-name]/  # Agent workspace
└── [any files Agent creates]   # Whatever Agent needs to write
```

Example enforcement:
- MAIN: Creates any file → [directory_path]/main/[file_name]
- Agent: "Create a test script" → Creates: [directory_path]/agent/fullstack-engineer/test_script.py
- NOT: ./test_script.py or /tmp/test_script.py (unless user specifies)
```

---

**Key Point:** Agent descriptions automatically define state transitions - no manual configuration needed.