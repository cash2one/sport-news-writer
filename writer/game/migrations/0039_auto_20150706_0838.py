# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0038_player_photos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['-pub_date', '-id']},
        ),
        migrations.AddField(
            model_name='game',
            name='classament_rendered',
            field=models.TextField(null=True, blank=True),
        ),
    ]
