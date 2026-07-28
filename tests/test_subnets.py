"""
Tests for subnet lookup, which turns a client IP into a campus location.
"""

from internet.subnets import lookup, subnets


def test_subnets_are_loaded() -> None:
    assert len(list(subnets())) > 0


def test_lookup_resolves_a_known_campus_address() -> None:
    # 172.25.155.0/24 is the ICT centre.
    assert lookup("172.25.155.10") is not None


def test_lookup_resolves_loopback() -> None:
    # 127.0.0.0/8 is mapped so local development shows a location.
    assert lookup("127.0.0.1") is not None


def test_lookup_returns_none_for_addresses_outside_campus() -> None:
    assert lookup("8.8.8.8") is None


def test_lookup_returns_none_for_malformed_input() -> None:
    assert lookup("not-an-ip") is None
    assert lookup("") is None
