from datetime import datetime
from typing import Optional


def parse_datetime(date_str):
    """
    Parse "last updated" datetimes according to known formats
    """
    if not date_str:
        raise ValueError('Date is missing')
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return datetime.strptime(date_str, r'%m/%d/%y %H:%M')


def clean_optional_field(original: Optional[str]) -> Optional[str]:
    return original if original else None
