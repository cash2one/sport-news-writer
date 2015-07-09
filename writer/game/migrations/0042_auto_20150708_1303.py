# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0041_team_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='slug',
            field=models.CharField(default=b'1', max_length=160, db_index=True),
        ),
    ]
