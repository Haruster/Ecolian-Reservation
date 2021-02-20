from datetime import datetime, timedelta

from dateutil import relativedelta


def get_date():
    # 1달 더해주어야 한다
    result: datetime = datetime.today() + relativedelta.relativedelta(months=1)
    return result


def find_day_position(date: datetime):
    """
    날짜를 받아서 몇 주 째인지, 무슨 요일인지 반환한다

    :param date: 위치를 얻고자 하는 날짜
    :return nth_week, weekday: 당월의 몇 주 째, 요일 (1~7: Sun~Sat)
    """
    print(date, type(date))

    first_day = date.replace(day=1)
    if first_day.weekday() == 6:  # 일요일
        origin = first_day
    elif first_day.weekday() < 3:
        origin = first_day - timedelta(days=first_day.weekday() + 1)
    else:
        origin = first_day + timedelta(days=6 - first_day.weekday())
    return (date - origin).days // 7 + 1, (date.weekday() + 1) % 7 + 1


def time2int(time_str: str) -> int:
    if ":" not in time_str:
        return int(time_str)
    return int("".join(time_str.split(":")))
