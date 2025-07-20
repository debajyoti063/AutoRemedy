from agentic.agent import Agent, MultiAgentOrchestrator
from agentic.sensor_sim import SimulatedSensor
from agentic.memory import Memory
from agentic.reasoning_llm import LLMReasoningModule
from notifications.notifier import NotifierEffector
from agentic.self_reflection import SelfReflectionModule

if __name__ == '__main__':
    # Agent 1
    sensor1 = SimulatedSensor()
    effector1 = NotifierEffector()
    reasoning1 = LLMReasoningModule()
    memory1 = Memory()
    self_reflection1 = SelfReflectionModule(min_failures_for_escalation=2)
    agent1_cfg = {
        'sensors': [sensor1],
        'effectors': [effector1],
        'reasoning_module': reasoning1,
        'memory': memory1,
        'self_reflection': self_reflection1
    }
    # Agent 2 (could use different sensor/effector/reasoning if desired)
    sensor2 = SimulatedSensor()
    effector2 = NotifierEffector()
    reasoning2 = LLMReasoningModule()
    memory2 = Memory()
    agent2_cfg = {
        'sensors': [sensor2],
        'effectors': [effector2],
        'reasoning_module': reasoning2,
        'memory': memory2
        # No self_reflection for agent 2 (demo)
    }
    orchestrator = MultiAgentOrchestrator([agent1_cfg, agent2_cfg])
    event_count = 0
    max_events = 5  # Process only 5 events for debugging
    try:
        while event_count < max_events:
            orchestrator.run_once()
            event_count += 1
    except KeyboardInterrupt:
        pass
    print("\nMulti-agent orchestrator stopped. Event/action history:")
    for idx, agent in enumerate(orchestrator.agents):
        print(f"\nAgent {idx+1} history:")
        for record in agent.memory.get_history():
            print(record)
    # Example feedback for agent 1
    if orchestrator.agents[0].memory.get_history():
        orchestrator.agents[0].feedback({'user': 'admin', 'rating': 5, 'comment': 'Handled well'})
        print("\nFeedback added to last record of Agent 1:")
        print(orchestrator.agents[0].memory.get_history()[-1]) 