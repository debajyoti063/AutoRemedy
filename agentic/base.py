from abc import ABC, abstractmethod
from typing import Any, Dict

class Sensor(ABC):
    @abstractmethod
    def get_event(self) -> Dict[str, Any]:
        """Fetch or receive an event from the environment or external system."""
        pass

class Effector(ABC):
    @abstractmethod
    def execute(self, action: str, params: Dict[str, Any]) -> Any:
        """Execute an action with given parameters."""
        pass

class ReasoningModule(ABC):
    @abstractmethod
    def decide(self, event: Dict[str, Any], context: Dict[str, Any]) -> list:
        """Given an event and context, return a list of actions to perform."""
        pass 