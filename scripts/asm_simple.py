#!/usr/bin/env python3
"""
Simplified ASM Helper - Minimal implementation that focuses on essentials
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

# Global parent path for all ASM files
PARENT_PATH = Path('./.asm')
PARENT_PATH.mkdir(exist_ok=True)

# Define permissions for different states
MAIN_PERMISSIONS = {
    "can_write": ["*.md", "*.txt", "*.log", "*.json", "*.csv", "non-executable files"],
    "cannot_write": ["*.py", "*.js", "*.ts", "*.sh", "*.go", "*.rs", "*.c", "*.cpp", "*.java", "package.json", "requirements.txt", "Dockerfile", "Makefile", "any executable file"],
    "can_execute": ["read", "list", "search", "analyze", "information-gathering functions only"],
    "cannot_execute": ["run", "exec", "eval", "compile", "build"]
}

AGENT_PERMISSIONS = {
    "can_write": ["*"],
    "can_execute": ["*"]
}

BASH_PERMISSIONS = {
    "can_write": ["*"],
    "can_execute": ["*"],
    "note": "System initialization phase"
}

def output_json(data):
    """Simple JSON output"""
    print(json.dumps(data, indent=2))

def get_session_path():
    """Get or create session path"""
    session_file = PARENT_PATH / '.current_asm_session'

    if session_file.exists():
        return session_file.read_text().strip()

    return None

def init_session(mode='orchestrator', name=None):
    """Initialize ASM session - simplified"""
    # Session is always 'start' during initialization
    session = 'start'

    if name:
        # Use specified name under PARENT_PATH
        session_path = str(PARENT_PATH / name)
    else:
        # Use default with timestamp under PARENT_PATH
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        session_path = str(PARENT_PATH / f"session_{timestamp}")

    # Create directories and save session path
    os.makedirs(f"{session_path}/conversations", exist_ok=True)

    # Save session pointer in PARENT_PATH
    session_pointer_file = PARENT_PATH / '.current_asm_session'
    session_pointer_file.write_text(session_path)

    # Create messages.jsonl file for conversation index
    messages_file = Path(session_path) / 'conversations' / 'messages.jsonl'
    messages_file.touch()

    # Initialize state.jsonl with BASH state (system initialization)
    bash_init_entry = {
        "timestamp": datetime.now().isoformat(),
        "session": session,  # Always 'start' during initialization
        "state": "BASH",
        "mode": mode,
        "path": session_path,
        "permissions": BASH_PERMISSIONS
    }

    with open(f"{session_path}/state.jsonl", 'w') as f:
        f.write(json.dumps(bash_init_entry) + '\n')

    # Run agent list generator if exists
    generator = Path('/root/.claude/scripts/generate-agent-list.py')
    if generator.exists():
        os.system(f"python3 {generator} {session_path}")

    # Count agents from agent-list.txt
    agent_list_file = Path(session_path) / 'agent-list.txt'
    agent_count = 0
    if agent_list_file.exists():
        agent_count = len(agent_list_file.read_text().strip().split('\n'))

    print("\n🚀 Agent State Machine Initialized\n")
    print("Session Parameters:")
    print(f' Mode: "{mode}"')
    session_name = name if name else f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f' Name: "{session_name}"')
    print(f' Location: "{session_path}"')
    print(f'Available Agents: {agent_count} agents loaded')
    print(f' ✓ State persistence: "{session_path}/state.jsonl"')
    print(f' ✓ Agent descriptions: "{session_path}/AGENT_DIRECTORY.md"')
    print(f' ✓ Conversations directory: "{session_path}/conversations/"\n')
    print('MAIN State Permissions:')
    print(f' Can Write: [{", ".join(MAIN_PERMISSIONS["can_write"])}]')
    print(f' Cannot Write: [{", ".join(MAIN_PERMISSIONS["cannot_write"])}]')
    print(f' Can Execute: [{", ".join(MAIN_PERMISSIONS["can_execute"])}]')
    print(f' Cannot Execute: [{", ".join(MAIN_PERMISSIONS["cannot_execute"])}]\n')
    print('Agent State Permissions:')
    print(f' Can Write: [{", ".join(AGENT_PERMISSIONS["can_write"])}]')
    print(f' Can Execute: [{", ".join(AGENT_PERMISSIONS["can_execute"])}]\n')
    print('Waiting for first user input to create conversation...')

    output_json({
        "status": "success",
        "session_path": session_path,
        "session": session,
        "state": "BASH",
        "agent_count": agent_count
    })

    transition_to("MAIN", "initialization_complete")

def get_status():
    """Get current state - simplified"""
    session_path = get_session_path()
    if not session_path:
        output_json({"status": "error", "message": "No active session"})
        return

    state_file = Path(session_path) / 'state.jsonl'
    if not state_file.exists():
        output_json({"status": "error", "message": "State file not found"})
        return

    # Get last state
    lines = state_file.read_text().strip().split('\n')
    last_state = json.loads(lines[-1])

    # Get initial session state from first line
    first_state = json.loads(lines[0])
    session = first_state.get("session", "start")

    output_json({
        "status": "success",
        "state": last_state.get("state", "MAIN"),
        "session": session,
        "session_path": session_path,
        "workspace": last_state.get("workspace", session_path)
    })

def start_conversation():
    """Start new conversation - simplified"""
    session_path = get_session_path()
    if not session_path:
        output_json({"status": "error", "message": "No active session"})
        return

    # Count existing conversations
    conv_dir = Path(session_path) / 'conversations'
    existing = list(conv_dir.glob('conv_*'))
    next_num = len(existing) + 1
    conv_id = f"conv_{next_num:03d}"

    # Create conversation directory
    workspace = f"{session_path}/conversations/{conv_id}/outputs"
    os.makedirs(workspace, exist_ok=True)

    # Create dialogue.md file - IMPORTANT for recording
    dialogue_path = f"{session_path}/conversations/{conv_id}/dialogue.md"
    with open(dialogue_path, 'w') as f:
        f.write(f"# Conversation: {conv_id}\n\n")
        f.write(f"Started: {datetime.now().isoformat()}\n\n")

    # Update state
    state_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "conversation_start",
        "conversation_id": conv_id,
        "workspace": workspace
    }

    with open(f"{session_path}/state.jsonl", 'a') as f:
        f.write(json.dumps(state_entry) + '\n')

    output_json({
        "status": "success",
        "conversation_id": conv_id,
        "workspace": workspace,
        "dialogue_path": dialogue_path
    })

def transition_to(new_state, trigger=""):
    """Record state transition - simplified"""
    
    session_path = get_session_path()
    if not session_path:
        output_json({"status": "error", "message": "No active session"})
        return

    # Get current state
    state_file = Path(session_path) / 'state.jsonl'
    lines = state_file.read_text().strip().split('\n')
    last_state = json.loads(lines[-1])

    # Determine permissions based on state
    if new_state == "MAIN":
        session = 'dialogue'
        permissions = MAIN_PERMISSIONS
    else:
        session = 'execution'
        # Agent state has full permissions
        permissions = AGENT_PERMISSIONS

    # Record transition
    state_entry = {
        "timestamp": datetime.now().isoformat(),
        "session": session,  # Always 'start' during initialization
        "state": new_state,
        "previous": last_state.get("state", "MAIN"),
        "trigger": trigger,
        "workspace": last_state.get("workspace", session_path),
        "permissions": permissions
    }

    with open(state_file, 'a') as f:
        f.write(json.dumps(state_entry) + '\n')

    output_json({
        "status": "success",
        "previous": last_state.get("state", "MAIN"),
        "new_state": new_state,
        "workspace": last_state.get("workspace", session_path)
    })

    if new_state == "MAIN":
        start_conversation()

def delegate_task(agent_name, task):
    """Prepare delegation - simplified"""
    session_path = get_session_path()
    if not session_path:
        output_json({"status": "error", "message": "No active session"})
        return

    # Get workspace
    state_file = Path(session_path) / 'state.jsonl'
    lines = state_file.read_text().strip().split('\n')
    last_state = json.loads(lines[-1])
    workspace = last_state.get("workspace", session_path)

    # Build delegation prompt
    prompt = f"""**WORKSPACE REQUIREMENTS:**
- All generated files MUST be placed in: {workspace}
- Do NOT use your default working directory or any other location

**TASK DETAILS:**
{task}"""

    output_json({
        "status": "success",
        "task_tool_params": {
            "subagent_type": agent_name,
            "description": task[:50],  # Brief description
            "prompt": prompt
        },
        "workspace": workspace
    })

def end_conversation(summary=""):
    """End conversation and update messages.jsonl"""
    session_path = get_session_path()
    if not session_path:
        output_json({"status": "error", "message": "No active session"})
        return

    # Get current conversation from state
    state_file = Path(session_path) / 'state.jsonl'
    lines = state_file.read_text().strip().split('\n')

    # First pass: identify the last active conversation
    conv_id = None
    workspace = None
    ended_conversations = set()

    # Process chronologically to find ended conversations
    for line in lines:
        entry = json.loads(line)
        if entry.get("type") == "conversation_end":
            ended_conversations.add(entry.get("conversation_id"))

    # Find the last conversation that hasn't ended
    for line in reversed(lines):
        entry = json.loads(line)
        if entry.get("type") == "conversation_start":
            cid = entry.get("conversation_id")
            if cid not in ended_conversations:
                conv_id = cid
                workspace = entry.get("workspace")
                break

    # Second pass: collect all agents used in this conversation
    agents_used = set()
    if conv_id:
        in_conversation = False
        for line in lines:
            entry = json.loads(line)

            # Start collecting when we find our conversation
            if entry.get("type") == "conversation_start" and entry.get("conversation_id") == conv_id:
                in_conversation = True

            # Collect agent transitions within our conversation
            if in_conversation and entry.get("type") == "transition":
                state = entry.get("state")
                if state and state != "MAIN":
                    agents_used.add(state)

            # Stop if we hit the end of our conversation (shouldn't happen for active conv)
            if entry.get("type") == "conversation_end" and entry.get("conversation_id") == conv_id:
                break

    # Check if we found an active conversation
    if not conv_id:
        output_json({"status": "error", "message": "No active conversation found"})
        return

    # List files created in outputs
    outputs_dir = Path(workspace)
    files_created = []
    if outputs_dir.exists():
        for file in outputs_dir.iterdir():
            if file.is_file():
                files_created.append({
                    "path": str(file),
                    "summary": f"{file.suffix[1:] if file.suffix else 'unknown'} file"
                })

    # Update messages.jsonl
    messages_file = Path(session_path) / 'conversations' / 'messages.jsonl'
    message_entry = {
        "conversation_id": conv_id,
        "timestamp": datetime.now().isoformat(),
        "summary": summary or "Conversation completed",
        "files_created": files_created,
        "agents_used": list(agents_used)
    }

    with open(messages_file, 'a') as f:
        f.write(json.dumps(message_entry) + '\n')

    # Update dialogue.md with end marker
    dialogue_path = Path(session_path) / 'conversations' / conv_id / 'dialogue.md'
    if dialogue_path.exists():
        with open(dialogue_path, 'a') as f:
            f.write(f"\n## Conversation Ended: {datetime.now().isoformat()}\n")
            f.write(f"Summary: {summary}\n\n")

    # Update state with conversation_end
    state_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "conversation_end",
        "conversation_id": conv_id
    }

    with open(state_file, 'a') as f:
        f.write(json.dumps(state_entry) + '\n')

    output_json({
        "status": "success",
        "conversation_id": conv_id,
        "summary_recorded": summary,
        "files_created": len(files_created),
        "agents_used": list(agents_used)
    })

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        output_json({"status": "error", "message": "Usage: asm_simple.py <command> [args]"})
        return

    command = sys.argv[1]

    if command == "init":
        # Parse arguments for mode and name
        mode = "orchestrator"
        name = None

        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == "--mode" and i + 1 < len(sys.argv):
                mode = sys.argv[i + 1]
                i += 2
            elif sys.argv[i] == "--name" and i + 1 < len(sys.argv):
                name = sys.argv[i + 1]
                i += 2
            else:
                # Support old format (just mode)
                mode = sys.argv[i]
                i += 1

        init_session(mode, name)
    elif command == "status":
        get_status()
    elif command == "conv-start":
        start_conversation()
    elif command == "conv-end":
        summary = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        end_conversation(summary)
    elif command == "transition":
        if len(sys.argv) < 3:
            output_json({"status": "error", "message": "Usage: transition <new_state> [trigger]"})
        else:
            new_state = sys.argv[2]
            trigger = sys.argv[3] if len(sys.argv) > 3 else ""
            transition_to(new_state, trigger)
    elif command == "delegate":
        if len(sys.argv) < 4:
            output_json({"status": "error", "message": "Usage: delegate <agent> <task>"})
        else:
            agent = sys.argv[2]
            task = " ".join(sys.argv[3:])
            delegate_task(agent, task)
    else:
        output_json({"status": "error", "message": f"Unknown command: {command}"})

if __name__ == "__main__":
    main()