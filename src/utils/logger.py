""" Класс простого JSON-логгера """


from contextvars import ContextVar
from datetime import datetime
from json import dumps
from logging import Logger, StreamHandler, Formatter, INFO
from sys import stdout
from uuid import uuid4


class CustomJSONLogger(Logger):

    def __init__(self, name: str, level: int = INFO):

        super().__init__(name)
        handler = StreamHandler(stdout)
        handler.setFormatter(Formatter(""))
        self.handlers.clear()
        self.setLevel(level)
        self.addHandler(handler)
        self.propagate = False
        self.session = ContextVar("SESSION", default=str(uuid4()))

    def _log(self, level: int, msg: dict, *args, **kwargs) -> None:
        """
        Переопределение метода родительского класса для логгирования
        словарей как JSON.
        Временная метка ставится здесь.
        Args:
            level: уровень логгирования;
            msg: словарь-представление логгируемого JSON;
        """

        if not isinstance(msg, dict):
            raise RuntimeError("JSONLogger needs 'dict' object as a message")
        msg["asctime"] = datetime.now().isoformat()
        msg["session"] = self.session.get()
        msg = dumps(msg, ensure_ascii=False)
        super()._log(level, msg, *args, **kwargs)  # noqa
