"""
each section of the university has its own network.
this module handle these networks.
"""
import dataclasses
import ipaddress
import json
import collections.abc


@dataclasses.dataclass()
class Subnet:
    network: ipaddress.IPv4Network | ipaddress.IPv6Network
    description: str


__subnets: list[Subnet] = []
if not (__subnets):
    with open("subnets/subnets.json", encoding="utf-8") as fp:
        for subnet in json.load(fp):
            __subnets.append(
                Subnet(
                    network=ipaddress.ip_network(subnet["subnet"]),
                    description=subnet["description"],
                )
            )


def subnets() -> collections.abc.Iterator[Subnet]:
    return iter(__subnets)


def lookup(ip: str) -> str | None:
    try:
        ip_addr = ipaddress.ip_address(ip)
    except ValueError:
        return None
    for subnet in __subnets:
        if ip_addr in subnet.network:
            return subnet.description
    return None
