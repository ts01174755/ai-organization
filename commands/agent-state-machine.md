# Agent State Machine Command

## Command: `/agent-state-machine [--session start/end] [--project project_name]`

**Purpose:** Implement a finite state machine where MAIN state has restricted permissions and delegates to agents when needed.

---

## Core Workflow

**Every workflow starts with a todo list:**

```bash
python3 ~/.claude/scripts/asm_todo.py [scenario]
```

**Available scenarios:**
- `init` - Initialize session
- `start_conversation` - Begin new conversation (use EVERY time user sends a message)
- `transition_to_agent` - Delegate to agent
- `end_session` - Terminate session

**Workflow pattern:**
1. Execute `asm_todo.py [scenario]` to get todo list
2. Follow each step in the returned todo list sequentially
3. Execute the commands shown in the todo list

**Important:** Always call `asm_todo.py` first, even if you remember the steps.

---

## Command Parameters

```yaml
--session start --project [name]:
  - Initialize state machine session
  - Creates .asm/[project_name]/ directory
  - Example: /agent-state-machine --session start --project my_project

--session end:
  - Terminate state machine session
  - Returns to normal operation
  - Example: /agent-state-machine --session end
```

---

## Permission Rules

### MAIN State (Restricted)
**Can:**
- Read any files
- Write non-executable files (*.md, *.txt, *.log, *.json, *.csv)
- Information gathering (search, analyze, WebSearch, WebFetch)
- Task management (TodoWrite)
- Delegate to agents (Task tool)

**Cannot:**
- Write executable files (*.py, *.js, *.ts, *.sh, etc.)
- Execute code (python, node, npm, bash commands)
- Edit executable files or configs

**When MAIN cannot do something → Delegate to agent**

### Agent State (Full Access)
**Can:**
- Write any files
- Execute any code
- Full development capabilities

---

## State Flow

```
Session start: BASH (init)
First conversation: BASH → MAIN
Subsequent conversations: MAIN → MAIN (each new user input)
Agent delegation: MAIN → AGENT → MAIN
Session end: MAIN → BASH
```

**Key concept:** Each user message = new conversation = new conv_[NNN] directory

---

## Scenario 1: Session Initialization

```bash
User: /agent-state-machine --session start --project test_project

LLM Actions:
1. python3 ~/.claude/scripts/asm_todo.py init
2. Follow returned todo list:
   - Execute: python3 asm_init.py test_project
   - Display: [State: BASH] - Session initialized
```

**Result:** Session created at `.asm/test_project/`, waiting for first conversation.

---

## Scenario 2: Start Conversation (EVERY user message)

```bash
User: "Hello, what can you help with?"

LLM Actions:
1. python3 ~/.claude/scripts/asm_todo.py start_conversation
2. Follow returned todo list (5 steps):
   [1] Execute: asm_start_conversation.py
       → Returns: workspace, dialogue_path

   [2] Execute: asm_transition_to.py MAIN start_conversation
       → State: BASH → MAIN (or MAIN → MAIN for subsequent conversations)
       → Display: [BASH → MAIN] [Conv: 001]

   [3] Process request in MAIN state
       → Check permissions
       → If blocked: delegate to agent (see Scenario 3)
       → If allowed: respond directly

   [4] Record dialogue to dialogue.md
       → Use Write/Edit tool to update dialogue.md
       → Record thinking, decisions, actions

   [5] Execute: asm_end_conversation.py "brief summary (50 chars max)"
       → Display: [State: MAIN] [Conv: 001 Ended]
```

**Example responses:**
- Information request: Answer directly in MAIN
- Code request: Delegate to agent (see Scenario 3)

---

## Scenario 3: Delegate to Agent

```bash
User: "Write hello_world.py and execute it"

Analysis in MAIN:
  → Task requires: Writing *.py file (BLOCKED)
  → Task requires: Executing code (BLOCKED)
  → Decision: Must delegate to agent

LLM Actions:
1. python3 ~/.claude/scripts/asm_todo.py transition_to_agent

2. Follow returned todo list (4 steps):
   [1] Execute: asm_transition_to.py [agent-name] [trigger]
       Example: asm_transition_to.py consolidated-fullstack-data-engineer 'user requested Python script'
       → Returns: workspace, dialogue_path, permissions
       → Display: [MAIN → CONSOLIDATED-FULLSTACK-DATA-ENGINEER]

   [2] Use Task tool with workspace requirements:
       prompt: |
         Create hello_world.py and execute it.

         **WORKSPACE REQUIREMENTS:**
         - All generated files MUST be placed in: {workspace}
         - Record your thinking process in: {dialogue_path}
         - Do NOT use your default working directory

   [3] Wait for agent completion

   [4] Execute: asm_transition_to.py MAIN task_completed
       → Display: [CONSOLIDATED-FULLSTACK-DATA-ENGINEER → MAIN]
```

**Agent selection:** Read `.asm/[project_name]/AGENT_DIRECTORY.md` to choose appropriate agent.

---

## Scenario 4: Session Termination

```bash
User: /agent-state-machine --session end

LLM Actions:
1. python3 ~/.claude/scripts/asm_todo.py end_session
2. Follow returned todo list:
   - Execute: asm_transition_to.py BASH session_end
   - Display: [MAIN → BASH] Session Ended
   - Display session summary
```

**Result:** System returns to normal operation mode.

---

## Dialogue Recording Template

Use Write/Edit tool to update `.asm/[project_name]/conversations/conv_[NNN]/dialogue.md`:

```markdown
# Conversation [NNN] - [Brief Title]

**Timestamp:** [YYYY-MM-DD]T[HH:MM:SS]

**User Request:**
[User's exact message]

## MAIN Analysis

**Permission Check:**
- Task requires: [list requirements]
- MAIN can/cannot: [analysis]

**Decision:**
- [Handle in MAIN / Delegate to agent]
- Reason: [brief explanation]

---

## [MAIN Response / Agent Delegation]

[If MAIN handles:]
[Your response to user]

[If agent delegation:]
**Agent Selected:** [agent-name]
**Trigger:** [reason for delegation]

### Agent Execution
[Describe what agent will do]

### Agent Results
[Agent's output/files created]

---

## Conversation Summary
[Brief summary of what was accomplished]
```

---

## Quick Reference

### State Transition Display Format
- `[BASH → MAIN] [Conv: 001]` - First conversation starts
- `[MAIN → MAIN] [Conv: 002]` - Subsequent conversation starts
- `[MAIN → AGENT-NAME]` - Delegate to agent
- `[AGENT-NAME → MAIN]` - Agent returns
- `[State: MAIN] [Conv: 001 Ended]` - Conversation ends
- `[MAIN → BASH] Session Ended` - Session terminates

### Decision Tree
```
User input received
  ↓
Call: asm_todo.py start_conversation
  ↓
Analyze request in MAIN
  ↓
Can MAIN handle it?
  ├─ Yes → Respond directly → End conversation
  └─ No → Call: asm_todo.py transition_to_agent
           ↓
           Delegate to agent → Agent executes → Return to MAIN → End conversation
```

### Common Patterns

**Information/explanation request:**
- MAIN can handle → respond directly

**Code creation/execution request:**
- MAIN cannot handle → delegate to agent

**File operations:**
- Non-executable files → MAIN can handle
- Executable files → delegate to agent

---

## Important Notes

1. **Always use asm_todo.py first** - Don't execute scripts directly
2. **Every user message = new conversation** - Always call `start_conversation`
3. **Workspace paths from todo lists** - Don't construct paths manually
4. **Record to dialogue.md** - Use Write/Edit tool during conversation
5. **Brief summaries for end_conversation** - 50 characters max

---

**Key Point:** Follow the todo lists returned by `asm_todo.py` - they contain the exact commands and workflows needed for each scenario.