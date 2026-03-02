# AI Skill Extractor
## AI Employee Capability Evaluation System

---

## 專案介紹

這是一個 AI 驅動的員工能力評估系統，透過 AI Agent 與員工的日常互動，自然地收集行為信號並進行能力評估。

---

## 系統架構

```
┌─────────────────────────────────────────────────────────┐
│                    系統架構                               │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  📱 WhatsApp           🤖 Companion Agent              │
│  ┌─────────┐          ┌─────────────────┐              │
│  │  Employee │ ◄─────► │  AI 助手        │              │
│  └─────────┘          └────────┬────────┘              │
│                                │                        │
│                         對話內容                        │
│                                │                        │
│                         ┌──────▼──────┐                │
│                         │  Evidence   │                │
│                         │ Extraction  │                │
│                         └──────┬──────┘                │
│                                │                        │
│                         ┌──────▼──────┐                │
│                         │  Evaluator  │                │
│                         │    Agent    │                │
│                         └─────────────┘                │
│                                │                        │
│                         📊 評估報告                   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 四大評估維度

| 維度 | 說明 | 範例問題 |
|------|------|----------|
| 📌 CONTEXT_JUDGMENT | 情境判斷 | 你是如何決定優先順序的？ |
| ⚠️ EXCEPTION_HANDLING | 異常處理 | 面對意外問題，你第一步做什麼？ |
| 🔮 RISK_ANTICIPATION | 風險預判 | 你考慮了哪些可能的副作用？ |
| 🤝 COLLABORATION | 團隊協作 | 還需要跟誰溝通？ |

---

## 專案結構

```
aiskill_extractor/
├── prompts/                    # AI Prompts
│   ├── companion_prompt.py     # Companion Agent Prompt
│   ├── evidence_extraction_prompt.py
│   └── evaluator_prompt.py
├── src/                       # 程式碼
│   ├── evaluator.py           # 評估引擎
│   └── report_server.py      # 報告網頁伺服器
├── data/                      # 資料庫
│   └── evidence.db            # SQLite 資料庫
├── reports/                   # 報告模板
│   └── template.html          # HTML 報告模板
└── README.md
```

---

## 安裝與執行

### 1. 安裝依賴

```bash
# 安裝 Flask
pip install flask
```

### 2. 初始化資料庫

```bash
cd src
python evaluator.py
```

### 3. 啟動報告伺服器

```bash
python report_server.py
```

### 4. 開啟瀏覽器

```
http://localhost:5000
```

---

## Demo 展示

### 1. WhatsApp 對話

員工透過 WhatsApp 與 Companion Agent 對話：

```
Employee: 今天處理了一個緊急的客戶問題
Agent:  很棒！請問你是如何決定優先順序的？
Employee: 我會先看客戶的緊急程度，然後跟老闆確認時程
Agent:  了解！這是很謹慎的做法👍
```

### 2. Evidence Extraction

每次對話後，系統自動萃取行為信號：

```json
{
  "dimension": "CONTEXT_JUDGMENT",
  "inferred_skill": "優先順序判斷",
  "supporting_quote": "我會先看客戶的緊急程度...",
  "confidence": 0.85
}
```

### 3. 評估報告

打開網頁查看完整評估報告：
```
http://localhost:5000/report/demo
```

---

## 技術堆疊

| 項目 | 技術 |
|------|------|
| 對話介面 | OpenClaw + WhatsApp |
| AI Model | OpenAI / Gemini |
| 資料庫 | SQLite |
| 網頁 | Flask + HTML/CSS |
| 部署 | Server (Ubuntu) |

---

## 開發團隊

- **Brandon** - 專案發想
- **隊友** - 商業規劃
- **悟空** - 技術開發

---

## License

MIT

---

*這個系統是為了參加 2026 智慧創新大賞而開發*
