import urllib.error, urllib.request

from datetime import date, datetime, timedelta
from typing import Union



class DaysMap:
    """
    Start and end date period info.
      `duration`  the number of days in the period (inclusive)
      `days_off`  the number of "days off" according to isdayoff.ru
      `weekends`  the number of Saturdays and Sundays
      `public`    the number of official public holidays
      `generic`   the number of supposedly days of if the service is unavailable
      `generator` iter dates
    """

    def __init__(
        self,
        date_start: Union[date, datetime],
        date_end: Union[date, datetime],
    ) -> None:

        self.date_start = date_start
        self.date_end = date_end

        self.PUBLIC_HOLYDAYS = (
            (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
            (2, 23), (3, 8), (5, 1), (9, 1), (6, 12), (11, 4)
        )

    @property
    def daily(self):
        "To Be Done"
        raise NotImplementedError

    @property
    def days_off(self) -> int:
        if days_map := self.get_daysoff():
            return days_map.count('1') + days_map.count('4')
        raise RuntimeError("Service unavailable")

    @property
    def weekends(self) -> int:
        "Возвращает количество суббот и воскресений в диапазоне"
        days = self.generator()
        return sum(day.isoweekday() in [6, 7] for day in days)

    @property
    def public(self) -> int:
        "Количество официальных выходных"
        days = self.generator()
        return sum((day.month, day.day) in self.PUBLIC_HOLYDAYS for day in days)

    @property
    def generic(self):
        """
        Количество выходных + праздников (т.к. они переносятся), минус один
        день, если последний день пребывания — воскресенье
        """
        return self.public + self.weekends - (1 if self.date_end.isoweekday() == 7 else 0)

    @property
    def duration(self) -> int:
        return (self.date_end - self.date_start).days + 1 # type: ignore

    def generator(self):
        iter_date = self.date_start
        while iter_date <= self.date_end:
            yield iter_date
            iter_date += timedelta(days=1)

    def get_daysoff(self):
        "Получает с сервера данные о выходных и праздниках или None при ошибке"

        url = (
            f"https://isdayoff.ru/api/getdata?date1={self.date_start.strftime('%Y%m%d')}"
            f"&date2={self.date_end.strftime('%Y%m%d')}&cc=ru&covid=1&pre=1"
        )

        try:
            with urllib.request.urlopen(url) as response:
                days_map = response.read().decode()
        except urllib.error.URLError as err:
            print(err.reason)
            return None

        return days_map
