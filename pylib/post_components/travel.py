import requests
from bs4 import BeautifulSoup, SoupStrainer

from post_components.base import PostInterface


class TravelInfo(PostInterface):
    def __init__(self):
        self.stations_to_check = ["GLC", "GLQ"]
        self.ignore_lines = [
            "no line updates reported",
            "');" "delay-repay",
            "Additional Information",
            "Impact",
            "Customer Advice:",
            "For live journey updates",
            "Need further info",
            "Alterations to services",
            "Last Updated :",
        ]

    @classmethod
    def can_update(cls) -> bool:
        return True

    def get_header(self) -> str:
        return "Travel"

    def get_body(self) -> str:
        parse_only = SoupStrainer(attrs={"id": "lu_update_body"})
        train_info = []
        for station in self.stations_to_check:
            check_url = f"http://www.journeycheck.com/scotrail/route?from=&to={station}&action=search&savedRoute="
            resp = requests.get(check_url)
            update_text = BeautifulSoup(resp.text, "html.parser", parse_only=parse_only).get_text()
            relevant_lines = filter(
                lambda x: x and all(ignore_line.casefold() not in x.casefold() for ignore_line in self.ignore_lines),
                update_text.split("\n"),
            )
            for line in relevant_lines:
                if line not in train_info:
                    train_info.append(line)

        train_string = (
            "\n\n".join(train_info).replace("Glasgow Queen Street", "Queen Street") or "No line problems reported."
        )
        if len(train_string) > 3500:
            return "Trains are fucked."
        else:
            return train_string
