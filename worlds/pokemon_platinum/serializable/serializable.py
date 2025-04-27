from abc import ABC, abstractmethod
from typing import Self

class Serializable(ABC):
    @abstractmethod
    def serialize(self) -> bytes:
        pass

    @abstractmethod
    def deserialize(self, data: bytes) -> Self:
        pass

    @abstractmethod
    def size(self) -> int:
        pass