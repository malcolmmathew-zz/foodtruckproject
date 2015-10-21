# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20151019_1752'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='location',
        ),
        migrations.AddField(
            model_name='event',
            name='description',
            field=models.TextField(default=b'', max_length=1500),
        ),
    ]
