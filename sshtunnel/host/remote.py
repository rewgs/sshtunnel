import socket
from ipaddress import IPv4Address, IPv6Address
from typing import override

from .host import Host


class Remote(Host):
    """A remote host."""

    def __init__(self, addr: str, port: int):
        super().__init__(addr=addr, port=port)

    @property
    @override
    def ipv4(self) -> IPv4Address:
        if not hasattr(self, "_ipv4"):

            # Gets ipv4 from name
            if hasattr(self, "_name"):
                _addr = socket.gethostbyname(self._name)
                _ipv4 = IPv4Address(_addr)
                self._ipv4 = _ipv4

            # Gets ipv4 from ipv6
            if hasattr(self, "_ipv6"):
                _ipv4 = self._ipv6.ipv4_mapped
                if _ipv4 is not None:
                    self._ipv4 = _ipv4

            raise Exception("Could not get ipv4 address")
        return self._ipv4

    @property
    @override
    def ipv6(self) -> IPv6Address:
        if not hasattr(self, "_ipv6"):
            if hasattr(self, "_name"):
                _addr = socket.gethostbyname(self._name)
                _ipv4 = IPv4Address(_addr)
                self._ipv4: IPv4Address = _ipv4
                self._ipv6: IPv6Address = self._ipv4.ipv6_mapped
            elif hasattr(self, "_ipv4"):
                self._ipv6 = self._ipv4.ipv6_mapped
            else:
                raise Exception("Could not get ipv6 address")
        return self._ipv6

    @property
    @override
    def name(self) -> str:
        if not hasattr(self, "_name"):
            if hasattr(self, "_ipv4"):
                name, _, _ = socket.gethostbyaddr(self.ipv4_as_string)
                self._name: str = name
            else:
                raise Exception("Could not get name")
        return self._name

    @ipv4.setter
    def ipv4(self, value: IPv4Address) -> None:
        self._ipv4 = value

    @ipv6.setter
    def ipv6(self, value: IPv6Address) -> None:
        self._ipv6 = value

    # TODO:
    @override
    def __str__(self) -> str: ...
