import streamlit as st
import json
import os
import pandas as pd
from app import MonitoredOptimizationEngine, HumanFeedback

st.set_page_config(page_title="Telemetry & Optimization Controls", layout="wide")
st.title("📊 Enterprise Telemetry Dashboard & Cost Optimization Center")
st.write("Real-time optimization matrix tracking latency, model costs, and human evaluation logic loops.")

# Component Persistent Architecture Initialization
if "engine" not in st.session_state:
    st.session_state.engine = MonitoredOptimizationEngine()
if "last_transaction" not in st.session_state:
    st.session_state.last_transaction = None

# Optimization Parameters Deck
with st.sidebar:
    st.header("⚙️ Optimization Parameters")
    selected_model = st.selectbox("Inference Core Alignment:", ["gpt-4o-mini", "gpt-4o"])
    st.session_state.engine.model_name = selected_model
    
    cache_toggle = st.checkbox("Enable Semantic Response Caching", value=True)
    st.session_state.engine.cache_enabled = cache_toggle
    
    st.markdown("---")
    st.subheader("💡 Strategic Trade-Off Analysis")
    st.info(
        "**Quantization & Cache Strategy:**\n"
        "- Response Caching reduces latency to < 15ms and cost to $0.00.\n"
        "- Fine-Tuning optimizes task precision for structured routines but yields higher baseline server cost.\n"
        "- Prompt Engineering maximizes multi-tasking adaptability but consumes massive input token footprints."
    )

# Execution Window
layout_left, layout_right = st.columns([2, 3])

with layout_left:
    st.subheader("🚀 Agent Live Tester")
    user_prompt = st.text_area("Input Action Request Pipeline:", "Calculate compound interest amortization schemas over a 30-year maturity loop.")
    force_refresh = st.checkbox("Bypass Optimization Cache (Force Live Compute)")
    
    if st.button("Dispatch Route Command"):
        with st.spinner("Processing Agent Network..."):
            tx = st.session_state.engine.execute_agent(user_prompt, bypass_cache=force_refresh)
            st.session_state.last_transaction = tx
            
    if st.session_state.last_transaction:
        tx = st.session_state.last_transaction
        st.markdown("#### **Latest Operational Output**")
        if tx["error"]:
            st.error(tx["answer"])
        else:
            st.success(tx["answer"])
            
        # Human-in-the-Loop Feedback Interface
        st.markdown("---")
        st.subheader("🧑‍💻 Human-in-the-Loop Alignment")
        if not tx.get("human_verified", False):
            with st.form("feedback_alignment"):
                rating = st.slider("Response Quality Score:", 1, 5, 5)
                approved = st.radio("Approve for Production deployment?", [True, False])
                notes = st.text_input("Engineering Audit Adjustments:")
                
                if st.form_submit_button("Commit Alignment Feedback"):
                    feedback_obj = HumanFeedback(approved=approved, correction=notes, rating=rating)
                    success = st.session_state.engine.apply_human_in_the_loop(tx["timestamp"], feedback_obj)
                    if success:
                        st.success("Auditor signature embedded cleanly into optimization logs!")
                        st.session_state.last_transaction["human_verified"] = True
                        st.rerun()
        else:
            st.warning("✅ Feedback Loop recorded for this execution frame.")

with layout_right:
    st.subheader("📈 Real-Time Telemetry & Financial Dashboards")
    
    if os.path.exists(st.session_state.engine.logs_path):
        with open(st.session_state.engine.logs_path, "r") as f:
            log_data = json.load(f)
            
        if log_data:
            df = pd.DataFrame(log_data)
            
            # Display Executive Metrics
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            metric_col1.metric("Gross Pipeline Executions", len(df))
            metric_col2.metric("Mean Latency", f"{df['latency_ms'].mean():.2f} ms")
            metric_col3.metric("Total Operational Budget Spent", f"${df['cost_usd'].sum():.6f}")
            
            # Cache Performance Charting
            st.markdown("#### Cache Hit vs. Miss Metrics")
            cache_counts = df['cache_status'].value_value_counts() if 'cache_status' in df else pd.Series()
            st.bar_chart(cache_counts)
            
            # Granular Telemetry View
            st.markdown("#### Complete Trace Log Dataframe")
            st.dataframe(df[["timestamp", "cache_status", "latency_ms", "cost_usd", "tokens_used", "model", "human_verified"]].tail(10))
        else:
            st.info("No active operations tracked inside telemetry storage yet.")
    else:
        st.info("Telemetry system currently standby.")

