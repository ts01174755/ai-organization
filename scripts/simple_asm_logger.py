#!/usr/bin/env python3
"""
Simple Agent State Machine Conversation Logger

A lightweight Python script for logging Agent State Machine conversations
to messages.jsonl format. Supports JSON input to handle spaces and special characters.
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any


class SimpleASMLogger:
    """Simple conversation logger for Agent State Machine."""

    def __init__(self, session_path: str):
        """Initialize logger with session path."""
        self.session_path = Path(session_path)
        self.conversations_dir = self.session_path / "conversations"
        self.messages_file = self.conversations_dir / "messages.jsonl"

        # Ensure conversations directory exists
        self.conversations_dir.mkdir(parents=True, exist_ok=True)

        # Ensure messages.jsonl exists
        if not self.messages_file.exists():
            self.messages_file.touch()

    def log_conversation(self,
                        conversation_id: str,
                        timestamp: str,
                        summary: str,
                        files_created: List[Dict[str, str]],
                        agents_used: List[str]) -> bool:
        """
        Log a conversation to messages.jsonl

        Args:
            conversation_id: Unique conversation identifier
            timestamp: ISO format timestamp
            summary: Brief conversation description
            files_created: List of {"path": str, "summary": str} objects
            agents_used: List of agent names used

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create conversation record
            record = {
                "conversation_id": conversation_id,
                "timestamp": timestamp,
                "summary": summary,
                "files_created": files_created,
                "agents_used": agents_used
            }

            # Append to messages.jsonl
            with open(self.messages_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')

            print(f"✅ Successfully logged conversation: {conversation_id}")
            print(f"📁 Location: {self.messages_file}")
            return True

        except Exception as e:
            print(f"❌ Error logging conversation: {e}", file=sys.stderr)
            return False

    def log_from_json(self, json_input: str) -> bool:
        """
        Log conversation from JSON input string.

        Expected JSON format:
        {
            "session_path": "/path/to/session",
            "conversation_data": {
                "conversation_id": "conv_001",
                "timestamp": "2025-09-18T08:10:09",
                "summary": "Description",
                "files_created": [{"path": "/file.py", "summary": "File description"}],
                "agents_used": ["agent1", "agent2"]
            }
        }
        """
        try:
            data = json.loads(json_input)

            # Extract session path and conversation data
            session_path = data.get("session_path")
            conv_data = data.get("conversation_data", {})

            if not session_path:
                raise ValueError("Missing 'session_path' in JSON input")

            # Initialize logger with session path
            logger = SimpleASMLogger(session_path)

            # Log the conversation
            return logger.log_conversation(
                conversation_id=conv_data.get("conversation_id", ""),
                timestamp=conv_data.get("timestamp", ""),
                summary=conv_data.get("summary", ""),
                files_created=conv_data.get("files_created", []),
                agents_used=conv_data.get("agents_used", [])
            )

        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON input: {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"❌ Error processing JSON: {e}", file=sys.stderr)
            return False


def main():
    """Command line interface for the logger."""
    # Read JSON from stdin
    try:
        json_input = sys.stdin.read()

        # If no input or empty input, show help
        if not json_input.strip():
            print("Simple ASM Logger - Conversation logging for Agent State Machine")
            print("")
            print("Usage:")
            print(f"    echo '<json>' | python3 {sys.argv[0]}")
            print("")
            print("JSON format:")
            print('''{
    "session_path": "/path/to/session",
    "conversation_data": {
        "conversation_id": "conv_001",
        "timestamp": "2025-09-18T08:10:09",
        "summary": "Task description",
        "files_created": [
            {"path": "/path/to/file.py", "summary": "File description"}
        ],
        "agents_used": ["agent1", "agent2"]
    }
}''')
            sys.exit(1)

        logger = SimpleASMLogger("/tmp")  # Temporary, will be overridden by JSON
        success = logger.log_from_json(json_input)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()