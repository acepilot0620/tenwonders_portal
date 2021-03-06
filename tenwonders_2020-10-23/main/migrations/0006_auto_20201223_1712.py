# Generated by Django 3.1.4 on 2020-12-23 17:12

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
        ('main', '0005_auto_20201223_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(default=datetime.datetime(2020, 12, 23, 17, 12, 20, 428278), null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='업무 이름')),
                ('content', models.TextField(verbose_name='업무 내용')),
                ('row', models.TextField()),
                ('assigned_worker', models.ManyToManyField(to='login.Account', verbose_name='배정된 직원')),
            ],
        ),
        migrations.RemoveField(
            model_name='record',
            name='contract',
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 23, 17, 12, 20, 429651), null=True),
        ),
        migrations.AlterField(
            model_name='notice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 23, 17, 12, 20, 429319), null=True),
        ),
        migrations.DeleteModel(
            name='Contract',
        ),
        migrations.DeleteModel(
            name='Record',
        ),
        migrations.AddField(
            model_name='log',
            name='work',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.work'),
        ),
        migrations.AddField(
            model_name='log',
            name='worker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.account'),
        ),
    ]
