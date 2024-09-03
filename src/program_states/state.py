from abc import ABC, abstractmethod
from GameStateManager import GameStateManager


class State(ABC):
    gamestate_manager: GameStateManager

    @abstractmethod
    def changeState(self):
        pass