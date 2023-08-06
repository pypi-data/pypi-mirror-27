"""Different ways to log information out of your service."""
from pythonjsonlogger import jsonlogger


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
