from datetime import date
from typing import Dict, List

from . import exceptions
from .base import UseCase


class ReportHolidaysList(UseCase):
    def execute(
        self,
        year: List[int] = None,
        holiday_type: List[str] = None,
        holiday_reference: List[str] = None,
        holiday_date: List[date] = None,
    ) -> List[Dict]:
        sorted_items = sorted(
            self.uow.holidays_repo.get_holidays(
                year, holiday_type, holiday_reference, holiday_date
            ),
            key=lambda x: x.holiday_date,
            reverse=True,
        )
        return [item.to_dict() for item in sorted_items]


class ReportHolidays(UseCase):
    def execute(
        self, holiday_date: date, holiday_type: str, holiday_reference: str
    ) -> dict:
        items = self.uow.holidays_repo.get_holidays(
            holiday_date=[holiday_date],
            holiday_type=[holiday_type],
            holiday_reference=[holiday_reference],
        )
        if not items:
            raise exceptions.ResourceNotFound
        return items[0].to_dict()
