"""
This module will hold reusable context managers.
"""
import contextlib

@contextlib.contextmanager
def ignored(*exceptions):
    """
    Context manager to be used when we want to ignore exceptions.

    Args:
        exceptions (exception class): exceptions to ignore.

    Example usage:
        with ignored(OSError):
            os.remove('i_probably_do_not_exist')
    """
    try:
        yield
    except exceptions:
        pass
