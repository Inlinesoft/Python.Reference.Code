import re
from abc import ABCMeta, abstractmethod

class ParserBase(metaclass=ABCMeta):
    def __init__(self):
        pass

    @classmethod
    def match_file(self, file_name):
        for pattern in self.file_patterns:
            if re.match(pattern[0], file_name):
                return True
        return False

    @abstractmethod
    def extract_file_data(self, file_path):
        pass
   