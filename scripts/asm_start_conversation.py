#!/usr/bin/env python3
"""
ASM Start Conversation Module - Handles conversation initialization
"""

import json
import os
from pathlib import Path
from datetime import datetime

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
    """Start new conversation"""
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

    # Output conversation metadata
    output_json({
        "status": "conversation_started",
        "conversation_id": conv_id,
        "workspace": workspace,
        "dialogue_path": dialogue_path,
        "message": f"Conversation {conv_id} initialized"
    }, prefix_info="Conversation initialized:")

if __name__ == "__main__":
    main()