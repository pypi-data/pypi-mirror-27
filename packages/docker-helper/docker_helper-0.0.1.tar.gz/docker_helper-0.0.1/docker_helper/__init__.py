import os


def get_current_container_id():
    """
    Get the ID of the container the application is currently running in,
    otherwise return `None` if not running in a container.
    """

    if not os.path.exists('/proc/1/cgroup'):
        return

    with open('/proc/1/cgroup', 'r') as cgroup:
        for line in cgroup:
            if 'docker/' in line:
                return line.split('/')[-1].strip()


def read_configuration(key, path=None, default=None, single_config=False, fallback_to_env=True):
    """
    Read configuration from a file, Docker config or secret or from the environment variables.

    :param key: the configuration key
    :param path: the path of the configuration file (regular file or Docker config or secret)
    :param default: the default value when not found elsewhere (default: `None`)
    :param single_config: treat the configuration file as containing the full configuration,
        otherwise the file is expected to be a '=' separated key-value list line by line
        (default: `False`)
    :param fallback_to_env: look for the configuration key in the environment variables
        if not found elsewhere (default: `True`)
    """

    if path and os.path.exists(path):
        with open(path, 'r') as config_file:
            if single_config:
                return config_file.read()

            for line in config_file:
                if line.startswith('%s=' % key):
                    return line.split('=', 1)[1].strip()

    if fallback_to_env and key in os.environ:
        return os.environ[key]

    return default

