# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-24 08:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_products', '0022_typetax_default'),
        ('codenerix_corporate', '0002_auto_20170724_0832'),
        ('codenerix_invoicing', '0022_auto_20170724_0832'),
        ('codenerix_pos', '0005_auto_20170719_1454'),
    ]

    operations = [
        migrations.CreateModel(
            name='POSPlant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('name', models.CharField(max_length=250, unique=True, verbose_name='Name')),
                ('billing_series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posplants', to='codenerix_invoicing.BillingSeries', verbose_name=b'Billing series')),
                ('corporate_image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posplants', to='codenerix_corporate.CorporateImage', verbose_name='Corporate image')),
            ],
            options={
                'default_permissions': ('add', 'change', 'delete', 'view', 'list'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='POSProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('enable', models.BooleanField(default=True, verbose_name='Enable')),
                ('pos', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posproducts', to='codenerix_pos.POS', verbose_name='POS')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posproducts', to='codenerix_products.ProductFinal', verbose_name='Product')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view', 'list'),
            },
        ),
        migrations.RemoveField(
            model_name='posslot',
            name='orders',
        ),
        migrations.AddField(
            model_name='poszone',
            name='plant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='zones', to='codenerix_pos.POSPlant', verbose_name='Plant'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='posproduct',
            unique_together=set([('pos', 'product')]),
        ),
    ]
