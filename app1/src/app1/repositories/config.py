from abc import ABCMeta, abstractmethod
from datetime import date
from typing import List

from loader.domain.entities import Config


class ConfigNotFound(Exception):
    pass


class ConfigAlreadyExists(Exception):
    pass


class ConfigsRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_configs(
        self,
        namespace: str,
        config_code: str,
        start_date: date,
        end_date: date,
    ) -> List[Config]:
        pass

    @abstractmethod
    def get_active_config(
        self,
        namespace: str,
        config_code: str,
        as_of: date = None,
    ) -> Config:
        pass

    @abstractmethod
    def delete(
        self,
        namespace: str,
        config_code: str,
        as_of: date,
        username: str,
    ) -> None:
        pass

    @abstractmethod
    def save(self, configs: List[Config]):
        pass
