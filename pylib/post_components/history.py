from bs4 import BeautifulSoup, SoupStrainer
import random
import requests

from post_components.base import PostInterface
from utils.common import local_time


class History(PostInterface):
    def get_header(self) -> str:
        return "Today in Scottish History"

    def _format_line(self, line):
        return line.strip().replace("\n", "").replace("\t", "")

    def get_body(self) -> str:
        date_string_for_url = local_time().strftime("%m%B").lower()
        date_string_for_page = (
            f'{local_time().day} {local_time().strftime("%B")}'  # Need to use `.day` to get non-zero padded
        )

        base = f"https://www.undiscoveredscotland.co.uk/usfeatures/onthisday/{date_string_for_url}.html"
        r = requests.get(base)
        p_only = SoupStrainer("p")
        soup = BeautifulSoup(r.text, 'html.parser', parse_only=p_only)
        formatted_lines = [self._format_line(line.text) for line in soup]
        today_lines = [line for line in formatted_lines if line.startswith(date_string_for_page)]
        chosen_line = random.choice(today_lines)
        return chosen_line
