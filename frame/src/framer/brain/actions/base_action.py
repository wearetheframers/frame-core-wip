from abc import ABC, abstractmethod


class BaseAction(ABC):
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    async def execute(self, *args, **kwargs):
        pass
