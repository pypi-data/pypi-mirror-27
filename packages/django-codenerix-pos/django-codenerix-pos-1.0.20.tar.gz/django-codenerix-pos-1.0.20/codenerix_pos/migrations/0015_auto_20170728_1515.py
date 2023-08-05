# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-28 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_pos', '0014_auto_20170727_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pos',
            name='cid',
        ),
        migrations.AddField(
            model_name='pos',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
