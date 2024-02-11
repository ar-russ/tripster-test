# pylint: disable=invalid-name

from src.enums.base import ExtendedEnum


class Filter(str, ExtendedEnum):
    latest = "latest"
    best = "best"
