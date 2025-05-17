from abc import ABC, abstractmethod

class CncPlugin(ABC):
    @abstractmethod
    def __init__(self, data, db_manager):
        """All plugins must accept data (dict) and db_manager"""
        pass
