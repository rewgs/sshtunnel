from dataclasses import dataclass


@dataclass
class Address:
    host: str
    port: int

    def as_string(self) -> str:
        return f"{self.host}:{self.port}"
