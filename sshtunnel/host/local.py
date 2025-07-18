import socket
from ipaddress import IPv4Address, IPv6Address
from typing import override

from .host import Host


class Local(Host):
    def __init__(self, port: int):
        super().__init__(addr="127.0.0.1", port=port)

    @property
    @override
    def ipv4(self) -> IPv4Address:
        if not hasattr(self, "_ipv4"):
            self._ipv4: IPv4Address = IPv4Address("127.0.0.1")
        return self._ipv4

    @property
    @override
    def ipv6(self) -> IPv6Address:
        if not hasattr(self, "_ipv6"):
            self._ipv6: IPv6Address = self.ipv4.ipv6_mapped
        return self._ipv6

    @property
    @override
    def name(self) -> str:
        if not hasattr(self, "_name"):
            name, _, _ = socket.gethostbyaddr(self.ipv4_as_string)
            self._name: str = name
        return self._name

    @ipv4.setter
    def ipv4(self, value: IPv4Address) -> None:
        self._ipv4 = value

    @ipv6.setter
    def ipv6(self, value: IPv6Address) -> None:
        self._ipv6 = value
