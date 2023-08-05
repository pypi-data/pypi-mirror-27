# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-09-01 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_invoicing', '0033_auto_20170901_0939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='saleslinebasket',
            name='discount',
            field=models.FloatField(default=0, verbose_name='Discount (%)'),
        ),
        migrations.AlterField(
            model_name='saleslinebasket',
            name='price',
            field=models.FloatField(verbose_name='Price base'),
        ),
        migrations.AlterField(
            model_name='saleslinebasket',
            name='price_recommended',
            field=models.FloatField(verbose_name='Recomended price base'),
        ),
        migrations.AlterField(
            model_name='saleslineinvoice',
            name='discount',
            field=models.FloatField(default=0, verbose_name='Discount (%)'),
        ),
        migrations.AlterField(
            model_name='saleslineinvoice',
            name='price',
            field=models.FloatField(verbose_name='Price base'),
        ),
        migrations.AlterField(
            model_name='saleslineinvoice',
            name='price_recommended',
            field=models.FloatField(verbose_name='Recomended price base'),
        ),
        migrations.AlterField(
            model_name='saleslineorder',
            name='discount',
            field=models.FloatField(default=0, verbose_name='Discount (%)'),
        ),
        migrations.AlterField(
            model_name='saleslineorder',
            name='price',
            field=models.FloatField(verbose_name='Price base'),
        ),
        migrations.AlterField(
            model_name='saleslineorder',
            name='price_recommended',
            field=models.FloatField(verbose_name='Recomended price base'),
        ),
        migrations.AlterField(
            model_name='saleslineticket',
            name='discount',
            field=models.FloatField(default=0, verbose_name='Discount (%)'),
        ),
        migrations.AlterField(
            model_name='saleslineticket',
            name='price',
            field=models.FloatField(verbose_name='Price base'),
        ),
        migrations.AlterField(
            model_name='saleslineticket',
            name='price_recommended',
            field=models.FloatField(verbose_name='Recomended price base'),
        ),
    ]
