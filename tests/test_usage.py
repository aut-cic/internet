"""
Unit tests for the pure reporting helpers in internet.accounting.usage.
"""

import math

import pytest

from internet.accounting.usage import (
    Package,
    Report,
    Usage,
    UsageType,
    bytes_to_str,
)


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, "-"),
        (512, "-"),
        (1024, "1 KB"),
        (1024 * 1024, "1 MB"),
        (1024**3, "1 GB"),
        (1024**4, "1 TB"),
    ],
)
def test_bytes_to_str_units(value: int, expected: str) -> None:
    assert bytes_to_str(value, "en") == expected


def test_bytes_to_str_nan_is_infinity() -> None:
    assert bytes_to_str(math.nan) == "∞"


def test_bytes_to_str_defaults_to_persian_units() -> None:
    assert bytes_to_str(1024**3) == "1 گیگابایت"


def test_bytes_to_str_keeps_one_decimal_above_mb() -> None:
    # 1.5 GB should not be rounded down to a flat "1 GB".
    assert bytes_to_str(int(1.5 * 1024**3), "en") == "1.5 GB"


def test_bytes_to_str_rejects_unknown_language() -> None:
    with pytest.raises(AssertionError):
        bytes_to_str(1024, "de")


def test_usage_type_str_is_lowercase_name() -> None:
    assert str(UsageType.DAILY) == "daily"
    assert str(UsageType.FREE) == "free"


def make_report(groupname: str) -> Report:
    return Report(
        usage_history=[],
        package=Package(),
        groupname=groupname,
        usage=Usage(),
        username="someone",
        sessions=[],
    )


@pytest.mark.parametrize(
    ("groupname", "expected"),
    [
        ("students-H1", UsageType.WEEKLY),
        ("students-H2", UsageType.MONTHLY),
        ("students-H3", UsageType.FREE),
        ("students", UsageType.DAILY),
        ("", UsageType.DAILY),
        # An unknown suffix must not be mistaken for a paid tier.
        ("students-H9", UsageType.DAILY),
    ],
)
def test_get_active_type_from_group_suffix(groupname: str, expected: UsageType) -> None:
    assert make_report(groupname).get_active_type() is expected
