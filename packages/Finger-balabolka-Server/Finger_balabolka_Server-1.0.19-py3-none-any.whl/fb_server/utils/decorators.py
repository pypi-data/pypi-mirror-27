from functools import wraps

from .log_config import logger

LOGGING = {
            "CRITICAL": logger.critical,
            "ERROR": logger.error,
            "WARNING": logger.warning,
            "INFO": logger.info,
            "DEBUG": logger.debug,
            }

def log(name=__name__, msg=None, level="INFO"):
    def decorator(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            log_decor = LOGGING[level]
            log_decor('{}-{}-{}'.format(name, func.__name__, msg))
            res = func(*args, **kwargs)

            return res
        return decorated
    return decorator