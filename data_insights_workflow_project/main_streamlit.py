import streamlit as st
import pandas as pd
from app import AutomatedDataPipeline

st.set_page_config(page_title="Automated Data & Workflows", layout="wide")
st.title("📊 Automated Business Insights & Low-Code Orchestration")
st.write("Text-to-SQL data engineering engine coupled with simulated third-party platform workflows (n8n, Zapier, Make).")

if "pipeline" not in st.session_state:
    st.session_state.pipeline = AutomatedDataPipeline()

col_left, col_right = st.columns([3, 2])

with col_left:
    st.subheader("🔍 Automated Data Insights (Text-to-SQL)")
    user_query = st.text_input(
        "Ask your database an operational question:", 
        "Show me the top 5 candidates with high technical_score and experience_years greater than 5 ordered by probability"
    )
    
    if st.button("Generate & Execute Data Stream"):
        with st.spinner("Processing architectural natural language query..."):
            res = st.session_state.pipeline.text_to_sql_execution(user_query)
            
            if res["status"] == "SUCCESS":
                st.code(res["generated_sql"], language="sql")
                if res["data"]:
                    df_res = pd.DataFrame(res["data"])
                    st.dataframe(df_res)
                    
                    # Target selection for downstream business automation triggering
                    st.session_state.selected_lead = res["data"][0]
                else:
                    st.info("No matching records found for this query parameter configuration.")
            else:
                st.error(f"SQL Compilation/Execution Fault: {res['error']}")

with col_right:
    st.subheader("🚀 Connected Low-Code Business Workflow Automation Engine")
    st.write("Simulate downstream actions across tools like **n8n, Zapier, Bubble, and Calendly** using extracted query states.")
    
    selected_lead = st.session_state.get("selected_lead", None)
    if selected_lead:
        st.markdown(f"**Target Workflow Payload Context Found:** `{selected_lead['candidate_name']}` (Score: {selected_lead['technical_score']})")
        
        platform = st.selectbox("Select Target Automation Orchestrator:", ["n8n Integration Server", "Zapier Webhooks Core", "Make.com Scenario Hub", "Postman AI Builder Gateway"])
        
        if st.button("Trigger Downstream Execution Sequence"):
            payload = {
                "lead_id": selected_lead["lead_id"],
                "candidate": selected_lead["candidate_name"],
                "action": "Schedule Interview via Calendly API & Log to Notion CRM"
            }
            hook_res = st.session_state.pipeline.trigger_webhook_workflow(platform, payload)
            st.json(hook_res)
    else:
        st.info("Run an insight query on the left to extract an operational data payload for the automation sequence.")
