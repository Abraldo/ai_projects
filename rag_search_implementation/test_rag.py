import pytest
from langchain_core.documents import Document
from app import HybridSearchEngine, GuardrailEngine

@pytest.fixture
def populated_engine():
    """Initializes and runs test cases directly on the engine architecture"""
    engine = HybridSearchEngine(use_local=True)
    mock_data = [
        Document(page_content="Quarterly product margins expanded to 42% due to automation optimizations.", metadata={"source": "internal_test"}),
        Document(page_content="System architecture requires OAuth2 encryption tokens for all outgoing microservices.", metadata={"source": "security_test"})
    ]
    engine.index_documents(mock_data)
    return engine

def test_hybrid_search_retrieval(populated_engine):
    """Verifies semantic keyword and similarity mapping pulls target answers"""
    results = populated_engine.retrieve("What are the quarterly product margins?")
    assert len(results) > 0
    assert "42%" in results[0]

def test_guardrail_blocks_hallucinations():
    """Asserts that out-of-bounds assertions trigger safe rejection faults"""
    guardrail = GuardrailEngine()
    context = ["Quarterly product margins expanded to 42% due to automation optimizations."]
    
    # Query asking about unmentioned things (Q4 forecasts)
    unsafe_query = "What are the projected Q4 stock predictions based on the 42% margin?"
    output = guardrail.execute(unsafe_query, context)
    
    assert output["status"] in ["REJECTED", "HALT"]
    assert "❌" in output["answer"]