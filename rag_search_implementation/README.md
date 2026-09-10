# Enterprise-Grade RAG Engine with Hybrid Search & Hallucination Guardrails

An advanced, production-ready Retrieval-Augmented Generation (RAG) and hybrid search pipeline. This system seamlessly integrates semantic vector indexing with structural keyword search, wrapped in a double-pass programmatic self-reflection layer to ensure zero-hallucination compliance for enterprise environments.

## 🚀 Architectural Design

1. **Dual-Channel Ingestion & Hybrid Retrieval**: Documents are structured into chunk payloads and simultaneously vectorized via dense models (OpenAI `text-embedding-3-small` indexed onto serverless **Pinecone/Weaviate clusters**) and indexed using standard statistical lexical weights (**BM25**). 
2. **Context Fusion Layer**: Retrieval requests execute across both sparse and dense nodes, combining textual precision (for specific identifiers, tracking keys, or exact figures) with deep contextual semantic match vectors.
3. **Double-Pass Audit Guardrails**: Prior to payload presentation, an evaluation runner constructed over **LlamaIndex** executes a grounding validation audit, verifying that the generated text relies explicitly on fetched context segments and dropping outputs containing unauthorized outside data.

## 🛠️ Stack Components

*   **Orchestration Engine:** LangChain Ecosystem & LlamaIndex Data Hubs
*   **Vector Engine:** Pinecone DB / Weaviate DB Architecture
*   **Lexical Scorer:** Rank-BM25 Tokenized Scorer
*   **Auditing Framework:** Zero-Temperature GPT Engines (Self-Consistency Guardrails)
*   **Dashboard Visualizer:** Streamlit Front-End Interface

## 💻 Rapid Setup & Installation

1. **Clone the Infrastructure Files:**
   Ensure you place `requirements.txt`, `app.py`, and `main_streamlit.py` together in your working root directory.

2. **Initialize Environment Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Deploy the Front-End Application:**
   ```bash
   streamlit run main_streamlit.py
   ```

## 📈 System Operational Flows

*   **Ingestion Segment:** Input text or corpus data files are split dynamically into vector blocks. 
*   **Precision Retrieval Check:** Query parameters strike dense geometric matrices and sparse dictionary arrays concurrently, assembling unified context anchors.
*   **Validation Checkpoint:** A strict verification step drops ungrounded statements or answers built from external LLM parameters, protecting downstream dependencies from hallucinated analytics data.
