"""Allow decorated methods and functions to log activity instead of performing activity.

Inspired by these projects:

Dryable - enabling --dry-run functionality
https://github.com/haarcuba/dryable

drypy - easy dryrun mode for Python
https://github.com/dzanotelli/drypy
"""

import logging

logger = logging.getLogger("dryrun")


def method(flag_name="dryrun"):
    """Return a method decorator to run a function in dry run mode if the named
    flag is true."""

    def decorator(method):
        """Decorate a method with a wrapper that gates operation with a named
        flag."""

        def wrapper(obj, *args, **kwargs):
            """Wrap a function, running it in dry run mode it the named flag is
            true. The function runs normally if the flag is false."""
            dry_run = getattr(obj, flag_name, False)
            if dry_run:
                return log_method_call(method, obj, *args, **kwargs)
            else:
                return method(obj, *args, **kwargs)

        return wrapper

    return decorator


def log_method_call(method, obj, *args, **kwargs):
    """Log a method call by an object with some arguments."""
    arg_text = ", ".join((f"{arg!r}" for arg in args))
    kwarg_text = ", ".join((f"{key:s}={value!r}" for key, value in kwargs.items()))
    non_blank_all_args = filter(None, [arg_text, kwarg_text])
    all_args_text = ", ".join(non_blank_all_args)
    method_name = method.__name__
    logger.info(f"Skipped {obj!r}.{method_name:s}({all_args_text:s})")


# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 autoindent
