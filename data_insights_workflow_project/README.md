# Automated Data Insights Pipeline & Business Workflow Orchestrator

Production-ready Text-to-SQL analytics orchestration pipeline linking standard data storage to production database layers, backed by cross-platform automation patterns.

## 🏗️ Architectural Topology Overview

```
 [Natural Language Query] ──► [LangChain Core Engine] ──► [Structured Text-to-SQL Translation]
                                                                  │
                                                                  ▼
 [Business Webhook Dispatches] ◄── [Streamlit Interactive] ◄── [SQLite Memory Execution]
 (n8n / Zapier / Make / Calendly)
```

## 🛠️ Technology Mapping Matrix
- **Core Engineering Layer**: LangChain Pipeline Parsing, Python (Pandas/NumPy standard data structures).
- **Relational Memory System**: SQLAlchemy Engine Core interacting with in-memory standard environments.
- **Workflow Simulation Gateways**: Abstracted hooks modeling **n8n, Zapier, Make, and Calendly API structures**.
- **Interactive Panel Layout**: Streamlit UI framework for runtime execution tracking.

## 🚀 Deployment Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
2. **Execute Automated Architecture Testing**:
   ```bash
   pytest test_pipeline.py -v
   ```
3. **Run Interactive Dashboard Control Deck**:
   ```bash
   streamlit run main_streamlit.py
   ```
