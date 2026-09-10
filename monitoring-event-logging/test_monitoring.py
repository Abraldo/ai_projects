import pytest
import os
import json
import time
from app import MonitoredOptimizationEngine, AgentPerformanceMetric, HumanFeedback

@pytest.fixture
def clean_engine():
    """Initializes a sandboxed instance of the optimization tracking framework"""
    engine = MonitoredOptimizationEngine(model_name="gpt-4o-mini", cache_enabled=True)
    # Patch log target paths to isolate test vectors from staging environments
    engine.logs_path = "./.test_telemetry_logs.json"
    if os.path.exists(engine.logs_path):
        os.remove(engine.logs_path)
    with open(engine.logs_path, "w") as f:
        json.dump([], f)
    return engine

def test_cost_calculation():
    """Validates the financial math tracking formula across execution payloads"""
    cost = AgentPerformanceMetric.calculate_cost(tokens_in=1000, tokens_out=2000, model_name="gpt-4o-mini")
    # 1000 input ($0.00015) + 2000 output ($0.0012) = $0.00135
    assert abs(cost - 0.00135) < 1e-6

def test_cache_latency_optimization(clean_engine):
    """Asserts that secondary cache loops execute efficiently with zero financial footprint"""
    prompt = "System Integration Verification Pattern Test"
    
    # Run 1: Cold Execution (Cache Miss)
    first_run = clean_engine.execute_agent(prompt, bypass_cache=False)
    assert first_run["cache_status"] == "MISS"
    
    # Run 2: Cached Execution (Cache Hit)
    second_run = clean_engine.execute_agent(prompt, bypass_cache=False)
    assert second_run["cache_status"] == "HIT"
    assert second_run["cost_usd"] == 0.0
    assert second_run["tokens_used"] == 0

def test_human_in_the_loop_feedback(clean_engine):
    """Confirms alignment logic loops securely mutate database transaction records"""
    prompt = "Human feedback automation loop test case"
    tx = clean_engine.execute_agent(prompt)
    
    feedback = HumanFeedback(approved=True, correction="Optimized validation text", rating=5)
    success = clean_engine.apply_human_in_the_loop(tx["timestamp"], feedback)
    
    assert success is True
    
    with open(clean_engine.logs_path, "r") as f:
        logs = json.load(f)
    assert logs[-1]["human_verified"] is True
    assert logs[-1]["human_metrics"]["rating"] == 5
