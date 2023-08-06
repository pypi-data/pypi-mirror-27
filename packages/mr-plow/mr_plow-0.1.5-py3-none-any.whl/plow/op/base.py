import functools

from ..config import Config


ENV = object()


def get_config(config, *required):
    """Generate config and validate against required parameters.

    If config is not provided, it is provided using Config.from_environment().

    If provided as a dict, Config is built on it directly.

    :param config: a Config object, dict, string, or None.
        If a dict, we use Config(**config).
        If the literal string "ENV" or "env, we use Config.from_environment().
        If a string, we use Config.from_filename(config).
    :param *required: config parameters that must be present.
    """
    if isinstance(config, dict):
        config = Config(**config)
    if isinstance(config, (str, bytes)):
        if config.lower() == 'env':
            config = Config.from_environment()
        else:
            config = Config.from_filename(config)
    if not isinstance(config, Config):
        raise TypeError(f'Config not found (got {config!r})')

    missing = {attr for attr in required if getattr(config, attr) is None}
    if missing:
        raise ValueError(f'required configs {missing!r} not found')
    return config


def inject_config(*required):
    """wrapper for operations that require config.


    Functions must accept a keyword-only arg "config". This wrapper makes it
    optional but the function may make it required.

    See get_config() for explanation of required_config and the `config`
    argument accepted by the wrapped function.
    """
    def wrapper(f):
        @functools.wraps(f)
        def wrapped(*args, config, **kwargs):
            return f(*args, config=get_config(config, *required), **kwargs)
        return wrapped
    return wrapper
