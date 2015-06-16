# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20150227_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='host',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 2, 27, 15, 6, 29, 473124)),
            preserve_default=True,
        ),
    ]
