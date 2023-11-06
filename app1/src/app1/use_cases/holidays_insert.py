from typing import List

from pricers.domain.entities import Holiday

from ..repositories import HolidayAlreadyExists
from . import exceptions
from .base import UseCase


class InsertHolidays(UseCase):
    def execute(self, values: List[dict], username: str) -> dict:
        holidays = []
        for value in values:
            value["created_by"] = username
            holiday = Holiday.from_dict(value)
            holidays.append(holiday)

        with self.uow:
            try:
                self.uow.holidays_repo.save(holidays)
                self.uow.commit()
            except HolidayAlreadyExists as exc:
                raise exceptions.ResourceAlreadyExists(str(exc))
            else:
                return {"Status": "success"}
