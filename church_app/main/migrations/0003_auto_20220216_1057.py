# Generated by Django 3.2.12 on 2022-02-16 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20220216_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriberdb',
            name='subscription_status',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Subscription Status'),
        ),
        migrations.AlterField(
            model_name='subscriberdb',
            name='user_avatar',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='User Avatar'),
        ),
        migrations.AlterField(
            model_name='subscriberdb',
            name='user_language',
            field=models.CharField(blank=True, max_length=5, null=True, verbose_name='User Language'),
        ),
        migrations.AddConstraint(
            model_name='subscriberdb',
            constraint=models.UniqueConstraint(fields=('user_id',), name='unique-content-user_id'),
        ),
    ]