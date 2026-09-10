import os
import time
import json
import hashlib
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from diskcache import Cache
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

# Initialize API Key Configuration
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "your-openai-key")

# System Infrastructure: Initializing Persistent Disk Cache for Cost Optimization
cache_store = Cache("./.rag_response_cache")

class HumanFeedback(BaseModel):
    approved: bool = Field(description="True if the agent answer is accurate and safe, False otherwise.")
    correction: Optional[str] = Field(default=None, description="Corrected textual baseline provided by the human auditor.")
    rating: int = Field(description="System score quality from 1 (poor) to 5 (excellent).")

class AgentPerformanceMetric:
    @staticmethod
    def calculate_cost(tokens_in: int, tokens_out: int, model_name: str) -> float:
        """Calculates exact execution cost tracking based on standard enterprise models"""
        # Blended enterprise rates per 1K tokens
        pricing = {
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
            "gpt-4o": {"input": 0.0025, "output": 0.010}
        }
        rates = pricing.get(model_name, pricing["gpt-4o-mini"])
        return ((tokens_in / 1000) * rates["input"]) + ((tokens_out / 1000) * rates["output"])

class MonitoredOptimizationEngine:
    def __init__(self, model_name: str = "gpt-4o-mini", cache_enabled: bool = True):
        self.model_name = model_name
        self.cache_enabled = cache_enabled
        self.llm = ChatOpenAI(model=self.model_name, temperature=0.0)
        self.logs_path = "./.agent_telemetry_logs.json"
        
        # Ensure telemetry persistence layer exists
        if not os.path.exists(self.logs_path):
            with open(self.logs_path, "w") as f:
                json.dump([], f)

    def _generate_cache_key(self, prompt: str) -> str:
        """Generates deterministic hash keys to represent incoming network queries"""
        return hashlib.sha256(prompt.strip().lower().encode('utf-8')).hexdigest()

    def _log_event(self, log_entry: Dict[str, Any]):
        """Persists granular engineering execution metrics to the logging dashboard backend"""
        try:
            with open(self.logs_path, "r") as f:
                logs = json.load(f)
            logs.append(log_entry)
            with open(self.logs_path, "w") as f:
                json.dump(logs, f, indent=4)
        except Exception as e:
            print(f"Telemetry logging error: {e}")

    def execute_agent(self, prompt: str, bypass_cache: bool = False) -> Dict[str, Any]:
        """Executes an agent request optimizing for cost and latency while gathering metrics"""
        start_time = time.perf_counter()
        cache_key = self._generate_cache_key(prompt)
        
        # 1. Deduplication & Caching Check
        if self.cache_enabled and not bypass_cache:
            cached_data = cache_store.get(cache_key)
            if cached_data:
                latency = (time.perf_counter() - start_time) * 1000  # Convert to ms
                log_entry = {
                    "timestamp": time.time(),
                    "prompt": prompt,
                    "answer": cached_data["answer"],
                    "latency_ms": latency,
                    "cost_usd": 0.0,  # Zero operational expense on hit
                    "cache_status": "HIT",
                    "tokens_used": 0,
                    "model": self.model_name,
                    "error": None,
                    "human_verified": False
                }
                self._log_event(log_entry)
                return log_entry

        # 2. Live Network Inference Route
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            latency = (time.perf_counter() - start_time) * 1000
            
            # Extract underlying token allocations
            metadata = response.response_metadata.get("token_usage", {})
            prompt_tokens = metadata.get("prompt_tokens", 0)
            completion_tokens = metadata.get("completion_tokens", 0)
            total_tokens = prompt_tokens + completion_tokens
            
            calculated_cost = AgentPerformanceMetric.calculate_cost(prompt_tokens, completion_tokens, self.model_name)
            answer_text = response.content
            
            # Save optimization state
            if self.cache_enabled:
                cache_store.set(cache_key, {"answer": answer_text, "tokens": total_tokens}, expire=86400)

            log_entry = {
                "timestamp": time.time(),
                "prompt": prompt,
                "answer": answer_text,
                "latency_ms": latency,
                "cost_usd": calculated_cost,
                "cache_status": "MISS",
                "tokens_used": total_tokens,
                "model": self.model_name,
                "error": None,
                "human_verified": False
            }
            
        except Exception as e:
            latency = (time.perf_counter() - start_time) * 1000
            log_entry = {
                "timestamp": time.time(),
                "prompt": prompt,
                "answer": "❌ Operational Engine Execution Failure",
                "latency_ms": latency,
                "cost_usd": 0.0,
                "cache_status": "ERROR",
                "tokens_used": 0,
                "model": self.model_name,
                "error": str(e),
                "human_verified": False
            }
            
        self._log_event(log_entry)
        return log_entry

    def apply_human_in_the_loop(self, timestamp: float, feedback: HumanFeedback) -> bool:
        """Appends human verification feedback directly onto historical execution blocks"""
        try:
            with open(self.logs_path, "r") as f:
                logs = json.load(f)
            
            updated = False
            for entry in logs:
                if abs(entry["timestamp"] - timestamp) < 0.01:
                    entry["human_verified"] = True
                    entry["human_metrics"] = feedback.model_dump()
                    updated = True
                    break
            
            if updated:
                with open(self.logs_path, "w") as f:
                    json.dump(logs, f, indent=4)
            return updated
        except Exception as e:
            print(f"Feedback alignment error: {e}")
            return False
