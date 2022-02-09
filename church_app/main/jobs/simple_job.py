from .job_base import JobBase


class SimpleJob(JobBase):
    def __init__(self):
        super().__init__(self.__class__.__name__.__str__())

    def execute(self, parameters):
        pass

