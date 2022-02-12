import abc


from logging import getLogger


class HandlerBase(metaclass=abc.ABCMeta):
    def __init__(self, handler_name: str):
        self._handler_name: str = handler_name

    @abc.abstractmethod
    def execute(self, parameters):
        pass

    def handle(self, parameters):
        logger = getLogger(__name__)

        try:
            self.execute(parameters)
        except Exception:
            logger.exception(f'Handler {self._handler_name} has error')
            raise
