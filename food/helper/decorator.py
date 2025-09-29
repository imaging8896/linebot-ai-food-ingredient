import functools
import logging
import time


def log_call(logger: logging.Logger):
    def _decorator(func):

        @functools.wraps(func)
        def _wrapper(*args, **kw):
            start = time.time()

            positional_args_str = ', '.join(map(_truncated_str, args))
            keyword_args_str = ', '.join(f'{k}={_truncated_str(v)}' for k, v in kw.items())

            logger.debug(f"{func.__name__}({positional_args_str}{', ' if kw else ''}{keyword_args_str}) called")
            result = func(*args, **kw)
            logger.debug(f"{func.__name__} spent {time.time() - start:.2f}")
            return result
        return _wrapper
    return _decorator


def _truncated_str(v) -> str:
    max_length = 20
    s = str(v)
    if len(s) > max_length:
        return s[:max_length] + "..."
    return s
