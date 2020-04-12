from covidapi.import_data_jh import parse_datetime
from datetime import datetime
import pytest


def test_parse_iso_datetime():
    assert parse_datetime('2020-04-11 22:45:33') == datetime(2020, 4, 11, 22, 45, 33)


def test_parse_us_datetime():
    assert parse_datetime('3/29/20 23:08') == datetime(2020, 3, 29, 23, 8)


def test_blank_datetime_raises_valueerror():
    with pytest.raises(ValueError):
        parse_datetime('')


def test_none_datetime_raises_valueerror():
    with pytest.raises(ValueError):
        parse_datetime(None)


def test_unknown_format_datetime_raises_valueerror():
    with pytest.raises(ValueError):
        parse_datetime('29/3/20 23:08')
