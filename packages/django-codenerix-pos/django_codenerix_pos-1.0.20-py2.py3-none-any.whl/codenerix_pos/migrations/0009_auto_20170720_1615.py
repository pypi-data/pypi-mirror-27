# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-20 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_pos', '0008_auto_20170720_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poshardware',
            name='kind',
            field=models.CharField(choices=[('TICKET', 'Ticket printer'), ('DNIE', 'DNIe card reader'), ('CASH', 'Cash drawer'), ('PRINT', 'Printer'), ('SIGN', 'Signature pad'), ('QUERY', 'Query service (Ex: Barcode)')], max_length=6, verbose_name='Kind'),
        ),
    ]
