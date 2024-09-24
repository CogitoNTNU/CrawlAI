from state import State


class GameStateManager:
    __instance = None
    currentState: State
    def __init__(self):
        """ Virtually private constructor. """
        if GameStateManager.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            GameStateManager.__instance = self


    def set_state(self, state: State):
        self.currentState = state 

    def get_state(self):
        pass
    
    @staticmethod
    def get_instance():
        """ Static access method. """
        if GameStateManager.__instance == None:
            GameStateManager()
        return GameStateManager.__instance
        