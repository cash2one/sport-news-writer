# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0022_auto_20150617_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(null=True, blank=True),
        ),
    ]
