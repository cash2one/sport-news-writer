# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0021_auto_20150616_1020'),
    ]

    operations = [
        migrations.AddField(
            model_name='synonims',
            name='used',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 6, 17, 7, 19, 52, 437449)),
        ),
    ]
