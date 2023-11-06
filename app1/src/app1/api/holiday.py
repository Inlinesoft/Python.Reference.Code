from datetime import date, datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from pydantic import BaseModel as ViewModel

from pricers.application.use_cases import (
    DeleteHoliday,
    InsertHolidays,
    ReportHolidays,
    ReportHolidaysList,
)

from ...helpers.conversions import from_utc_to_london_tz
from .security import User, get_current_user


class HolidayBase(ViewModel):
    holiday_date: date
    holiday_name: str
    holiday_type: str
    holiday_reference: str
    reason: str


class Holiday(HolidayBase):
    created_by: str
    created_on: Optional[datetime]


class HolidayInsert(HolidayBase):
    pass


class HolidayInsertBulk(ViewModel):
    holidays: List[HolidayInsert]


class Holidays(ViewModel):
    holidays: List[Holiday]


router = APIRouter()


def holiday_presenter(item):
    item["created_on"] = from_utc_to_london_tz(item["created_on"])
    return Holiday(**item)


@router.get("", response_model=Holidays)
def report_holidays(
    year: List[int] = Query(None),
    holiday_type: List[str] = Query(None),
    holiday_reference: List[str] = Query(None),
    holiday_date: List[date] = Query(None),
):
    use_case = ReportHolidaysList()
    holidays = use_case.execute(
        year, holiday_type, holiday_reference, holiday_date
    )
    holiday = Holidays(holidays=[holiday_presenter(d) for d in holidays])
    return holiday


@router.get(
    "/{holiday_date}/{holiday_type}/{holiday_reference}",
    response_model=Holiday,
)
def report_holiday(
    holiday_date: date,
    holiday_type: str,
    holiday_reference: str,
):
    use_case = ReportHolidays()
    holiday = use_case.execute(holiday_date, holiday_type, holiday_reference)
    return holiday_presenter(holiday)


@router.delete(
    "/{holiday_date}/{holiday_type}/{holiday_reference}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_holiday(
    holiday_date: date,
    holiday_type: str,
    holiday_reference: str,
    user: User = Depends(get_current_user),
):
    use_case = DeleteHoliday()
    use_case.execute(
        holiday_date, holiday_type, holiday_reference, user.username
    )


@router.post(
    "/bulk",
    status_code=status.HTTP_200_OK,
)
def insert_holidays_bulk(
    item: HolidayInsertBulk,
    user: User = Depends(get_current_user),
):
    use_case = InsertHolidays()
    values = [item.dict() for item in item.holidays]
    resp = use_case.execute(values, user.username)
    return resp
