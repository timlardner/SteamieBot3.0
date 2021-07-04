from post_components.base import PostInterface
from utils.common import local_time


class Footer(PostInterface):
    def get_header(self) -> str:
        return ""

    @classmethod
    def format_header(cls, header):
        return "\n\n\n\n"

    @classmethod
    def can_update(cls) -> bool:
        return True

    def get_body(self) -> str:
        return f"\n\n^(Last updated at {local_time().strftime('%H:%M')})"

    @classmethod
    def disabled(cls):
        return True
