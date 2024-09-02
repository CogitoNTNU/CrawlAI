
from typing import Protocol

class Agent(Protocol):
    def act(self, env) -> int:
        pass

    def save(self, path) -> None:
        pass

    def load(self, path) -> None:
        pass

    def get_genome(self) :
        pass

class Creature():
    def __init__(self, env):
        self.env = env