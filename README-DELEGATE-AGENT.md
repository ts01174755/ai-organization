# /delegate-agent 命令使用指南

## 📋 簡介

`/delegate-agent` 命令會自動將您的任務分派給最合適的專門代理來處理，而不是直接執行。這樣能獲得更專業的結果並節省處理時間。

## 🎯 核心理念

"**當有專家能做得更好時，為什麼要自己動手？**"

系統會自動為您的任務找到最合適的專門代理，就像是有一個專業團隊隨時待命。

## 🚦 快速入門指南

**提交您的任務**：
```bash
/delegate-agent 構建帶認證的 REST API
```

## 📝 命令語法

```bash
/delegate-agent <任務描述>
```

### 參數
- `任務描述`：需要完成的自然語言描述

### 示例
```bash
# 簡單任務
/delegate-agent 為認證模塊編寫單元測試

# 複雜任務
/delegate-agent 零停機時間將數據庫從 MySQL 遷移到 PostgreSQL

# 多個目標
/delegate-agent 修復安全漏洞並添加 GDPR 合規

# 模糊請求（將觸發澄清）
/delegate-agent 改進它
```

## 🎭 可用的專門代理

系統目前包含 23+ 個專門代理，涵蓋：

### 開發與工程
- `consolidated-fullstack-data-engineer` - 全棧和數據工程
- `juvenile-api-gateway-architect` - API 設計和網關管理
- `juvenile-database-architect` - 數據庫架構和優化
- `juvenile-prototype-integrator` - 快速原型開發

### 安全與合規
- `juvenile-security-compliance-guardian` - 安全審計和 GDPR 合規
- `juvenile-log-analyzer` - 日誌分析和異常檢測

### 基礎設施與運維
- `optimized-devops-infrastructure-engineer` - DevOps 和雲基礎設施
- `consolidated-chaos-engineering-platform` - 韌性測試

### AI 與分析
- `juvenile-llm-prompt-engineer` - 提示詞優化
- `consolidated-analysis-research-specialist` - 研究和分析
- `juvenile-ml-ops-engineer` - ML 模型部署

### 代理管理
- `agent-incubator` - 創建新的專門代理
- `juvenile-agent-ecosystem-optimizer` - 優化代理生態系統
- `consolidated-agent-quality-pipeline` - 代理質量評估

## 📈 性能優勢

### 令牌效率
- 專門代理使用優化、聚焦的提示詞
- 並行執行減少對話長度
- 避免主程序上下文污染

### 質量改進
- 來自專門代理的**領域專業知識**
- 跨相似任務的**一致方法**
- 通過代理專業化實現**更好的錯誤處理**

## 🔄 版本歷史

### v1.0（當前版本）
- 使用 `juvenile-agent-task-matcher` 的初始實現
- 基本的匹配/無匹配邏輯
- 後備到直接執行

### v2.0（未來的方向）
- 針對模糊請求的上下文感知匹配
- 多代理協作檢測
- 信心評分系統
- 從使用中學習模式
- 不用 '/delegate-agent [task]' 使用命令，改成 'delegate-agent --start' or 'delegate-agent --end' 等命令模式來開啟，關閉 'delegate-agent' 模式。

## 📚 相關文檔

- `/root/.claude/commands/delegate-agent.md` - 命令實現細節
- `/root/.claude/agents/juvenile-agent-task-matcher.md` - 匹配器代理規範
- `/root/.claude/scripts/generate-agent-list.py` - 代理目錄生成腳本（自動掃描並生成代理清單）
- `/root/.claude/data/AGENT_DIRECTORY.md` - 完整代理註冊表

---

**記住**：`/delegate-agent` 命令將每個請求轉變為專業卓越的機會。信任委派，利用專業知識，見證生產力飆升！🚀