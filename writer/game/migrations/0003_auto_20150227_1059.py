# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20150227_1058'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='city',
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 2, 27, 10, 59, 31, 807051)),
            preserve_default=True,
        ),
    ]
