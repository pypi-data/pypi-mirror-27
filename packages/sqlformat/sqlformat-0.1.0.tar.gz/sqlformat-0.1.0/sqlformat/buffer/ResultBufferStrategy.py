import uuid
from abc import ABC, abstractmethod

class ResultBufferStrategy(ABC):
    """
    Class default do nothing.
    """

    def __init__(self):
        self.change_buffer_id()
        self.buffer_destination = None

    def change_buffer_id(self):
        self.buffer_id = uuid.uuid4()

    def create_buffer(self):
        self.change_buffer_id()
        return self._init_buffer()

    def flush_buffer(self):
        statement =  self._flush_buffer()
        statement.is_latest_statement = True
        return statement

    @abstractmethod
    def _init_buffer(self):
        pass

    @abstractmethod
    def _flush_buffer(self):
        pass
