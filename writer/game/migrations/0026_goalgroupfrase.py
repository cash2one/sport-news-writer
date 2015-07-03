# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0025_game_season'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoalGroupFrase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('first', models.BooleanField(default=False)),
                ('duble', models.BooleanField(default=False)),
                ('triple', models.BooleanField(default=False)),
                ('more', models.BooleanField(default=False)),
            ],
        ),
    ]
