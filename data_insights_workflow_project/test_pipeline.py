import pytest
import os
from app import AutomatedDataPipeline

def test_pipeline_database_bootstrapping():
    pipeline = AutomatedDataPipeline(csv_path="test_leads.csv")
    assert os.path.exists("test_leads.csv")
    schema = pipeline.get_schema()
    assert "leads" in schema
    if os.path.exists("test_leads.csv"):
        os.remove("test_leads.csv")

def test_text_to_sql_generation():
    pipeline = AutomatedDataPipeline(csv_path="test_leads.csv")
    res = pipeline.text_to_sql_execution("Show all new leads")
    assert res["status"] == "SUCCESS"
    assert "SELECT" in res["generated_sql"].upper()
    if os.path.exists("test_leads.csv"):
        os.remove("test_leads.csv")
