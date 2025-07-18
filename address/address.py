from dataclasses import dataclass


@dataclass
class Address:
    def __init__(self, host: str, port: int):
        self.host: str = host
        self.port: int = port
