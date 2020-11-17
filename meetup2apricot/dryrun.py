"""Allow decorated methods to log activity instead of performing activity.

Inspired by these projects:

Dryable - enabling --dry-run functionality
https://github.com/haarcuba/dryable

drypy - easy dryrun mode for Python
https://github.com/dzanotelli/drypy
"""

import logging

logger = logging.getLogger("dryrun")


def dryrunnable(flag_name="dryrun"):
    """Return a class decorator to accept a named flag during object initialization."""

    def decorator(cls):
        """Decorate a class with a wrapper that accepts a named flag during
        object initialization."""

        def wrapper(*args, **kwargs):
            """Wrap a class __init__ method, accepting a named flag among the
            keyword arguments."""
            dry_run = kwargs.get(flag_name, False)
            reduced_kwargs = {
                key: value for key, value in kwargs.items() if key != flag_name
            }
            obj = cls(*args, **reduced_kwargs)
            setattr(obj, flag_name, dry_run)
            return obj

        return wrapper

    return decorator


def method(value=None, *, flag_name="dryrun"):
    """Return a method decorator to skip a function in dry run mode, returning
    the value, if the named flag is true."""

    def decorator(method):
        """Decorate a method with a wrapper that gates operation with a named
        flag."""

        def wrapper(obj, *args, **kwargs):
            """Wrap a function, skipping it in dry run mode it the named flag is
            true and returning the value. The function runs normally if the
            flag is false."""
            dry_run = getattr(obj, flag_name, False)
            if dry_run:
                log_method_call(method, obj, *args, **kwargs)
                return value
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
