# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20150227_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='city',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 2, 27, 10, 59, 48, 771684)),
            preserve_default=True,
        ),
    ]
