import os
import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field

class DeploymentConfig(BaseModel):
    platform: str = Field(description="The targeting interface platform (Streamlit, Gradio, Retool, LangFlow)")
    endpoint_url: str = Field(description="The mock routing or live deployment access hook.")
    theme: str = Field(default="dark", description="Visual UI presentation styling wrapper.")
    active_agents: List[str] = Field(default_factory=list, description="Array of structural agents assigned to this UI layer.")

class UIOrchestrationEngine:
    def __init__(self):
        self.deployment_registry_path = "./.ui_deployment_registry.json"
        self._initialize_registry()

    def _initialize_registry(self):
        """Pre-seeds the registry with infrastructure configurations for the diverse ecosystem architectures."""
        if not os.path.exists(self.deployment_registry_path):
            initial_configs = {
                "Streamlit": {
                    "platform": "Streamlit",
                    "endpoint_url": "http://localhost:8501",
                    "theme": "dark",
                    "active_agents": ["Customer Support Bot", "Financial Analyzer"]
                },
                "Gradio": {
                    "platform": "Gradio",
                    "endpoint_url": "http://localhost:7860",
                    "theme": "default",
                    "active_agents": ["Vision Model Segmenter", "Speech-to-Text Transcriber"]
                },
                "Retool": {
                    "platform": "Retool",
                    "endpoint_url": "https://retool.com",
                    "theme": "corporate",
                    "active_agents": ["ERP Query Router", "Lead Scoring Agent"]
                },
                "LangFlow": {
                    "platform": "LangFlow",
                    "endpoint_url": "http://localhost:7817/api/v1/run/workflow_id",
                    "theme": "canvas",
                    "active_agents": ["Multi-Agent Graph Orchestrator"]
                }
            }
            with open(self.deployment_registry_path, "w") as f:
                json.dump(initial_configs, f, indent=4)

    def get_platform_config(self, platform_name: str) -> Dict[str, Any]:
        """Retrieves targeted deployment metrics for specific dashboard systems."""
        with open(self.deployment_registry_path, "r") as f:
            registry = json.load(f)
        return registry.get(platform_name, {})

    def update_platform_config(self, config: DeploymentConfig) -> bool:
        """Mutates active deployment states dynamically across orchestration boundaries."""
        try:
            with open(self.deployment_registry_path, "r") as f:
                registry = json.load(f)
            
            registry[config.platform] = config.model_dump()
            
            with open(self.deployment_registry_path, "w") as f:
                json.dump(registry, f, indent=4)
            return True
        except Exception as e:
            print(f"Failed to patch UI deployment configuration registry: {e}")
            return False

    def generate_langflow_schema(self) -> Dict[str, Any]:
        """Generates a structural visual topology template mocking LangFlow JSON canvas mappings."""
        return {
            "id": "langflow-agent-graph-01",
            "nodes": [
                {"id": "input-node-1", "type": "ChatInput", "position": {"x": 100, "y": 250}},
                {"id": "agent-core-2", "type": "OpenAIAgent", "position": {"x": 400, "y": 250}, "params": {"temperature": 0.0}},
                {"id": "output-node-3", "type": "ChatOutput", "position": {"x": 700, "y": 250}}
            ],
            "edges": [
                {"source": "input-node-1", "target": "agent-core-2", "type": "text-stream"},
                {"source": "agent-core-2", "target": "output-node-3", "type": "text-response"}
            ]
        }
