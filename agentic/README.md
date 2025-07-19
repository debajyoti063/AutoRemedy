# Agentic System Overview

This directory contains the core agentic system for AutoRemedy.

## Core Concepts

- **Sensor**: Receives or fetches events from external systems (e.g., job monitors, webhooks).
- **Effector**: Executes actions to remediate issues or notify stakeholders (e.g., send notification, restart job).
- **ReasoningModule**: Decides what actions to take given an event and context (e.g., rule-based, LLM-powered).
- **Agent**: The main loop that ties everything together.

## Adding New Components

- **Sensor**: Subclass `Sensor` from `base.py` and implement `get_event()`.
- **Effector**: Subclass `Effector` from `base.py` and implement `execute()`.
- **ReasoningModule**: Subclass `ReasoningModule` from `base.py` and implement `decide()`.

## Example Usage

```
from agentic.agent import Agent
from my_sensors import MySensor
from my_effectors import MyEffector
from my_reasoning import MyReasoningModule

agent = Agent(
    sensors=[MySensor()],
    effectors=[MyEffector()],
    reasoning_module=MyReasoningModule()
)
agent.run_forever()
```

## Extending
- Add new sensors/effectors/reasoning modules as plugins for easy extensibility.
- See `base.py` for interface definitions. 