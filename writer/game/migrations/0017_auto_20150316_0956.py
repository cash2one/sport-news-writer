# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_auto_20150316_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='action',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 3, 16, 9, 56, 3, 406807)),
            preserve_default=True,
        ),
    ]
