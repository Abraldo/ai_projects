import streamlit as st
import os
from langchain_core.documents import Document
from app import HybridSearchEngine, HallucinationGuardrail

st.set_page_config(page_title="Enterprise RAG Engine", layout="wide")

st.title("🛡️ Enterprise RAG & Hybrid Search Engine")
st.subheader("Architected with LangChain, LlamaIndex, & Pinecone")

# Sidebar Configuration
st.sidebar.header("🔑 Authentication Setup")
openai_key = st.sidebar.text_input("OpenAI API Key", type="password")
pinecone_key = st.sidebar.text_input("Pinecone API Key", type="password")

if openai_key:
    os.environ["OPENAI_API_KEY"] = openai_key
if pinecone_key:
    os.environ["PINECONE_API_KEY"] = pinecone_key

# Document Ingestion Simulation
st.header("📄 Knowledge Base Management")
st.write("Simulate corporate data uploads:")

default_docs = (
    "Q3 Net Revenue for Retail Corp reached $14.2 Billion, driven by a 12% growth in e-commerce segments.\n"
    "The financial system utilizes a horizontal multi-agent routing ledger to handle cross-border payments under 2 seconds.\n"
    "Total operational expenses grew by 4% due to unexpected supply chain disruptions."
)

doc_input = st.text_area("Paste Corpus Documents (One per line)", value=default_docs, height=150)

if st.button("🚀 Initialize & Index Knowledge Base"):
    if not os.environ.get("OPENAI_API_KEY") or not os.environ.get("PINECONE_API_KEY"):
        st.error("Please provide both API Keys in the sidebar to run embeddings and indexing.")
    else:
        with st.spinner("Parsing text, computing dense embeddings, and building hybrid retrieval indices..."):
            lines = [line.strip() for line in doc_input.split("\n") if line.strip()]
            documents = [Document(page_content=line, metadata={"source": "dashboard_upload"}) for line in lines]
            
            st.session_state["search_engine"] = HybridSearchEngine()
            st.session_state["search_engine"].index_documents(documents)
            st.session_state["guardrail"] = HallucinationGuardrail()
            st.success(f"Successfully built Vector Index and BM25 Sparse Index for {len(documents)} snippets!")

# Query Interface
st.header("🔍 Trust-Verifiable Q&A Interface")
query = st.text_input("Enter your business or financial question:", value="What was the Q3 Net Revenue for Retail Corp?")

if st.button("Query Engine"):
    if "search_engine" not in st.session_state:
        st.error("Please index the documents first using the button above.")
    else:
        engine = st.session_state["search_engine"]
        guardrail = st.session_state["guardrail"]
        
        with st.spinner("Retrieving via Hybrid Fusion and Auditing Output..."):
            # 1. Retrieval Stage
            contexts = engine.retrieve(query)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📚 Retrieved Context (Hybrid Pipeline)")
                if contexts:
                    for i, ctx in enumerate(contexts):
                        st.info(f"**Source Document Block {i+1}:**\n{ctx}")
                else:
                    st.warning("No grounding matches found in dense/sparse vectors.")
            
            with col2:
                st.subheader("🛡️ Hallucination Guardrail Verification")
                final_response, status, raw_generated = guardrail.verify_and_generate(query, contexts)
                
                if status == "SAFE":
                    st.success(final_response)
                elif status == "HALLUCINATION":
                    st.error(final_response)
                    with st.expander("Review Rejected Blueprint (Failed Verification)"):
                        st.write(raw_generated)
                else:
                    st.warning(final_response)
