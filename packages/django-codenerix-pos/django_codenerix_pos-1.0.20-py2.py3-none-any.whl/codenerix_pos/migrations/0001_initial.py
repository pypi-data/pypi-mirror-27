# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-19 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('codenerix_payments', '0018_auto_20170303_0839'),
        ('codenerix_invoicing', '0021_auto_20170531_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='POS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Name')),
                ('token', models.CharField(max_length=40, unique=True, verbose_name='Token')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view', 'list'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='POSHardware',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Name')),
                ('config', jsonfield.fields.JSONField(verbose_name='config')),
                ('kind', models.CharField(choices=[(b'T', 'Ticket'), (b'D', 'DNI'), (b'C', 'Cash'), (b'S', 'Signature'), (b'Q', 'Query')], max_length=1, verbose_name='Name')),
                ('token', models.CharField(blank=True, max_length=40, null=True, verbose_name='Token')),
                ('enable', models.BooleanField(default=True, verbose_name='Enable')),
                ('pos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hardwares', to='codenerix_pos.POS')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view', 'list'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='POSSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Name')),
                ('pos_x', models.IntegerField(blank=True, default=None, editable=False, null=True, verbose_name='Pos X')),
                ('pos_y', models.IntegerField(blank=True, default=None, editable=False, null=True, verbose_name='Pos Y')),
                ('orders', models.ManyToManyField(editable=False, related_name='slots', to='codenerix_invoicing.SalesOrder')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view', 'list'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='POSZone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Name')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view', 'list'),
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='posslot',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='codenerix_pos.POSZone'),
        ),
        migrations.AddField(
            model_name='pos',
            name='hardware',
            field=models.ManyToManyField(related_name='poss', to='codenerix_pos.POSHardware'),
        ),
        migrations.AddField(
            model_name='pos',
            name='payments',
            field=models.ManyToManyField(related_name='poss', to='codenerix_payments.PaymentRequest'),
        ),
        migrations.AddField(
            model_name='pos',
            name='zone',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poss', to='codenerix_pos.POSZone'),
        ),
    ]
