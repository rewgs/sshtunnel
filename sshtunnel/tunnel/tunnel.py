from sshtunnel.address.address import Address
from sshtunnel.ssh_config.ssh_config import SSH_Config


# NOTE: This is a re-write of SSHTunnelForwarder.
class Tunnel:
    """SSH tunnel class."""

    def __init__(self, address: Address, ssh_config: SSH_Config):
        self.address: Address = address
        self.ssh_config: SSH_Config = ssh_config
