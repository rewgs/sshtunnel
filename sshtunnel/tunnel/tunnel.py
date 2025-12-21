from typing import Optional

from paramiko import SSHConfig, SSHConfigDict

from sshtunnel.host import Local, Remote
from sshtunnel.ssh_config import default_file


# NOTE: This is a re-write of SSHTunnelForwarder.
class Tunnel:
    """
    SSH tunnel class.

    Initializes an SSH tunnel to a remote host according to the input arguments.

    Optionally:
        - Reads an SSH configuration file (typically `~/.ssh/config`)
        - Loads keys from a running SSH agent (i.e. Pageant, GNOME Keyring)
    """

    def __init__(
        self,
        ssh_host: Remote,
        # NOTE: Using paramiko.SSHConfig instead of what is basically a thin wrapper for it.
        # ssh_config: SSH_Config,
        remote_host: Remote,
        local_host: Optional[Local] = None,
    ):
        self.ssh_host: Remote = ssh_host
        # NOTE: Using paramiko.SSHConfig instead of what is basically a thin wrapper for it.
        # self.ssh_config: SSH_Config = ssh_config
        self.remote_host: Remote = remote_host
        self.local_host: Local = (
            local_host if local_host is not None else Local(port=22)
        )

    def _read_ssh_config(self):
        try:
            with open(default_file, "r") as f:
                ssh_config: SSHConfig = SSHConfig().from_file(f)

                # Looks for information for the destination system
                hostname_info: SSHConfigDict = ssh_config.lookup(self.ssh_host.name)
        # TODO:
        # - Offer to point to a different file?
        # - Attach to logger.warning like in original version?
        except FileNotFoundError as error:
            raise error
