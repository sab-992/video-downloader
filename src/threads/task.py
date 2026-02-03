from abc import ABC, abstractmethod
from typing import Any


class Task(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def execute(self, thread_id: int) -> Any:
        pass
        