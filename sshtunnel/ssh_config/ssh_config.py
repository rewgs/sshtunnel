# TODO: Once Python 3.10 becomes minimum version, replace Optional with Unions.

from pathlib import Path
from typing import Optional

import paramiko

# NOTE: In retrospect, the original version is really just a thin wrapper for paramiko.SSHConfig.
# We should probably just stick with paramiko.SSHConfig and not wrap it.
#
# class SSH_Config:
#     def __init__(self):
#         self.default_dir: Path = Path.home().joinpath(".ssh")
#         self.default_config_file: Path = self.default_config_file.joinpath("config")
#         self.ssh_host_key: Optional[str]
#         self.ssh_password: Optional[str]
#         self.ssh_pkey: Optional[str]
#         self.ssh_private_key_password: Optional[str]
#         self.ssh_proxy: Optional[str]
#         self.ssh_proxy_enabled: bool
#         self.ssh_username: Optional[str]
#
#     def read(self):
#         try:
#             with open(self.default_config_file, "r") as f:
#                 ...
#         # TODO:
#         # - Offer to point to a different file?
#         # - Attach to logger.warning like in original version?
#         except FileNotFoundError as error:
#             raise error
