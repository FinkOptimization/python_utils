from math import floor
from datetime import date, timedelta
from . import WeekDay, get_day_of_the_week_from_date


def _calculate_danish_easter(year: int) -> date:
    """
    From https://da.wikipedia.org/wiki/P%C3%A5ske
    :param year:
    :return:
    """

    a = year % 19
    b = floor(year / 100)
    c = year % 100
    d = floor(b / 4)
    e = b % 4
    f = floor((b + 8) / 25)
    g = floor((b - f + 1) / 3)
    h = (19 * a + b - d - g + 15) % 30
    i = floor(c / 4)
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = floor((a + 11 * h + 22 * l) / 451)
    month = floor((h + l - 7 * m + 114) / 31)
    day = (h + l - 7 * m + 114) % 31 + 1
    return date(year=year, month=month, day=day)


def get_danish_holidays(year: int) -> []:
    new_year = date(year=year, month=1, day=1)
    easter = _calculate_danish_easter(year)
    easter_monday = easter + timedelta(days=1)
    good_friday = easter - timedelta(days=2)
    maundy_thursday = good_friday - timedelta(days=1)
    great_prayers_day = easter + timedelta(days=26)
    ascension_day = maundy_thursday + timedelta(days=42)
    pentecost = easter + timedelta(days=49)
    whit_monday = pentecost + timedelta(days=1)
    constitution_day = date(year=year, month=6, day=5)
    christmas_day = date(year=year, month=12, day=25)
    second_day_of_christmas = christmas_day + timedelta(days=1)
    return sorted([
        (new_year, 'New Year', 'Nytår'),
        (easter, 'Easter Sunday', 'Påskedag'),
        (easter_monday, 'Easter Monday', 'Anden påskedag'),
        (good_friday, 'Good Friday', 'Langfredag'),
        (maundy_thursday, 'Maundy Thursday', 'Skærtorsdag'),
        (great_prayers_day, "Great Prayer's Day", 'Store bededag'),
        (ascension_day, 'Ascension Day', 'Kristi himmelfartsdag'),
        (pentecost, 'Pentecost', 'Pinsedag'),
        (whit_monday, 'Whit Monday', 'Anden pinsedag'),
        (constitution_day, 'Constitution Day', 'Grundlovsdag'),
        (christmas_day, 'Christmas Day', 'Juledag'),
        (second_day_of_christmas, 'Second Day of Christmas', 'Anden juledag')
    ], key=lambda x: x[0])


def get_danish_public_holidays(year: int) -> []:
    return [holiday
            for holiday in get_danish_holidays(year)
            if get_day_of_the_week_from_date(holiday[0]) in WeekDay.weekday]


def get_danish_holidays_between_dates(first_date: date, second_date: date):
    start_date = min(first_date, second_date)
    end_date = max(first_date, second_date)

    holidays = []
    for year in range(start_date.year, end_date.year + 1):
        for holiday in get_danish_holidays(year):
            if start_date <= holiday[0] <= end_date:
                holidays.append(holiday)
    return holidays


def get_danish_public_holidays_between_dates(first_date: date, second_date: date):
    return [holiday
            for holiday in get_danish_holidays_between_dates(first_date, second_date)
            if get_day_of_the_week_from_date(holiday[0]) in WeekDay.weekday]
