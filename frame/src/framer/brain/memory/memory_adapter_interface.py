from abc import ABC, abstractmethod
from typing import Any, Optional


class MemoryAdapterInterface(ABC):
    @abstractmethod
    def store(self, data: Any, user_id: str = "default") -> int:
        pass

    @abstractmethod
    def retrieve(self, memory_id: int, user_id: str = "default") -> Optional[Any]:
        pass

    @abstractmethod
    def update(self, memory_id: int, data: Any, user_id: str = "default") -> None:
        pass

    @abstractmethod
    def delete(self, memory_id: int, user_id: str = "default") -> None:
        pass
