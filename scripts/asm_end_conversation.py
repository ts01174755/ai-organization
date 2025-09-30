#!/usr/bin/env python3
"""
ASM End Conversation Module - Handles conversation completion and logging
"""

import json
import sys
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
    """End conversation and update messages.jsonl"""
    summary = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""

    session_path = get_session_path()
    if not session_path:
        output_json({"status": "error", "message": "No active session"})
        return

    # Find active conversation by scanning conversations directory
    conv_dir = Path(session_path) / 'conversations'
    if not conv_dir.exists():
        output_json({"status": "error", "message": "No conversations directory found"})
        return

    # Get all conversation directories
    existing_convs = sorted(conv_dir.glob('conv_*'))
    if not existing_convs:
        output_json({"status": "error", "message": "No conversations found"})
        return

    # Get the latest conversation (last one in sorted list)
    latest_conv = existing_convs[-1]
    conv_id = latest_conv.name
    workspace = str(latest_conv / 'outputs')

    # Collect agents used from state transitions
    state_file = Path(session_path) / 'state.jsonl'
    agents_used = set()

    if state_file.exists():
        lines = state_file.read_text().strip().split('\n')
        # Collect recent agent transitions (simple approach: collect all agents from transitions)
        for line in lines:
            entry = json.loads(line)
            if entry.get("type") == "transition":
                state = entry.get("data", {}).get("state")
                if state and state not in ["MAIN", "BASH"]:
                    agents_used.add(state)

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

    with open(messages_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(message_entry, ensure_ascii=False) + '\n')

    # Update dialogue.md with end marker
    dialogue_path = Path(session_path) / 'conversations' / conv_id / 'dialogue.md'
    if dialogue_path.exists():
        with open(dialogue_path, 'a') as f:
            f.write(f"\n## Conversation Ended: {datetime.now().isoformat()}\n")
            f.write(f"Summary: {summary}\n\n")

    # Output conversation end metadata
    output_json({
        "status": "conversation_ended",
        "conversation_id": conv_id,
        "summary": summary,
        "files_created": len(files_created),
        "agents_used": list(agents_used),
        "message": f"Conversation {conv_id} ended successfully"
    })

if __name__ == "__main__":
    main()