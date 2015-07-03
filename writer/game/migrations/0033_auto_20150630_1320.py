# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0032_auto_20150630_1313'),
    ]

    operations = [
        migrations.AlterIndexTogether(
            name='game',
            index_together=set([('pub_date', 'campionat'), ('pub_date', 'campionat', 'season')]),
        ),
    ]
