# Agent 狀態機命令

## 概述

將 Claude Code 執行模型轉換為有限狀態機，主程序和 agents 是具有明確權限的獨立狀態。

## 核心概念：可執行邊界

MAIN 狀態**無法寫入可執行檔案**：
- ❌ 不能寫：`*.py`、`*.js`、`*.sh`、配置檔
- ✅ 可以寫：`*.md`、`*.txt`、文檔

這強制所有執行任務必須委派給 agents。

## 快速開始

```bash
# 啟動
/agent-state-machine --session start --mode orchestrator --path /root/.claude/fsm/session1

# 工作（系統自動處理狀態轉換）
User: "寫個 Python 函數"
[MAIN → FULLSTACK_ENGINEER]  # MAIN 無法寫 *.py
[FULLSTACK_ENGINEER → MAIN]  # 任務完成

# 結束
/agent-state-machine --session end
```

## 命令語法

```bash
/agent-state-machine --session [start/end] --mode [模式] --path [目錄路徑]
```

| 參數 | 選項 | 說明 |
|------|------|------|
| `--session` | `start`、`end` | 啟動或結束會話 |
| `--mode` | `orchestrator`、`interactive`、`response` | 轉換模式 |
| `--path` | 目錄路徑 | 工作空間位置 |

### 模式

- **Orchestrator**（已實現）：`MAIN → Agent → MAIN`
- **Interactive**（計劃中）：`MAIN → Agent_A → Agent_B → MAIN`
- **Response**（計劃中）：`Queue → Agent → Queue`

## 運作流程

1. **初始化**：載入 agents、創建目錄、初始化 `state.jsonl`
2. **模式匹配**：檢查輸入是否匹配 agent descriptions
3. **狀態轉換**：記錄到 `state.jsonl`，顯示 `[A → B]`
4. **執行**：MAIN 只能協調，agents 執行任務

## 實際範例

```bash
User: /agent-state-machine --session start --path /root/.claude/fsm --mode orchestrator
[State Machine Initialized]

User: "Hello World 的由來是什麼？寫個 hello_world.py 並執行"

# MAIN 可以回答問題
關於 "Hello, World!" 的文化起源...

# 但無法寫 *.py，必須委派
[MAIN → juvenile-prototype-integrator]
# Agent 創建並執行 hello_world.py
[juvenile-prototype-integrator → MAIN]

User: /agent-state-machine --session end
```

## 優點

1. **強制委派** - MAIN 物理上無法寫執行檔
2. **審計軌跡** - 所有轉換記錄在 `state.jsonl`
3. **Token 效率** - 執行上下文隔離在 agents
4. **確定性行為** - 模式匹配而非概率決策

## 目錄結構

```
[path]/
├── main/           # MAIN 工作空間
├── [agent-name]/   # Agent 工作空間
└── state.jsonl     # 狀態歷史
```

## 狀態歷史

```jsonl
{"type": "session_init", "state": "MAIN", "permissions":{...}, "parameters": {...}}
{"type": "transition", "state": "DATABASE_ARCHITECT", "permissions":{...},, "trigger": "database", "previous": "MAIN"}
{"type": "transition", "state": "MAIN", "permissions":{...},, "trigger": "completed", "previous": "DATABASE_ARCHITECT"}
```

## 權限系統

每個狀態有明確權限：
- `can_write` / `cannot_write` - 檔案寫入權限
- `can_execute` / `cannot_execute` - 執行權限

## 常見問題

**Q: 為什麼沒有委派？**
A: 檢查輸入是否匹配 agent descriptions

**Q: 如何查看當前狀態？**
A: 查看 `state.jsonl` 最新條目或回應中的 `[State: X]`

**Q: 可以讓 MAIN 寫程式碼嗎？**
A: 不行，這是設計核心原則

---

*詳細規範：`/root/.claude/commands/agent-state-machine.md`*