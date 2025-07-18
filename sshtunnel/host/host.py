from abc import ABC, abstractmethod
from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import override


class Host(ABC):
    """Base class for local and remote hosts."""

    @staticmethod
    def _addr_is_name(addr: str) -> bool:
        if addr[0].isalpha():
            return True
        return False

    # FIXME: This is a little...cludgey. Make tihs a bit more elegant.
    @staticmethod
    def _addr_is_ip(addr: str) -> bool:
        try:
            _ip = ip_address(addr)
        # TODO: Narrow down to specific Exceptions
        except:
            return False
        if not isinstance(_ip, IPv4Address) | isinstance(_ip, IPv6Address):
            return False
        return True

    def __init__(self, addr: str, port: int = 22):
        if self._addr_is_name(addr):
            self._name: str = addr

        if self._addr_is_ip(addr):
            if isinstance(addr, IPv4Address):
                self._ipv4: IPv4Address = addr
            if isinstance(addr, IPv6Address):
                self._ipv6: IPv6Address = addr

        self.port: int = port

    @property
    @abstractmethod
    def ipv4(self) -> IPv4Address: ...

    @property
    @abstractmethod
    def ipv6(self) -> IPv6Address: ...

    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    def ipv4_as_string(self) -> str:
        return self.ipv4.compressed

    @property
    def ipv6_as_string(self) -> str:
        return self.ipv6.compressed

    def as_string(self, prefer_name: bool = True) -> str:
        """Returns Host formatted as `addr:port`. `addr` defaults to `name`, but can use `ipv4` if `prefer_name` is False."""
        if not prefer_name:
            return f"{self.ipv4_as_string}:{self.port}"
        return f"{self.name}:{self.port}"

    @override
    @abstractmethod
    def __str__(self) -> str: ...
