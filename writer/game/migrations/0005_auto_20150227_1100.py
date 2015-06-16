# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20150227_1059'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goal',
            name='author',
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 2, 27, 11, 0, 32, 882573)),
            preserve_default=True,
        ),
    ]
