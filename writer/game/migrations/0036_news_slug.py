# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0035_remove_team_couch'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='slug',
            field=models.CharField(max_length=1024, null=True, blank=True),
        ),
    ]
