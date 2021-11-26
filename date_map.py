from typing import Union
from datetime import datetime, date, timedelta



class DaysMap:
    """
    Информация о периоде между начальной и конечной датой.
      `duration`  количество дней в периоде (включительно).
      `days_off`  количество нерабочих дней по isdayoff.ru.
      `weekends`  количество суббот и воскресений.
      `public`    количество официальных праздничных выходных.
      `generic`   все теоретически выходные дни без учёта реальности.
      `daily`     детальная информация по дням (TO BE IMPLEMENTED)
      `generator` позволяет циклически перебрать даты в заданном диапазоне
    """

    def __init__(self, 
                 date_start: Union[date, datetime],
                 date_end: Union[date, datetime]) -> None:

        self.date_start = date_start
        self.date_end = date_end

        self.PUBLIC_HOLYDAYS = (
            (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
            (2, 23), (3, 8), (5, 1), (9, 1), (6, 12), (11, 4))

    @property
    def daily(self): # -> dict:
        pass
        

    @property
    def days_off(self) -> int:
        days_map = self.get_daysoff()
        assert days_map is not None
        return days_map.count('1') + days_map.count('4')

    @property
    def weekends(self) -> int:
        "Возвращает количество суббот и воскресений в диапазоне"
        days = self.generator()
        days_off: int = 0
        for day in days:
            if day.isoweekday() in [6, 7]:
                days_off += 1
        return days_off

    @property
    def public(self) -> int:
        "Количество публичных выходных"
        
        days = self.generator()
        days_off: int = 0
        for day in days:
            if (day.month, day.day) in self.PUBLIC_HOLYDAYS:
                days_off += 1
        return days_off

    @property
    def generic(self):
        """
        Количество выходных + праздников (т.к. они переносятся), минус один 
        день, если последний день пребывания — воскресенье
        """
        return self.public + self.weekends - \
                    (1 if self.date_end.isoweekday() == 7 else 0)

    @property
    def duration(self) -> int:
        return (self.date_end - self.date_start).days + 1 # type:ignore

    def generator(self):
        iter_date = self.date_start
        while iter_date <= self.date_end:
            yield iter_date
            iter_date += timedelta(days=1)

    def get_daysoff(self):
        "Получает с сервера данные о выходных и праздниках или None при ошибке"
        
        url = 'https://isdayoff.ru/api/getdata?' + \
              'date1={}&date2={}&cc=ru&covid=1&pre=1'.format(
                                        self.date_start.strftime('%Y%m%d'),
                                        self.date_end.strftime('%Y%m%d')) 
        try:
            with urllib.request.urlopen(url) as response:
                days_map=response.read().decode()
        except urllib.error.URLError as err:
            print(err.reason)
            return None

        return days_map
