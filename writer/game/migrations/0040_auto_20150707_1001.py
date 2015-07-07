# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0039_auto_20150706_0838'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campionat',
            name='slug',
            field=models.CharField(max_length=160, db_index=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='slug',
            field=models.CharField(db_index=True, max_length=1024, null=True, blank=True),
        ),
    ]
