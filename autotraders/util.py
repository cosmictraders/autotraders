from datetime import datetime


def parse_time(time: str):
    # 2019-08-24T14:15:22Z
    return datetime.strptime(time, "%y-%m-%dT%H:%M:%SZ")
