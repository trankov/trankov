from datetime import date, timedelta


def check_year(year: int) -> None:
    if year > 2101: 
        raise AttributeError("Years after 2101 aren't applicable for Gauss formula")
    if year < 33:
        raise AttributeError("Jesus doesn't resurrected yet")


def orthodox_easter(year: int) -> tuple[date, date]:
    check_year(year)
    num2: int = (year % 4 * 2 + year % 7 * 4 + (num1 := (year % 19 * 19 + 15) % 30) * 6 + 6) % 7
    month: int = 3 if (num3 := num1 + num2) < 9 else 4
    easter: date = date(year=year, month=month, day=(num3 + 22, num3 - 9)[month - 3])
    
    return easter, easter + timedelta(days=13)


if __name__ == "__main__":
   oldstyle, newstyle = orthodox_easter(date.today().year)
   print(f'{oldstyle=}, {newstyle=}')
