from abc import ABC, abstractmethod


class PostInterface(ABC):
    @abstractmethod
    def get_header(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_body(self) -> str:
        raise NotImplementedError

    @classmethod
    def can_update(cls) -> bool:
        return False

    @classmethod
    def format_header(cls, header):
        return f"**{header}**\n\n"

    def get_info(self):
        return f"{self.format_header(self.get_header())}{self.get_body()}"
