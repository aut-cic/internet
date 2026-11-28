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


def test_no_subnet_is_shadowed_by_an_earlier_broader_one() -> None:
    # lookup() returns the first match in file order, so a range listed after
    # a broader one that contains it can never match. The broad "wireless"
    # catch-alls must stay at the end of subnets.json.
    entries = list(subnets())
    for later_index, later in enumerate(entries):
        for earlier in entries[:later_index]:
            if earlier.network != later.network:
                assert not later.network.subnet_of(earlier.network), (  # ty: ignore[invalid-argument-type]
                    f"{later.network} ({later.description}) is hidden by "
                    f"{earlier.network} ({earlier.description})"
                )


def test_descriptions_have_no_surrounding_whitespace() -> None:
    for subnet in subnets():
        assert subnet.description == subnet.description.strip()


def test_lookup_prefers_a_faculty_over_the_wireless_catch_all() -> None:
    # 172.21.96.0/19 is Materials and Metallurgy, inside 172.20.0.0/14.
    assert lookup("172.21.96.214") == "دانشکده مهندسی مواد و متالورژی"


def test_lookup_resolves_both_vpn_pools() -> None:
    assert lookup("172.25.220.90") == "VPN"
    assert lookup("172.25.221.10") == "VPN"
