from pathlib import Path
from typing import Optional


# TODO: Once Python 3.10 becomes minimum version, replace Optional with Unions.
class SSH_Config:
    def __init__(self):
        self.default_dir: Path = Path.home().joinpath(".ssh")
        self.default_config_file: Path = self.default_config_file.joinpath("config")
        self.ssh_host_key: Optional[str]
        self.ssh_password: Optional[str]
        self.ssh_pkey: Optional[str]
        self.ssh_private_key_password: Optional[str]
        self.ssh_proxy: Optional[str]
        self.ssh_proxy_enabled: bool
        self.ssh_username: Optional[str]
