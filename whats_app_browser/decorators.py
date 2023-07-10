import logging
from time import time


def with_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time()
        res = func(*args, **kwargs)
        end_time = time()
        logging.info(f"{func.__name__.ljust(20)}\t-\t{float(start_time - end_time):.3f}s")
        return res

    return wrapper
