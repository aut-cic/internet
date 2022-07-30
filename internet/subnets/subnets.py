"""
each section of the university has its own network.
this module handle these networks.
"""
import dataclasses
import ipaddress
import json
import typing


@dataclasses.dataclass()
class Subnet:
    network: ipaddress.IPv4Network | ipaddress.IPv6Network
    description: str


__subnets: list[Subnet] = []
if len(__subnets) == 0:
    with open("subnets/subnets.json", encoding="utf-8") as fp:
        for subnet in json.load(fp):
            __subnets.append(
                Subnet(
                    network=ipaddress.ip_network(subnet["subnet"]),
                    description=subnet["description"],
                )
            )


def list() -> typing.Iterator[Subnet]:
    return iter(__subnets)


def lookup(ip: str) -> str | None:
    try:
        ip_addr = ipaddress.ip_address(ip)
        for subnet in __subnets:
            if ip_addr in subnet.network:
                return subnet.description
        return None
    except ValueError:
        return None
