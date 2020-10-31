from covidapi.import_data_jh import parse_datetime
from datetime import datetime
import pytest


def test_parse_iso_datetime():
    assert parse_datetime('2020-06-12 21:34:29') == datetime(2020, 6, 12, 21, 34, 29)


def test_parse_us_datetime():
    assert parse_datetime('8/24/20 21:27') == datetime(2020, 8, 24, 21, 27)


def test_blank_datetime_raises_valueerror():
    with pytest.raises(ValueError):
        parse_datetime('')


def test_none_datetime_raises_valueerror():
    with pytest.raises(ValueError):
        parse_datetime(None)


def test_unknown_format_datetime_raises_valueerror():
    with pytest.raises(ValueError):
        parse_datetime('24/8/20 21:27')
