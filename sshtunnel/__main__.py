import argparse

from sshtunnel import __version__


# FIXME: This was simply copied from sshtunnel.py. This does not work at the moment.
def _bindlist(input_str):
    """Define type of data expected for remote and local bind address lists
    Returns a tuple (ip_address, port) whose elements are (str, int)
    """
    try:
        ip_port = input_str.split(":")
        if len(ip_port) == 1:
            _ip = ip_port[0]
            _port = None
        else:
            (_ip, _port) = ip_port
        if not _ip and not _port:
            raise AssertionError
        elif not _port:
            _port = "22"  # default port if not given
        return _ip, int(_port)
    except ValueError:
        raise argparse.ArgumentTypeError(
            "Address tuple must be of type IP_ADDRESS:PORT"
        )
    except AssertionError:
        raise argparse.ArgumentTypeError("Both IP:PORT can't be missing!")


# FIXME: This was simply copied from sshtunnel.py. This does not work at the moment.
def _parse_arguments(args=None):
    """
    Parse arguments directly passed from CLI
    """
    parser = argparse.ArgumentParser(
        description="Pure python ssh tunnel utils\n" "Version {0}".format(__version__),
        formatter_class=argparse.RawTextHelpFormatter,
    )

    parser.add_argument(
        "ssh_address",
        type=str,
        help="SSH server IP address (GW for SSH tunnels)\n"
        'set with "-- ssh_address" if immediately after '
        "-R or -L",
    )

    parser.add_argument(
        "-U",
        "--username",
        type=str,
        dest="ssh_username",
        help="SSH server account username",
    )

    parser.add_argument(
        "-p",
        "--server_port",
        type=int,
        dest="ssh_port",
        default=22,
        help="SSH server TCP port (default: 22)",
    )

    parser.add_argument(
        "-P",
        "--password",
        type=str,
        dest="ssh_password",
        help="SSH server account password",
    )

    parser.add_argument(
        "-R",
        "--remote_bind_address",
        type=_bindlist,
        nargs="+",
        default=[],
        metavar="IP:PORT",
        required=True,
        dest="remote_bind_addresses",
        help="Remote bind address sequence: "
        "ip_1:port_1 ip_2:port_2 ... ip_n:port_n\n"
        "Equivalent to ssh -Lxxxx:IP_ADDRESS:PORT\n"
        "If port is omitted, defaults to 22.\n"
        "Example: -R 10.10.10.10: 10.10.10.10:5900",
    )

    parser.add_argument(
        "-L",
        "--local_bind_address",
        type=_bindlist,
        nargs="*",
        dest="local_bind_addresses",
        metavar="IP:PORT",
        help="Local bind address sequence: "
        "ip_1:port_1 ip_2:port_2 ... ip_n:port_n\n"
        "Elements may also be valid UNIX socket domains: \n"
        "/tmp/foo.sock /tmp/bar.sock ... /tmp/baz.sock\n"
        "Equivalent to ssh -LPORT:xxxxxxxxx:xxxx, "
        "being the local IP address optional.\n"
        "By default it will listen in all interfaces "
        "(0.0.0.0) and choose a random port.\n"
        "Example: -L :40000",
    )

    parser.add_argument("-k", "--ssh_host_key", type=str, help="Gateway's host key")

    parser.add_argument(
        "-K",
        "--private_key_file",
        dest="ssh_private_key",
        metavar="KEY_FILE",
        type=str,
        help="RSA/DSS/ECDSA private key file",
    )

    parser.add_argument(
        "-S",
        "--private_key_password",
        dest="ssh_private_key_password",
        metavar="KEY_PASSWORD",
        type=str,
        help="RSA/DSS/ECDSA private key password",
    )

    parser.add_argument(
        "-t",
        "--threaded",
        action="store_true",
        help="Allow concurrent connections to each tunnel",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Increase output verbosity (default: {0})".format(
            logging.getLevelName(DEFAULT_LOGLEVEL)
        ),
    )

    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="%(prog)s {version}".format(version=__version__),
        help="Show version number and quit",
    )

    parser.add_argument(
        "-x",
        "--proxy",
        type=_bindlist,
        dest="ssh_proxy",
        metavar="IP:PORT",
        help="IP and port of SSH proxy to destination",
    )

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default=SSH_CONFIG_FILE,
        dest="ssh_config_file",
        help="SSH configuration file, defaults to {0}".format(SSH_CONFIG_FILE),
    )

    parser.add_argument(
        "-z",
        "--compress",
        action="store_true",
        dest="compression",
        help="Request server for compression over SSH transport",
    )

    parser.add_argument(
        "-n",
        "--noagent",
        action="store_false",
        dest="allow_agent",
        help="Disable looking for keys from an SSH agent",
    )

    parser.add_argument(
        "-d",
        "--host_pkey_directories",
        nargs="*",
        dest="host_pkey_directories",
        metavar="FOLDER",
        help="List of directories where SSH pkeys (in the format `id_*`) "
        "may be found",
    )
    return vars(parser.parse_args(args))


# FIXME: This was simply copied from sshtunnel.py and the _cli_main() function was renamed to main(). This does not work at the moment.
# TODO: Lose the **extras -- improve this.
def main(args=None, **extras):
    """Pass input arguments to open_tunnel

    Mandatory: ssh_address, -R (remote bind address list)

    Optional:
    -U (username) we may gather it from SSH_CONFIG_FILE or current username
    -p (server_port), defaults to 22
    -P (password)
    -L (local_bind_address), default to 0.0.0.0:22
    -k (ssh_host_key)
    -K (private_key_file), may be gathered from SSH_CONFIG_FILE
    -S (private_key_password)
    -t (threaded), allow concurrent connections over tunnels
    -v (verbose), up to 3 (-vvv) to raise loglevel from ERROR to DEBUG
    -V (version)
    -x (proxy), ProxyCommand's IP:PORT, may be gathered from config file
    -c (ssh_config), ssh configuration file (defaults to SSH_CONFIG_FILE)
    -z (compress)
    -n (noagent), disable looking for keys from an Agent
    -d (host_pkey_directories), look for keys on these folders
    """
    arguments = _parse_arguments(args)
    # Remove all "None" input values
    _remove_none_values(arguments)
    verbosity = min(arguments.pop("verbose"), 4)
    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG, TRACE_LEVEL]
    arguments.setdefault("debug_level", levels[verbosity])
    # do this while supporting py27/py34 instead of merging dicts
    for extra, value in extras.items():
        arguments.setdefault(extra, value)
    with open_tunnel(**arguments) as tunnel:
        if tunnel.is_alive:
            input_(
                """

            Press <Ctrl-C> or <Enter> to stop!

            """
            )


if __name__ == "__main__":
    main()
