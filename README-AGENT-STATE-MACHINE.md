# Agent State Machine

## 快速開始

```bash
# 啟動狀態機（預設模式）
/agent-state-machine

# 結束狀態機
/agent-state-machine --session end
```

就這麼簡單！系統會自動處理所有狀態轉換。

## 這是什麼？

Agent State Machine 是一個讓 Claude Code 更有組織的執行模式：
- **MAIN 狀態**：只能讀取、分析和寫文檔
- **Agent 狀態**：執行專項任務

當你執行專項任務時，系統會自動切換到適合的 Agent。

## 使用範例

```bash
# 啟動
User: /agent-state-machine

# 正常對話
User: "寫個 Python 爬蟲"
[MAIN → juvenile-prototype-integrator]  # 自動切換
# Agent 寫程式碼...
[juvenile-prototype-integrator → MAIN]  # 完成返回

User: "執行測試"
[MAIN → consolidated-fullstack-data-engineer]
# Agent 執行測試...
[consolidated-fullstack-data-engineer → MAIN]

# 結束
User: /agent-state-machine --session end
```

## 進階選項（選用）

```bash
# 指定工作目錄
/agent-state-machine --path /my/workspace

# 完整參數
/agent-state-machine --session start --mode orchestrator --path /my/workspace
```

### 參數說明

| 參數 | 預設值 | 說明 |
|------|--------|------|
| `--session` | `start` | `start` 啟動 / `end` 結束 |
| `--mode` | `orchestrator` | 執行模式（目前只支援 orchestrator） |
| `--path` | 自動生成時間戳目錄 | 工作空間路徑 |

## 為什麼要用？

1. **更安全**：MAIN 不能直接執行程式碼
2. **更清楚**：每個狀態轉換都有記錄
3. **更專業**：專門的 Agent 處理專門的任務

## 注意事項

- 狀態機啟動後，所有操作都會遵循狀態規則
- MAIN 狀態不能寫程式檔案（*.py, *.js 等）
- 需要寫程式時會自動切換到適合的 Agent
- 使用 `--session end` 結束狀態機模式

就這樣，開始使用吧！