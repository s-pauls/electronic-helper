import abc


from logging import getLogger


class JobBase(metaclass=abc.ABCMeta):
    def __init__(self, job_name: str):
        self._job_name: str = job_name

    @abc.abstractmethod
    def execute(self, parameters):
        pass

    def run(self, parameters):
        logger = getLogger(__name__)

        try:
            logger.info(f'Job {self._job_name} begin')
            self.execute(parameters)
            logger.info(f'Job {self._job_name} finish')
        except Exception:
            logger.exception(f'Job {self._job_name} has error: ')
