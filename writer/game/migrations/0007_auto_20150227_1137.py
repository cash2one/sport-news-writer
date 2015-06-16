# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20150227_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='url',
            field=models.CharField(max_length=512, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 2, 27, 11, 37, 58, 187926)),
            preserve_default=True,
        ),
    ]
