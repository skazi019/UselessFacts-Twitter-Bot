import logging


class Logger:
    def __init__(self, filename: str) -> None:
        self._logger = logging.getLogger(__name__)
        _handler = logging.FileHandler(filename=filename)
        _handler.setLevel(logging.DEBUG)
        logformat = logging.Formatter(
            "%(asctime)s |  %(name)s |  %(levelname)s |  %(message)s"
        )
        _handler.setFormatter(logformat)
        self._logger.addHandler(_handler)

    def get_logger(self):
        return self._logger
