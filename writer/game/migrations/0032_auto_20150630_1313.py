# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0031_campionat_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='news',
            name='pub_date',
            field=models.DateTimeField(db_index=True),
        ),
        migrations.AlterField(
            model_name='synonims',
            name='title',
            field=models.CharField(max_length=128, db_index=True),
        ),
    ]
