

from background_task import background
from background_task.models import Task
from django.utils import timezone

from .jobs.ru_worship_three_songs import RuWorshipTheeSongs
from .jobs.simple_job import SimpleJob


# https://django-background-tasks.readthedocs.io/en/latest/#repeating-tasks
def run_jobs():
    # run_each_minute_jobs('', verbose_name='Each Minute Jobs', repeat=60, repeat_until=None)
    # run_each_five_minute_jobs('', verbose_name='Each 5 Minute Jobs', repeat=60*5, repeat_until=None)
    # run_each_hour_jobs('', verbose_name='Each Hour Jobs', repeat=Task.HOURLY, repeat_until=None)
    # run_each_weak_jobs('', verbose_name='Each Week Jobs', repeat=Task.WEEKLY, repeat_until=None)
    run_ru_worship_thee_songs_job('',
                                  schedule=timezone.datetime(2022, 2, 11, 5),
                                  verbose_name='RuWorship Each Day at 5:00:utc',
                                  repeat=Task.DAILY,
                                  repeat_until=None)

    run_ru_worship_thee_songs_job('',
                                  schedule=timezone.datetime(2022, 2, 11, 12),
                                  verbose_name='RuWorship Each Day at 12:00:utc',
                                  repeat=Task.DAILY,
                                  repeat_until=None)


@background(schedule=5)
def run_each_minute_jobs(parameters):
    job = SimpleJob()
    job.run(parameters)


@background(schedule=10)
def run_each_five_minute_jobs(parameters):
    pass


@background(schedule=15)
def run_each_hour_jobs(parameters):
    job = SimpleJob()
    job.run(parameters)


@background(schedule=15)
def run_each_weak_jobs(parameters):
    pass


@background()
def run_ru_worship_thee_songs_job(parameters):
    job = RuWorshipTheeSongs()
    job.run(parameters)

