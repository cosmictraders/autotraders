from autotraders.shared_models.map_symbol import MapSymbol
from autotraders.time import parse_time


def test_time_parser():
    assert parse_time("2023-05-21T00:07:07.475Z").year == 2023
    assert parse_time("2023-05-21T00:07:07.475Z").month == 5
    assert parse_time("2023-05-21T00:07:07.475Z").day == 21
    assert parse_time("2023-05-21T00:07:07.475Z").hour == 0
    assert parse_time("2023-05-21T00:07:07.475Z").minute == 7
    assert parse_time("2023-05-21T00:07:07.475Z").second == 7


def test_map_symbol():
    s = MapSymbol("X1-TEST")
    s1 = MapSymbol("X1-TEST-V2")
    s2 = MapSymbol("X1-TEST")
    assert s != s1
    assert s == s2
    assert s == MapSymbol(s2)
    assert s / "V2" == s1
    assert s / "-V2" == s1
    try:
        MapSymbol("x1-test-test-test")
        assert False
    except Exception as e:
        assert type(e) is ValueError
    # try:
    #     MapSymbol("x1test-test-test")
    #     assert False
    # except Exception as e:
    #     assert type(e) is ValueError
