from abc import ABC, abstractmethod

from domain.context import GenerationContext


class Action(ABC):
    @abstractmethod
    def execute(self, context: GenerationContext) -> None:
        ...
