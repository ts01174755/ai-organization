#!/usr/bin/env python3
"""
ASM Initialization Module - Handles state machine initialization
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Define permissions for different states
BASH_PERMISSIONS = {
    "can_write": ["*"],
    "can_execute": ["*"],
    "note": "System initialization phase"
}

def output_json(data, prefix_info=""):
    """Simple JSON output"""
    if prefix_info:
        print(prefix_info)
    print(json.dumps(data, indent=2, ensure_ascii=False))

def main():
    """Initialize ASM session"""
    # Parse arguments - requires both project_name and mode
    if len(sys.argv) < 2:
        output_json({"status": "error", "message": "Usage: asm_init.py <project_name> <mode>"})
        return

    name = sys.argv[1]

    # Session path is in current working directory under .asm/
    cwd = Path.cwd()
    parent_path = cwd / '.asm'
    parent_path.mkdir(parents=True, exist_ok=True)

    if name:
        # Use specified name under parent_path
        session_path = str(parent_path / name)
    else:
        # Use default with timestamp under parent_path
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        session_path = str(parent_path / f"session_{timestamp}")

    # Create directories and save session path
    os.makedirs(f"{session_path}/conversations", exist_ok=True)

    # Save session pointer in parent_path
    session_pointer_file = parent_path / '.current_asm_session'
    session_pointer_file.write_text(session_path)

    # Create messages.jsonl file for conversation index
    messages_file = Path(session_path) / 'conversations' / 'messages.jsonl'
    messages_file.touch()

    # Run agent list generator from user's home directory
    home_dir = Path.home()
    generator = home_dir / '.claude' / 'scripts' / 'generate-agent-list.py'
    if generator.exists():
        os.system(f"python3 {generator} {session_path}")

    # Count agents from agent-list.txt
    agent_description_file = Path(session_path) / 'AGENT_DIRECTORY.md'  # This is
    agent_list_file = Path(session_path) / 'agent-list.txt'

    # Initialize state.jsonl with BASH state (system initialization)
    bash_init_entry = {
        "timestamp": datetime.now().isoformat(),
        "type": "initialization",
        "session_path": session_path,
        "session": 'system',  # Always 'system' during initialization
        "data": {
            "previous_state": '',
            "state": "BASH",
            'trigger': 'init',
            'agent_list_file': str(agent_list_file) if agent_list_file.exists() else "",
            'agent_description_file': str(agent_description_file) if agent_description_file.exists() else "",
            "permissions": BASH_PERMISSIONS
        }
    }

    with open(f"{session_path}/state.jsonl", 'w', encoding='utf-8') as f:
        f.write(json.dumps(bash_init_entry, ensure_ascii=False) + '\n')

    # Output initialization metadata
    output_json(bash_init_entry, prefix_info="✅ ASM Initialized Successfully")

if __name__ == "__main__":
    main()