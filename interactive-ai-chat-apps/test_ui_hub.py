import pytest
import os
import json
from app import UIOrchestrationEngine, DeploymentConfig

@pytest.fixture
def clean_ui_engine():
    """Initializes a sandboxed runtime context tracking front-end pipeline deployments."""
    engine = UIOrchestrationEngine()
    engine.deployment_registry_path = "./.test_ui_deployment_registry.json"
    if os.path.exists(engine.deployment_registry_path):
        os.remove(engine.deployment_registry_path)
    engine._initialize_registry()
    return engine

def test_registry_initialization(clean_ui_engine):
    """Confirms deep parsing definitions extract initial configs safely."""
    streamlit_config = clean_ui_engine.get_platform_config("Streamlit")
    assert streamlit_config["platform"] == "Streamlit"
    assert "Customer Support Bot" in streamlit_config["active_agents"]

def test_update_platform_config(clean_ui_engine):
    """Ensures changes modify the tracking records without corruption errors."""
    updated_config = DeploymentConfig(
        platform="Streamlit",
        endpoint_url="http://localhost:9999",
        theme="light",
        active_agents=["Test Agent Core"]
    )
    success = clean_ui_engine.update_platform_config(updated_config)
    assert success is True
    
    refetched = clean_ui_engine.get_platform_config("Streamlit")
    assert refetched["endpoint_url"] == "http://localhost:9999"
    assert refetched["theme"] == "light"
    assert "Test Agent Core" in refetched["active_agents"]

def test_langflow_schema_generation(clean_ui_engine):
    """Validates structural visual topology template matches expected JSON keys."""
    schema = clean_ui_engine.generate_langflow_schema()
    assert "nodes" in schema
    assert "edges" in schema
    assert len(schema["nodes"]) == 3
