from datetime import date

from .base import UseCase


class DeleteHoliday(UseCase):
    def execute(
        self,
        holiday_date: date,
        holiday_type: str,
        holiday_reference: str,
        username: str,
    ) -> None:
        with self.uow:
            self.uow.holidays_repo.delete(
                holiday_date, holiday_type, holiday_reference, username
            )
            self.uow.commit()
