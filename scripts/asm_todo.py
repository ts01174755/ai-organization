#!/usr/bin/env python3
"""
SAM (State Agent Machine) Todo List Generator - Generates todo lists with examples for LLM guidance
"""

import sys
from pathlib import Path

SCRIPTS_PATH = Path('/Users/leon_wu/.claude/scripts')

def generate_init_todos():
    """Generate todos for initializing state machine"""
    todos = [
        {
            "task": "初始化狀態機",
            "command": f"python3 {SCRIPTS_PATH}/asm_init.py [project_name]",
            "example": f"python3 {SCRIPTS_PATH}/asm_init.py my_project",
            "description": "完成狀態機初始化，建立 .asm 目錄結構",
            "returns": "JSON: timestamp, type, session_path, session, data(state, agent_list_file, agent_description_file, permissions)"
        },
    ]
    return todos

def generate_conversation_todos():
    """Generate todos for starting a conversation"""
    todos = [
        {
            "task": "對話資料夾初始化",
            "command": f"python3 {SCRIPTS_PATH}/asm_start_conversation.py",
            "example": f"python3 {SCRIPTS_PATH}/asm_start_conversation.py",
            "description": "建立新的對話資料夾 (conv_XXX)",
            "returns": "JSON: status, conversation_id, workspace, dialogue_path, message"
        },
        {
            "task": "狀態轉換到 MAIN",
            "command": f"python3 {SCRIPTS_PATH}/asm_transition_to.py MAIN start_conversation",
            "example": f"python3 {SCRIPTS_PATH}/asm_transition_to.py MAIN start_conversation",
            "description": "從 BASH 狀態轉換到 MAIN 狀態",
            "returns": "JSON: timestamp, type, session_path, session, data(previous_state, state, trigger, workspace, dialogue_path, permissions)"
        },
        {
            "task": "依據權限執行使用者請求",
            "description": "根據 MAIN 狀態權限處理請求，必要時委派給 Agent"
        },
        {
            "task": "記錄對話過程到 dialogue.md",
            "description": "在執行操作的過程中，將重要的思考、決策、操作步驟、整盒agent執行的結果，記錄到 dialogue_path",
            "note": "使用 Edit 或 Write tool 持續更新 dialogue.md，記錄詳細對話內容（不限字數）"
        },
        {
            "task": "結束對話並記錄簡短摘要",
            "command": f"python3 {SCRIPTS_PATH}/asm_end_conversation.py [summary]",
            "example": f"python3 {SCRIPTS_PATH}/asm_end_conversation.py 'Created hello world script and tested it'",
            "description": "記錄 50 字以內的簡短摘要到 messages.jsonl",
            "returns": "JSON: status, conversation_id, summary, files_created, agents_used, message",
            "note": "summary 參數應該是簡短摘要（50字內），詳細內容應已記錄在 dialogue.md"
        }
    ]
    return todos

def generate_transition_to_agent_todos():
    """Generate todos for transitioning to agent"""
    todos = [
        {
            "task": "狀態轉換到 Agent",
            "command": f"python3 {SCRIPTS_PATH}/asm_transition_to.py [agent-name] [trigger]",
            "example": f"python3 {SCRIPTS_PATH}/asm_transition_to.py consolidated-fullstack-data-engineer 'user requested Python script'",
            "description": "記錄狀態轉換到指定 Agent（直接使用 agent 名稱）",
            "returns": "JSON: timestamp, type, session_path, session, data(previous_state, state, trigger, workspace, dialogue_path, permissions)",
            "note": "返回的 workspace 和 dialogue_path 用於委派任務給 Agent"
        },
        {
            "task": "使用 Task tool 委派給 Agent",
            "description": "使用 Task tool 調用 Agent，指定 workspace 和 dialogue_path，要求 Agent 在該目錄下創建文件並執行任務，並把中間的過程記錄在 dialogue.md 中",
            "note": "將上一步返回的 workspace 和 dialogue_path 加入 prompt 中，Agent 會在指定目錄創建文件"
        },
        {
            "task": "等待 Agent 執行結果",
            "description": "Agent 執行完成後會返回結果"
        },
        {
            "task": "狀態轉換回 MAIN",
            "command": f"python3 {SCRIPTS_PATH}/asm_transition_to.py MAIN task_completed",
            "example": f"python3 {SCRIPTS_PATH}/asm_transition_to.py MAIN task_completed",
            "description": "Agent 完成任務後返回 MAIN 狀態",
            "returns": "JSON: timestamp, type, session_path, session, data(previous_state, state, trigger, workspace, dialogue_path, permissions)"
        }
    ]
    return todos

def generate_end_session_todos():
    """Generate todos for ending session"""
    todos = [
        {
            "task": "狀態轉換到 BASH",
            "command": f"python3 {SCRIPTS_PATH}/asm_transition_to.py BASH session_end",
            "example": f"python3 {SCRIPTS_PATH}/asm_transition_to.py BASH session_end",
            "description": "結束狀態機會話，返回系統狀態",
            "returns": "JSON: timestamp, type, session_path, session, data(previous_state, state, trigger, workspace, dialogue_path, permissions)"
        },
        {
            "task": "恢復正常操作模式",
            "description": "LLM 恢復標準操作，不再受狀態機權限限制"
        }
    ]
    return todos

def print_todos(todos, title):
    """Print todos in formatted way"""
    print(f"\n{title}:")
    print("=" * 60)

    for i, todo in enumerate(todos, 1):
        print(f"\n[{i}] {todo['task']}")
        if 'command' in todo:
            print(f"    命令: {todo['command']}")
            print(f"    範例: {todo['example']}")
        print(f"    說明: {todo['description']}")
        if 'returns' in todo:
            print(f"    回傳: {todo['returns']}")
        if 'note' in todo:
            print(f"    注意: {todo['note']}")

    print("\n" + "=" * 60)

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: sam_todo.py <scenario>")
        print("Scenarios: init, start_conversation, end_conversation, transition_to_agent, end_session")
        return

    scenario = sys.argv[1]

    if scenario == "init":
        todos = generate_init_todos()
        print_todos(todos, "初始化狀態機 Todo List")

    elif scenario == "start_conversation":
        todos = generate_conversation_todos()
        print_todos(todos, "對話 Todo List")

    elif scenario == "transition_to_agent":
        todos = generate_transition_to_agent_todos()
        print_todos(todos, "委派給 Agent Todo List")

    elif scenario == "end_session":
        todos = generate_end_session_todos()
        print_todos(todos, "結束狀態機 Todo List")

    else:
        print(f"Unknown scenario: {scenario}")
        print("Valid scenarios: init, start_conversation, end_conversation, transition_to_agent, end_session")

if __name__ == "__main__":
    main()