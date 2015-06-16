# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_auto_20150319_1022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=1024)),
                ('image', models.ImageField(upload_to=b'images')),
            ],
        ),
        migrations.AlterField(
            model_name='game',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2015, 6, 15, 15, 9, 1, 963675)),
        ),
    ]
