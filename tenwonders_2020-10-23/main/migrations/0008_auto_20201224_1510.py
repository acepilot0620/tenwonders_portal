# Generated by Django 3.1.4 on 2020-12-24 15:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20201224_0934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='work',
            name='row',
        ),
        migrations.AddField(
            model_name='work',
            name='file',
            field=models.FileField(null=True, upload_to='files/'),
        ),
        migrations.AlterField(
            model_name='log',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 24, 15, 10, 14, 24341), null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 24, 15, 10, 14, 25602), null=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 24, 15, 10, 14, 25282), null=True),
        ),
    ]