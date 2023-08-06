"""This is a collection of tools to enable the building of microservices."""
import logging
import time
from functools import wraps
from typing import Callable

from pythonjsonlogger import jsonlogger

__version__ = "v0.0.1"

LOG = logging.getLogger("svc_tools")


def timer(log_level: Callable):
    """Time a function and log the time it took to execute.

    If you want to know how long a function takes to execute
    ang log alongside your application logs, then decorate
    your function with this.

    :param log_level: logging method to use in call
    :returns: Whatever your original function returns

    Usage ::
      >>> from svc_tools import timer
      >>> from time import sleep
      >>> import logging
      >>> @timer(logging.warning)
      >>> def myFunc(sleep_time):
      ...     # whatever you want to time
      ...     sleep(sleep_time)
      >>> myFunc(10)
      WARNING:root:myFunc took 10.000502109527588 to run.

    """

    def decorator(func):
        """Decorate the original function."""

        @wraps(func)
        def new_timed_func(*args, **kwargs):
            """Do the timing."""
            start_time = time.time()
            returned_value = func(*args, **kwargs)
            total_time = time.time() - start_time
            log_level(f"{func.__name__} took {total_time} to run.")
            return returned_value

        return new_timed_func

    return decorator


class StackdriverJsonFormatter(jsonlogger.JsonFormatter, object):
    """Format the logs in a way that is friendly with google logger.

        Stackdriver likes it when logs are in json format so
        it can display the logs in their UI.

        :param log_record: the log record that is to be processed
        :return: `dict` object of the log
        :rtype: dict

        Usage ::

          >>> from svc_tools import StackdriverJsonFormatter
          >>> import logging
          >>> HANDLER = logging.StreamHandler(sys.stdout)
          >>> FORMATTER = StackdriverJsonFormatter()
          >>> HANDLER.setFormatter(FORMATTER)
          >>> LOG = logging.getLogger()
          >>> LOG.addHandler(HANDLER)
          >>> LOG.info("This is my log message")

    """

    def __init__(self, *args, fmt="%(levelname) %(message)", **kwargs) -> None:
        """Init the custom formatter from the jsonlogger."""
        jsonlogger.JsonFormatter.__init__(self, *args, fmt=fmt, **kwargs)

    def process_log_record(self, log_record: dict) -> dict:
        """Change logs from standard formatting to json."""

        log_record["severity"] = log_record["levelname"]
        del log_record["levelname"]
        return super(StackdriverJsonFormatter,
                     self).process_log_record(log_record)
