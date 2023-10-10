import re
from abc import ABCMeta, abstractmethod

from loader_etl.services import api # api_client


class ParserBase(metaclass=ABCMeta):
    def __init__(self, event):
        self.session = api.get_session(event)
        self.base_url = api.get_base_url()
        self.reason = event.get("reason", "lambda trigger")
        self.force = event.get("force", True)

    @classmethod
    def match_file(self, file_name):
        for pattern in self.file_patterns:
            if re.match(pattern[0], file_name):
                return True
        return False

    @abstractmethod
    def run(self, file_path):
        pass


