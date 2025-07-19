from agentic.agent import Agent
from agentic.sensor_sim import SimulatedSensor
from agentic.memory import Memory
from agentic.reasoning_llm import LLMReasoningModule
from notifications.notifier import NotifierEffector

if __name__ == '__main__':
    sensor = SimulatedSensor()
    effector = NotifierEffector()
    reasoning = LLMReasoningModule()
    memory = Memory()
    agent = Agent(
        sensors=[sensor],
        effectors=[effector],
        reasoning_module=reasoning,
        memory=memory
    )
    event_count = 0
    max_events = 5  # Process only 5 events for debugging
    try:
        while event_count < max_events:
            agent.run_once()
            event_count += 1
    except KeyboardInterrupt:
        pass
    print("\nAgent stopped. Event/action history:")
    for record in memory.get_history():
        print(record)
    # Example feedback
    if memory.get_history():
        agent.feedback({'user': 'admin', 'rating': 5, 'comment': 'Handled well'})
        print("\nFeedback added to last record:")
        print(memory.get_history()[-1]) 