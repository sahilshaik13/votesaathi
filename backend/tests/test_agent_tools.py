import pytest
from agent.tools.get_timeline import get_election_timeline
from agent.tools.explain_step import explain_step
from agent.tools.check_eligibility import check_voter_eligibility
from agent.tools.get_faq import get_faq

def test_timeline_tool():
    """Verify election timeline tool results."""
    # General election
    result = get_election_timeline("general")
    assert "phases" in result
    assert len(result["phases"]) > 0
    assert "description" in result

    # State specific
    result = get_election_timeline("state", state="Telangana")
    assert "Phases" in result
    assert "Telangana" in result

def test_explain_step_tool():
    """Verify process explanation tool."""
    # Registration
    result = explain_step("registration")
    assert "steps" in result
    assert "forms" in result
    
    # EPIC
    result = explain_step("epic")
    assert "steps" in result
    
    # Unknown
    result = explain_step("unknown")
    assert "message" in result

def test_check_eligibility_tool():
    """Verify eligibility logic."""
    # Eligible
    result = check_voter_eligibility(18, True)
    assert result["eligible"] is True
    
    # Too young
    result = check_voter_eligibility(17, True)
    assert result["eligible"] is False
    
    # Not citizen
    result = check_voter_eligibility(25, False)
    assert result["eligible"] is False

def test_faq_tool():
    """Verify FAQ retrieval."""
    result = get_faq("epic")
    assert len(result) > 0
    assert any("EPIC" in item["question"] or "EPIC" in item["answer"] for item in result)
    
    # Default
    result = get_faq("none")
    assert len(result) > 0
