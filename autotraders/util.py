from datetime import datetime


def parse_time(time: str):
    return datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.%fZ")
