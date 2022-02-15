from background_task import background
from background_task.models import Task
from django.utils import timezone
from .jobs.ru_worship_three_songs_job import RuWorshipTheeSongsJob
from .jobs.simple_job import SimpleJob
from .jobs.sunday_mailing_at_9utc_job import SundayMailingAt9utcJob
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

    tasks = Task.objects.filter(verbose_name="Sunday Mailing at 6:00utc")
    if len(tasks) == 0:
        run_sunday_mailing_at_9_00(
            '',
            schedule=timezone.datetime(2022, 2, 20, 6),
            verbose_name='Sunday Mailing at 6:00utc',
            repeat=Task.WEEKLY,
            repeat_until=None
        )


    # run_each_five_minute_jobs('', verbose_name='Each 5 Minute Jobs', repeat=60*5, repeat_until=None)
    # run_each_hour_jobs('', verbose_name='Each Hour Jobs', repeat=Task.HOURLY, repeat_until=None)
    # run_each_weak_jobs('', verbose_name='Each Week Jobs', repeat=Task.WEEKLY, repeat_until=None)



@background(schedule=5)
def run_each_minute_jobs(parameters):
    youtube_active_broadcast_job = YouTubeActiveBroadcastJob()
    youtube_active_broadcast_job.run(parameters)


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
    job = RuWorshipTheeSongsJob()
    job.run(parameters)


@background()
def run_sunday_mailing_at_9_00(parameters):
    job = SundayMailingAt9utcJob()
    job.run(parameters)
