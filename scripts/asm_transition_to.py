#!/usr/bin/env python3
"""
ASM State Transition Module - Handles state transitions
"""

import json
import sys
from pathlib import Path
from datetime import datetime

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
    "can_execute": ["*"]
}

def output_json(data, prefix_info=""):
    """Simple JSON output"""
    if prefix_info:
        print(prefix_info)
    print(json.dumps(data, indent=2, ensure_ascii=False))

def get_session_path():
    """Get current session path from .asm directory in current working directory"""
    cwd = Path.cwd()
    session_file = cwd / '.asm' / '.current_asm_session'
    if session_file.exists():
        return session_file.read_text().strip()
    return None

def main():
    """Record state transition"""
    if len(sys.argv) < 2:
        output_json({"status": "error", "message": "Usage: asm_transition_to.py <new_state> [trigger]"})
        return

    new_state = sys.argv[1]
    trigger = sys.argv[2] if len(sys.argv) > 2 else ""

    session_path = get_session_path()
    if not session_path:
        output_json({"status": "error", "message": "No active session"})
        return

    # Get current state
    state_file = Path(session_path) / 'state.jsonl'
    if not state_file.exists():
        output_json({"status": "error", "message": "State file not found"})
        return

    lines = state_file.read_text().strip().split('\n')
    last_state = json.loads(lines[-1])

    # Find active conversation workspace by scanning conversations directory
    conv_dir = Path(session_path) / 'conversations'
    workspace = None
    dialogue_path = None

    # Get the latest conversation directory
    if conv_dir.exists():
        existing_convs = sorted(conv_dir.glob('conv_*'))
        if existing_convs:
            # Use the latest conversation (last one in sorted list)
            latest_conv = existing_convs[-1]
            workspace = str(latest_conv / 'outputs')
            dialogue_path = str(latest_conv / 'dialogue.md')

    # Fallback to session_path if no conversation found
    if not workspace:
        workspace = session_path

    # Determine permissions and session based on state
    if new_state == "MAIN":
        session = 'dialogue'
        permissions = MAIN_PERMISSIONS
    elif new_state == "BASH":
        session = 'system'
        permissions = BASH_PERMISSIONS
    else:
        # Any other state is considered an agent (e.g., consolidated-fullstack-data-engineer)
        session = 'execution'
        permissions = AGENT_PERMISSIONS

    # Record transition
    state_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "transition",
        "session_path": session_path,
        "session": session,
        "data": {
            "previous_state": last_state.get('data', {}).get("state", "MAIN"),
            "state": new_state,
            "trigger": trigger,
            "workspace": workspace,
            "dialogue_path": dialogue_path,
            "permissions": permissions
        }
    }

    with open(state_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(state_entry, ensure_ascii=False) + '\n')

    # Output transition metadata
    output_json(state_entry, prefix_info="State transition recorded:")

if __name__ == "__main__":
    main()