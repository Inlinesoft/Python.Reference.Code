from datetime import date, datetime
from typing import List

import sqlalchemy

from loader.application.repositories import (
    ConfigAlreadyExists,
    ConfigNotFound,
    ConfigsRepository,
)
from app1.domain.entities import Config

from .base import DBMixin
from .tables import tbl_configs


class DbConfigsRepository(DBMixin, ConfigsRepository):
    @staticmethod
    def map_rows_to_entities(rows):
        entities = []
        not_required = ["id", "is_active", "modified_by", "modified_on"]
        for row in rows:
            item = dict(row)
            for key in not_required:
                item.pop(key)
            hol = Config.from_dict(item)
            entities.append(hol)
        return entities

    def get_configs(
        self,
        namespace: str,
        config_code: str,
        start_date: date,
        end_date: date,
    ) -> List[Config]:
        try:
            result = [
                self.get_active_config(namespace, config_code, start_date)
            ]
        except Exception:
            result = []

        wheres = [
            tbl_configs.c.is_active == sqlalchemy.true(),
            tbl_configs.c.namespace == namespace,
            tbl_configs.c.config_code == config_code,
            tbl_configs.c.as_of >= start_date,
            tbl_configs.c.as_of <= end_date,
        ]

        query = tbl_configs.select().where(sqlalchemy.and_(*wheres))
        rows = self.conn.execute(query)
        result.extend(self.map_rows_to_entities(rows))
        if len(result) <= 0:
            raise ConfigNotFound

        return result

    def get_active_config(
        self,
        namespace: str,
        config_code: str,
        as_of: date = None,
    ) -> Config:
        dt = datetime.now().date()
        if as_of is not None:
            dt = as_of

        wheres = [
            tbl_configs.c.is_active == sqlalchemy.true(),
            tbl_configs.c.namespace == namespace,
            tbl_configs.c.config_code == config_code,
            tbl_configs.c.as_of <= dt,
        ]

        query = (
            tbl_configs.select()
            .where(sqlalchemy.and_(*wheres))
            .order_by(tbl_configs.c.as_of.desc())
        )
        rows = self.conn.execute(query)
        result = self.map_rows_to_entities(rows)
        if len(result) <= 0:
            raise ConfigNotFound
        return result[0]

    def delete(
        self,
        namespace: str,
        config_code: str,
        as_of: date,
        username: str,
    ) -> None:
        wheres = [
            tbl_configs.c.namespace == namespace,
            tbl_configs.c.config_code == config_code,
            tbl_configs.c.as_of == as_of,
        ]
        del_stmt = (
            tbl_configs.update()
            .where(sqlalchemy.and_(*wheres))
            .values(
                is_active=False,
                modified_by=username,
                modified_on=sqlalchemy.func.now(),
            )
        )
        self.conn.execute(del_stmt)

    def save(self, configs: List[Config]):
        for config in configs:
            self._save(config)

    def _save(self, config: Config) -> None:
        item = config.to_dict()
        if item["created_on"] is None:
            item.pop("created_on")

        wheres = [
            tbl_configs.c.is_active == sqlalchemy.true(),
            tbl_configs.c.namespace == config.namespace,
            tbl_configs.c.config_code == config.config_code,
            tbl_configs.c.as_of == config.as_of,
        ]

        query = (
            tbl_configs.select()
            .where(sqlalchemy.and_(*wheres))
            .order_by(tbl_configs.c.as_of.desc())
        )

        rows = self.conn.execute(query)
        result = self.map_rows_to_entities(rows)
        if len(result) > 0:
            raise ConfigAlreadyExists(
                f"Config already exists - "
                f"{config.config_code} - {config.as_of}"
            )
        self.conn.execute(tbl_configs.insert(), item)
