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
  interactive: "Agents can transition to other agents directly (planned)" (planned)
  response: "No MAIN state, agents respond to messages in directory (planned)" (planned)

--path: (optional, default: ./.claude/agent-state-machine/[YYYYMMDD_HHMMSS])
  structure:
    [directory_path]/conversations/: "Conversation-based organization"
    [directory_path]/conversations/messages.jsonl: "Conversation index (summary)"
    [directory_path]/conversations/conv_[NNN]/dialogue.md: "Full conversation with thinking"
    [directory_path]/conversations/conv_[NNN]/outputs/: "Conversation outputs"
    [directory_path]/state.jsonl: "State history and current state"
```

## State Definitions

```yaml
MAIN:
  capabilities:
    write: "Non-executable files only (see MAIN_PERMISSIONS)"
    read: ["any file", "system info (ls, pwd, git status)", "information-gathering functions only"]
    execute: ["planning", "coordinate", "pattern matching", "conversation"]
  restrictions: "See MAIN_PERMISSIONS for detailed restrictions"

AGENT_STATES:
  entry: "Agent description defines entry patterns"
  capabilities: "Full execution within specialization"
  exit:
    orchestrator: "Always → MAIN"
    interactive: "Can → another agent or MAIN"
    response: "No mandatory exit"
```

## Permission Definitions

```yaml
MAIN_PERMISSIONS:
  can_write: ["*.md", "*.txt", "*.log", "*.json", "*.csv", "non-executable files"]
  cannot_write: ["*.py", "*.js", "*.ts", "*.sh", "*.go", "*.rs", "*.c", "*.cpp", "*.java", "package.json", "requirements.txt", "Dockerfile", "Makefile", "any executable file"]
  can_execute: ["read", "list", "search", "analyze", "information-gathering functions only"]
  cannot_execute: ["run", "exec", "eval", "compile", "build"]

AGENT_PERMISSIONS:
  can_write: ["*"]  # Full write access within specialization
  can_execute: ["*"]  # Full execution capabilities
```

## Workspace Management

```yaml
workspace_structure:
  conversations: "[directory_path]/conversations/"
  active_conversation: "[directory_path]/conversations/conv_[NNN]/"  # NNN starts from 001, increments for each new conversation
  outputs: "[directory_path]/conversations/conv_[NNN]/outputs/"
  dialogue: "[directory_path]/conversations/conv_[NNN]/dialogue.md"
  messages_index: "[directory_path]/conversations/messages.jsonl"
  state_tracking: "[directory_path]/state.jsonl"

workspace_rules:
  conversation_based:
    primary: "All generated files go to conversation outputs"
    path: "[directory_path]/conversations/conv_[NNN]/outputs/"
    temp_files: "Use conversation outputs for temporary files"
    exceptions: "User's explicit project paths take precedence"
    dialogue_recording: "All thinking and actions recorded in dialogue.md"

  both_main_and_agents:
    shared_workspace: "[directory_path]/conversations/conv_[NNN]/outputs/"
    no_separation: "MAIN and agents share the same output directory"
    organization: "Files organized by task/purpose, not by state"

workspace_organization:
  structure: |
    [directory_path]/
    ├── conversations/
    │   ├── conv_001/
    │   │   ├── dialogue.md      # Full conversation record
    │   │   └── outputs/         # All generated files
    │   │       ├── [file1.py]   # Agent-generated
    │   │       ├── [file2.md]   # MAIN-generated
    │   │       └── [temp.txt]   # Any temporary files
    │   ├── conv_002/
    │   │   ├── dialogue.md
    │   │   └── outputs/
    │   └── messages.jsonl       # Conversation index
    └── state.jsonl              # State persistence
```

## Messages Index (messages.jsonl)

Each conversation is recorded as one line in `[directory_path]/conversations/messages.jsonl` using **Python logger script**:

```json
{"conversation_id": "conv_[NNN]", "timestamp": "[YYYY-MM-DD]T[HH:MM:SS]", "summary": "User asked about Hello World history and created hello_world.py", "files_created": [{"path": "[directory_path]/conversations/conv_[NNN]/outputs/hello_world.py", "summary": "Classic Hello World Python script"}], "agents_used": ["consolidated-fullstack-data-engineer"]}
```

### Recording Method
Use the Python script `/root/.claude/scripts/simple_asm_logger.py` with JSON input to handle spaces and special characters properly:
```bash
echo '<json_data>' | python3 /root/.claude/scripts/simple_asm_logger.py
```

### Field Definitions
- `conversation_id`: Conversation identifier
- `timestamp`: Conversation start time
- `summary`: Brief description of conversation content
- `files_created`: Array of `{path: string, summary: string}` objects for generated files
- `agents_used`: List of agents involved in the conversation

### Logger Location
`/root/.claude/scripts/simple_asm_logger.py` - Lightweight Python script for conversation logging

### Messages Index Maintenance
Use Python logger to record conversation at completion:
```bash
# Using JSON input (recommended - handles spaces and special characters)
echo '{
    "session_path": "[directory_path]",
    "conversation_data": {
        "conversation_id": "conv_[NNN]",
        "timestamp": "[YYYY-MM-DD]T[HH:MM:SS]",
        "summary": "Task description",
        "files_created": [{"path": "[directory_path]/conversations/conv_[NNN]/outputs/file.py", "summary": "Description"}],
        "agents_used": ["agent1"]
    }
}' | python3 /root/.claude/scripts/simple_asm_logger.py
```
- Python script handles JSONL formatting and file operations
- JSON input avoids command line parsing issues with spaces
- Logger focuses only on recording conversations to messages.jsonl

## Transition Function δ

### Agent Descriptions ARE Transition Functions

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

#### Interactive Mode (planned)
```
MAIN → Agent_i → [needs help] → Agent_j → Agent_k → MAIN
```

#### Response Mode (planned)
```
Queue → [message matches description] → Agent → Result → Queue
```

## State Persistence

First entry in `[directory_path]/state.jsonl` MUST be initialization:

```jsonl
{"timestamp": "[YYYY-MM-DD]T[HH:MM:SS]", "type": "session_init", "state": "MAIN", "parameters": {"mode": "orchestrator", "path": "[directory_path]"}, "agent_descriptions": "[directory_path]/AGENT_DIRECTORY.md", "agent_list": "[directory_path]/agent-list.txt", "workspace": "[directory_path]/conversations/conv_[NNN]/outputs/", "permissions": "[MAIN_PERMISSIONS - see Permission Definitions section]"}
{"timestamp": "[YYYY-MM-DD]T[HH:MM:SS]", "type": "transition", "state": "[agent-name]", "trigger": "[match-agent-description]", "previous": "MAIN", "workspace": "[directory_path]/conversations/conv_[NNN]/outputs/", "permissions": "[AGENT_PERMISSIONS - see Permission Definitions section]"}
{"timestamp": "[YYYY-MM-DD]T[HH:MM:SS]", "type": "transition", "state": "MAIN", "trigger": "task completed", "previous": "[agent-name]", "workspace": "[directory_path]/conversations/conv_[NNN]/outputs/", "permissions": "[MAIN_PERMISSIONS - see Permission Definitions section]"}
```

Required fields:
- `state`: Current state ("MAIN" or agent name)
- `type`: "session_init" or "transition"
- `parameters`: (first entry only) mode, path
- `agent_descriptions`: (first entry only) path to AGENT_DIRECTORY.md
- `workspace`: Current state's workspace directory
- `permissions`: Current state permissions (see Permission Definitions section for MAIN_PERMISSIONS and AGENT_PERMISSIONS)

## Initialization Process

When executing `/agent-state-machine` (uses defaults) or with explicit parameters:

0. **Apply Default Values** (if parameters not provided):
   - `--session`: If not specified → use `start`
   - `--mode`: If not specified → use `orchestrator`
   - `--path`: If not specified → generate `./.claude/agent-state-machine/[YYYYMMDD_HHMMSS]` based on current timestamp (first get system's current time)

1. **Generate Agent List**: Run `python3 /root/.claude/scripts/generate-agent-list.py [directory_path]` to generate agent list at `[directory_path]/agent-list.txt` and agent descriptions at `[directory_path]/AGENT_DIRECTORY.md`

2. **Create Base Directory Structure** (NO conversation directories yet):
  - Create base structure only:
    ```bash
    mkdir -p [directory_path]/conversations
    touch [directory_path]/conversations/messages.jsonl
    # DO NOT create any conv_XXX directories yet
    # Conversations will be created on-demand with each user input
    ```

3. **Initialize state.jsonl** with:
   - Session parameters (mode, path)
   - Agent descriptions file location (`[directory_path]/AGENT_DIRECTORY.md`)
   - Agent list file location (`[directory_path]/agent-list.txt`)
   - Initial state: "MAIN"
   - NO workspace field yet (will be set when first conversation starts)

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
     ✓ Conversations directory: [directory_path]/conversations/

   Waiting for first user input to create conversation...

   MAIN State Permissions:
     Can Write: [permissions.can_write from state.jsonl]
     Cannot Write: [permissions.cannot_write from state.jsonl]
     Can Execute: [permissions.can_execute from state.jsonl]
     Cannot Execute: [permissions.cannot_execute from state.jsonl]
   ```

## Execution Flow

### For Each User Input (Critical Change):

1. **Conversation Creation** (FIRST STEP for any user input except --session commands):
   ```bash
   # Count existing conversations
   conv_count=$(ls -d [directory_path]/conversations/conv_* 2>/dev/null | wc -l)
   next_num=$((conv_count + 1))
   conv_id=$(printf "conv_%03d" $next_num)

   # Create new conversation structure
   mkdir -p [directory_path]/conversations/$conv_id/outputs
   echo "# Conversation: $conv_id" > [directory_path]/conversations/$conv_id/dialogue.md

   # Log conversation start
   append to state.jsonl: {"type": "conversation_start", "conversation_id": "$conv_id", ...}
   ```

2. **Process Request**:
   - Load parameters and agent descriptions from state.jsonl
   - Check input against all agent descriptions
   - If match found → transition to agent state
   - Execute in MAIN or delegate to agent
   - Record all actions to current conversation's dialogue.md

3. **State Transitions** (when needed):
   ```json
   {"timestamp": "[time]", "type": "transition", "state": "[NEW_STATE]", "trigger": "[REASON]", "previous": "[OLD_STATE]"}
   ```
   Display: `[OLD_STATE → NEW_STATE]`

4. **Complete Response & Auto-Close Conversation**:
   ```bash
   # After assistant finishes responding
   append to state.jsonl: {"type": "conversation_end", "conversation_id": "$conv_id", ...}

   # Log to messages.jsonl using logger
   echo '{"conversation_id": "'$conv_id'", ...}' | python3 /root/.claude/scripts/simple_asm_logger.py
   ```

5. **Ready for Next Input**:
   - Conversation is closed
   - Next user input will trigger new conversation creation (back to step 1)

## Example Usage

```bash
# Using all defaults (most common)
/agent-state-machine
# Equivalent to: /agent-state-machine --session start --mode orchestrator --path ./.claude/agent-state-machine/[YYYYMMDD_HHMMSS]

# System initializes (NO conversation created yet):
# 1. Runs python3 /root/.claude/scripts/generate-agent-list.py [directory_path]
# 2. Creates base directory structure (conversations/ only)
# 3. Initializes state.jsonl
# [State: MAIN] - Waiting for user input...

User: "Hello, what can you help with?"
# Creates conv_001, processes, responds, closes conv_001
[State: MAIN] [Conv: 001] I can help with planning, coordination, and various technical tasks...
# conv_001 is now closed

User: "Write a hello world Python script"
# Creates conv_002
[State: MAIN] [Conv: 002]
[MAIN → FULLSTACK_ENGINEER]  # Matched: "write" + "Python"
# MAIN cannot write *.py files, must delegate
[FULLSTACK_ENGINEER → MAIN]  # Task completed
# Response complete, conv_002 is now closed

User: "Thanks!"
# Creates conv_003
[State: MAIN] [Conv: 003] You're welcome!
# conv_003 is now closed

User: "Can you explain what you just did?"
# Creates conv_004
[State: MAIN] [Conv: 004] I created a Python script that prints "Hello, World!"...
# conv_004 is now closed

# Each user input creates a new conversation with its own workspace
```

## Implementation Protocol

```markdown
You operate as a finite state machine with strict state enforcement:

### State Initialization
- Parameters: [Read from state.jsonl first entry]
- Current state: [Read from state.jsonl latest entry]
- Transitions: Agent descriptions define entry conditions

### Conversation Management (Critical Rule)
**EVERY USER INPUT = NEW CONVERSATION**
- Each user message (excluding --session commands) MUST create a new conv_[NNN]
- Assistant response completion automatically ends the conversation
- No conversation spans multiple user-assistant exchanges

#### Conversation Lifecycle:
1. **User Input Received (non-command)**:
   - Immediately check existing conv_* directories count
   - Create new conv_{count+1:03d}/ with outputs/ subdirectory
   - Append to state.jsonl: `{"type": "conversation_start", "conversation_id": "conv_XXX", ...}`
   - Set current workspace to new conversation directory

2. **Process and Respond**:
   - Execute all tasks within current conversation
   - Record everything to conv_[NNN]/dialogue.md
   - Generate all outputs to conv_[NNN]/outputs/

3. **Assistant Response Complete**:
   - Automatically append to state.jsonl: `{"type": "conversation_end", "conversation_id": "conv_XXX", ...}`
   - Log conversation summary to messages.jsonl using logger
   - Conversation is now closed
   - Next user input will create conv_[NNN+1]

### Dialogue Recording
Record in [directory_path]/conversations/conv_[NNN]/dialogue.md:
- User messages and timestamps
- MAIN thinking process before delegation
- Task tool invocations with full parameters
- Agent receiving task, thinking, and actions
- Agent reports back to MAIN
- State transitions with reasons

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

### Agent Delegation Protocol
When MAIN delegates to agents using Task tool:

**Step 1: Get current workspace path**
- Read latest entry from [directory_path]/state.jsonl to extract the `workspace` field
- This workspace path is the actual directory where the agent should store outputs
- Example: Reading state.jsonl might return `"workspace": "/root/.claude/agent-state-machine/20241218_143022/conversations/conv_001/outputs/"`

**Step 2: Pass workspace to agent in Task prompt**

**Format Template:**

    ```
    Task tool parameters:
    - subagent_type: [agent-name]
    - description: [brief task description]
    - prompt: "[MAIN state request]

    **WORKSPACE REQUIREMENTS:**
    - All generated files MUST be placed in: {workspace_from_state.jsonl}
    - Record your thinking process in: {dialogue_path_derived_from_workspace}
    - Do NOT use your default working directory or any other location, unless explicitly specified otherwise
    - Use only the specified absolute paths above for ALL file creation and documentation

    **TASK DETAILS:**

    [Here is task details]
    ```

**Example with actual paths:**

    ```
    # After reading state.jsonl and getting workspace:
    # "/root/.claude/agent-state-machine/20241218_143022/conversations/conv_001/outputs/"

    - subagent_type: "consolidated-fullstack-data-engineer"
    - description: "Create a hello_world.py"
    - prompt: "Create a hello_world.py file with print('Hello, World!')

    **WORKSPACE REQUIREMENTS:**
    - All generated files MUST be placed in: /root/.claude/agent-state-machine/20241218_143022/conversations/conv_001/outputs/
    - Record your thinking process in: /root/.claude/agent-state-machine/20241218_143022/conversations/conv_001/dialogue.md
    - Do NOT use your default working directory or any other location, unless explicitly specified otherwise
    - Use only the specified absolute paths above for ALL file creation and documentation

    **TASK DETAILS:**
    Create Python file and execute it to verify functionality."
    ```

### Violation Handling Protocol
If user requests blocked action in MAIN state:
1. RECOGNIZE: "This requires [capability], which MAIN cannot perform"
2. TRANSITION: Match to appropriate agent OR suggest agent creation
3. DELEGATE: Use Task tool with workspace protocol above
4. LOG: Record state transition in state.jsonl

### State Transition Display
Show all transitions: [STATE_A → STATE_B]
Log all transitions to state.jsonl with trigger reason

### Workspace Enforcement Protocol
For ALL states (MAIN and AGENT):

#### Conversation-Based Workspace Rules:
1. DEFAULT WORKSPACE: [directory_path]/conversations/conv_[NNN]/outputs/
2. FILE CREATION: All generated files go to conversation outputs
3. TEMP FILES: Always use conversation outputs directory
4. EXCEPTIONS: Only when user provides explicit paths
5. DIALOGUE RECORDING: All thinking and actions recorded in dialogue.md

#### Example enforcement:
- MAIN: Creates documentation → [directory_path]/conversations/conv_[NNN]/outputs/documentation.md
- Agent: "Create a test script" → Creates: [directory_path]/conversations/conv_[NNN]/outputs/test_script.py
- Both states share the same outputs directory for the conversation
- NOT: ./test_script.py or /tmp/test_script.py (unless user specifies)

```

---

**Key Point:** Agent descriptions automatically define state transitions - no manual configuration needed.