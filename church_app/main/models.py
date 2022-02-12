from django.db import models


# Урок по добавлению таблицы https://youtu.be/6K83dgjkQNw?t=2321

class YouTubeBroadcastsDb(models.Model):
    youtube_id = models.CharField("YouTube ID", max_length=50)
    youtube_title = models.CharField("LiveChat ID", max_length=200)
    status = models.CharField("Broadcast Status", max_length=20)
    live_chat_id = models.CharField("LiveChat ID", max_length=100)
    live_chat_next_page_token = models.CharField("Next Page Token", max_length=100)
    create_datetime = models.DateTimeField("Create Date")
    scheduled_start_time = models.DateTimeField("Scheduled Start Time")

    def __str__(self):
        return self.youtube_title

    class Meta:
        verbose_name = 'YouTube трансляция'
        verbose_name_plural = 'YouTube трансляции'
        indexes = [
            models.Index(fields=['youtube_id'])
        ]
