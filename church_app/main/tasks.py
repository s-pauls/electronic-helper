from background_task import background
from background_task.models import Task
from django.utils import timezone

from .jobs.daily_6utc_job import Daily6utcJob
from .jobs.ru_worship_three_songs_job import RuWorshipTheeSongsJob
from .jobs.youtube_active_broadcast_job import YouTubeActiveBroadcastJob


# https://django-background-tasks.readthedocs.io/en/latest/#repeating-tasks
def run_jobs():

    tasks = Task.objects.filter(verbose_name="Each Minute Jobs")
    if len(tasks) == 0:
        # no task running with this name, go ahead!
        run_each_minute_jobs('', verbose_name='Each Minute Jobs', repeat=60, repeat_until=None)
    else:
        # task already running
        pass

    tasks = Task.objects.filter(verbose_name="RuWorship Each Day at 5:00:utc")
    if len(tasks) == 0:
        # no task running with this name, go ahead!
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

    tasks = Task.objects.filter(verbose_name="Daily at 6:00utc")
    if len(tasks) == 0:
        run_daily_at_9_00(
            '',
            schedule=timezone.datetime(2022, 2, 23, 6),
            verbose_name='Daily at 6:00utc',
            repeat=Task.DAILY,
            repeat_until=None
        )



@background(schedule=5)
def run_each_minute_jobs(parameters):
    youtube_active_broadcast_job = YouTubeActiveBroadcastJob()
    youtube_active_broadcast_job.run(parameters)


@background()
def run_ru_worship_thee_songs_job(parameters):
    job = RuWorshipTheeSongsJob()
    job.run(parameters)


@background()
def run_daily_at_9_00(parameters):
    job = Daily6utcJob()
    job.run(parameters)
