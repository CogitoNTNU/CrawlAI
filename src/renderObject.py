from abc import abstractmethod

class RenderObject():
    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def get_position(self):
        pass

    @abstractmethod
    def set_position(self):
        pass

    def set_relative_position(self):
        pass

    def get_relative_position(self):
        pass
