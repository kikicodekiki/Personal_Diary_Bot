"""Defines the interface for the Command Design Pattern."""
from abc import ABC, abstractmethod # import needed modules for the creation of an abstract class


class Command(ABC):
    """Abstract base class for all bot commands."""
    @abstractmethod
    def execute(self):
        raise NotImplementedError('You must implement this method.')