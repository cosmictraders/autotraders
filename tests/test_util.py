from autotraders.util import parse_time


def test_time_parser():
    assert parse_time("2023-05-21T00:07:07.475Z").year == 2023
    assert parse_time("2023-05-21T00:07:07.475Z").month == 5
    assert parse_time("2023-05-21T00:07:07.475Z").day == 21
    assert parse_time("2023-05-21T00:07:07.475Z").hour == 0
    assert parse_time("2023-05-21T00:07:07.475Z").minute == 7
    assert parse_time("2023-05-21T00:07:07.475Z").second == 7
