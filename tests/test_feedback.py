import pytest
from feedback.store import store_feedback, get_feedback, event_hash, r
from feedback.adapter import enrich_prompt_with_feedback

# Dummy event for testing
DUMMY_EVENT = {
    "job_id": 123,
    "status": "fail",
    "event_type": "job_issue",
    "details": {
        "timestamp": "2024-07-19T12:00:00Z",
        "source": "TestSource",
        "description": "Disk full error"
    }
}

def test_feedback_submission_and_retrieval():
    store_feedback(DUMMY_EVENT, "clear_temp_files", "ineffective", "Disk still full")
    feedbacks = get_feedback(DUMMY_EVENT)
    assert feedbacks[-1]["feedback"] == "ineffective"
    assert feedbacks[-1]["action"] == "clear_temp_files"
    assert feedbacks[-1]["comment"] == "Disk still full"

def test_prompt_enrichment():
    prompt = "Analyze this log."
    feedbacks = [{"action": "clear_temp_files", "feedback": "ineffective", "comment": "Disk still full"}]
    enriched = enrich_prompt_with_feedback(prompt, feedbacks)
    assert "Feedback history" in enriched and "Disk still full" in enriched

def test_no_feedback():
    # Use a unique event hash to ensure no feedback
    event = dict(DUMMY_EVENT)
    event["job_id"] = 99999
    # Clear feedback for this event hash
    r.delete(f"feedback:event:{event_hash(event)}")
    feedbacks = get_feedback(event)
    assert feedbacks == []
    prompt = "Analyze this log."
    enriched = enrich_prompt_with_feedback(prompt, feedbacks)
    assert enriched == prompt 

def test_multi_agent_feedback():
    from agentic.agent import Agent, MultiAgentOrchestrator
    from agentic.memory import Memory
    from agentic.sensor_sim import SimulatedSensor
    from agentic.reasoning_simple import SimpleReasoningModule
    # Agent 1
    sensor1 = SimulatedSensor()
    memory1 = Memory()
    agent1_cfg = {
        'sensors': [sensor1],
        'effectors': [],
        'reasoning_module': SimpleReasoningModule(),
        'memory': memory1
    }
    # Agent 2
    sensor2 = SimulatedSensor()
    memory2 = Memory()
    agent2_cfg = {
        'sensors': [sensor2],
        'effectors': [],
        'reasoning_module': SimpleReasoningModule(),
        'memory': memory2
    }
    orchestrator = MultiAgentOrchestrator([agent1_cfg, agent2_cfg])
    # Ensure each agent processes at least one event
    max_attempts = 10
    for _ in range(max_attempts):
        orchestrator.run_once()
        if orchestrator.agents[0].memory.history and orchestrator.agents[1].memory.history:
            break
    assert orchestrator.agents[0].memory.history, "Agent 1 did not process any event."
    assert orchestrator.agents[1].memory.history, "Agent 2 did not process any event."
    # Add feedback to agent 1
    orchestrator.agents[0].feedback({'user': 'test', 'rating': 4, 'comment': 'Agent 1 feedback'})
    # Add feedback to agent 2
    orchestrator.agents[1].feedback({'user': 'test', 'rating': 5, 'comment': 'Agent 2 feedback'})
    # Assert feedback is stored independently
    assert orchestrator.agents[0].memory.history[-1]['feedback']['comment'] == 'Agent 1 feedback'
    assert orchestrator.agents[1].memory.history[-1]['feedback']['comment'] == 'Agent 2 feedback' 

def test_self_reflection_module():
    from agentic.self_reflection import SelfReflectionModule
    # Simulate memory with repeated failures and ineffective feedback
    memory = [
        {'event': {'status': 'fail'}, 'feedback': {'rating': 2}},
        {'event': {'status': 'fail'}, 'feedback': {'rating': 5}},
        {'event': {'status': 'fail'}, 'feedback': {'rating': 1}},
    ]
    reflection = SelfReflectionModule(min_failures_for_escalation=2)
    suggestions = reflection.reflect(memory)
    assert suggestions['escalate'] is True
    assert suggestions['review_strategy'] is True 