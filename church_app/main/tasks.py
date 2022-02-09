from background_task import background
from background_task.models import Task

from .jobs.simple_job import SimpleJob


def run_jobs():
    run_each_minute_jobs('', verbose_name='Each Minute Jobs', repeat=60, repeat_until=None)
    run_each_five_minute_jobs('', verbose_name='Each 5 Minute Jobs', repeat=60*5, repeat_until=None)
    run_each_hour_jobs('', verbose_name='Each Hour Jobs', repeat=Task.HOURLY, repeat_until=None)
    run_each_weak_jobs('', verbose_name='Each Week Jobs', repeat=Task.WEEKLY, repeat_until=None)


@background(schedule=5)
def run_each_minute_jobs(parameters):
    job = SimpleJob()
    job.run(parameters)


@background(schedule=10)
def run_each_five_minute_jobs(parameters):
    job = SimpleJob()
    job.run(parameters)


@background(schedule=15)
def run_each_hour_jobs(parameters):
    job = SimpleJob()
    job.run(parameters)


@background(schedule=15)
def run_each_weak_jobs(parameters):
    job = SimpleJob()
    job.run(parameters)
