# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 08:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_payments', '0017_auto_20161021_1202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currency',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterModelOptions(
            name='paymentanswer',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterModelOptions(
            name='paymentconfirmation',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterModelOptions(
            name='paymentrequest',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'list')},
        ),
        migrations.AlterField(
            model_name='currency',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='paymentanswer',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='paymentconfirmation',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='paymentrequest',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
    ]
