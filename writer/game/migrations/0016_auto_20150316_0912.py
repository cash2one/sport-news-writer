# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0015_auto_20150313_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='titlefrase',
            name='with_champion',
            field=models.NullBooleanField(default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 3, 16, 9, 12, 18, 894034)),
            preserve_default=True,
        ),
    ]
