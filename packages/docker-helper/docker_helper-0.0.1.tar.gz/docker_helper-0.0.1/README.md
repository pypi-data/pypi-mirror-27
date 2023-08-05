# Docker Helper

Convenience utilities for Python applications in Docker containers.

## Functions

```python
get_current_container_id()
```

Returns the ID of the container the application is currently running in,
otherwise returns `None` if not running in a container.

```python
read_configuration(key, path=None, default=None,
                   single_config=False, fallback_to_env=True)
```

A convenient way to read configuration values from files with an option
to fall back to using environment variables.
This can come handy to pass in multiple configuration options as key-value pairs
using Docker configs or secrets when working with Swarm services.
When `single_config` is `True`, the configuration file is treated as a single text value
which is useful to read JSON configuration for example for an application.

## License

MIT

