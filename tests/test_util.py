from autotraders.util import parse_time


def test_time_parser():
    assert parse_time("2019-08-24T14:15:22Z").second == 22
    assert parse_time("2019-08-24T14:15:22Z").minute == 15
    assert parse_time("2019-08-24T14:15:22Z").hour == 14
    assert parse_time("2019-08-24T14:15:22Z").day == 24
    assert parse_time("2019-08-24T14:15:22Z").month == 8
    assert parse_time("2019-08-24T14:15:22Z").year == 2019
