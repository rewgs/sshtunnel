# TODO: This was simply copied from sshtunnel.py and the _cli_main() function was renamed to main(). This does not work at the moment.
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
