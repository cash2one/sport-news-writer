# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0034_auto_20150702_0931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='couch',
        ),
    ]
