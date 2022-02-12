# Generated by Django 3.2.12 on 2022-02-11 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YouTubeBroadcastsDb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('youtube_id', models.CharField(max_length=50, verbose_name='YouTube ID')),
                ('youtube_title', models.CharField(max_length=200, verbose_name='LiveChat ID')),
                ('status', models.CharField(max_length=20, verbose_name='Broadcast Status')),
                ('live_chat_id', models.CharField(max_length=100, verbose_name='LiveChat ID')),
                ('live_chat_next_page_token', models.CharField(max_length=100, verbose_name='Next Page Token')),
                ('create_datetime', models.DateTimeField(verbose_name='Create Date')),
                ('scheduled_start_time', models.DateTimeField(verbose_name='Scheduled Start Time')),
            ],
            options={
                'verbose_name': 'YouTube трансляция',
                'verbose_name_plural': 'YouTube трансляции',
            },
        ),
        migrations.AddIndex(
            model_name='youtubebroadcastsdb',
            index=models.Index(fields=['youtube_id'], name='main_youtub_youtube_c210f7_idx'),
        ),
    ]