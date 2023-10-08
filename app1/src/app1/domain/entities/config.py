from datetime import date, datetime
from typing import Optional

from .base import Entity


class Config(Entity):
    def __init__(
        self,
        namespace: str,
        config_code: str,
        value: dict,
        as_of: date,
        reason: str,
        created_by: str,
        created_on: Optional[datetime] = None,
        is_active: bool = True,
    ):
        self.namespace = namespace
        self.config_code = config_code
        self.value = value
        self.as_of = as_of
        self.reason = reason
        self.created_by = created_by
        self.created_on = created_on
        self.is_active = is_active
