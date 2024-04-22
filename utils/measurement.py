import time
import logging
from logging import config
from functools import wraps
from .logging import configure_logging


log = logging.getLogger(__name__)
logging.config.dictConfig(configure_logging())


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        log.info(f'Starting {func.__name__}')
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        log.info(f'Function {func.__name__} completed total time:{total_time:.4f} seconds')
        return result

    return timeit_wrapper
