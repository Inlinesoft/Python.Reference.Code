from typing import List

from app1.domain.entities import Config

from ..repositories import ConfigAlreadyExists
from . import exceptions
from .base import BaseService


class ConfigService(BaseService):

    def insert(self, values: List[dict]) -> dict:
        # validate index_tickers
        configs = [Config.from_dict(value) for value in values]

        with self.uow:
            try:
                self.uow.configs_repo.save(configs)
                self.uow.commit()
            except ConfigAlreadyExists as exc:
                raise exceptions.ResourceAlreadyExists(str(exc))
            else:
                return {"Status": "success"}
