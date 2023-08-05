# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-09 11:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_invoicing', '0005_auto_20170309_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorder',
            name='budget',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_sales', to='codenerix_invoicing.SalesBudget', verbose_name='Budget'),
        ),
    ]
