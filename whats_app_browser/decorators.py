import functools
import logging
from time import time
from functools import wraps


def with_timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time()
        res = func(*args, **kwargs)
        end_time = time()
        logging.info(f"{func.__name__.ljust(20)}\t-\t{float(start_time - end_time):.3f}s")
        return res

    return wrapper
