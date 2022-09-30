from datetime import date, datetime, timedelta


class OrthEaster:
    def __init__(self, year: int):
        self.year = year
        self._check_year()

    def _check_year(self):
        if self.year > 2101:
            raise ValueError("Years after 2101 aren't applicable for Gauss formula")
        if self.year < 33:
            raise ValueError("Jesus doesn't resurrected yet")

    @property
    def oldstyle(self):
        num2: int = (
            self.year % 4 * 2
            + self.year % 7 * 4
            + (num1 := (self.year % 19 * 19 + 15) % 30) * 6
            + 6
        ) % 7
        month: int = 3 if (num3 := num1 + num2) < 9 else 4
        return date(year=self.year, month=month, day=(num3 + 22, num3 - 9)[month - 3])

    @property
    def newstyle(self):
        return self.oldstyle + timedelta(days=13)


if __name__ == "__main__":
    easter = OrthEaster(datetime.now().year)
    print(easter.oldstyle, easter.newstyle)
