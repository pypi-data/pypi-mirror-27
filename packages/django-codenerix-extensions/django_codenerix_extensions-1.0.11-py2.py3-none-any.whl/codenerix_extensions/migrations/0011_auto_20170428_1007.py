# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-28 10:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codenerix_extensions', '0010_auto_20170428_0850'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporateimage',
            name='business_name',
            field=models.CharField(blank=True, max_length=254, null=True, verbose_name='Business name'),
        ),
        migrations.AddField(
            model_name='corporateimage',
            name='nid',
            field=models.CharField(blank=True, max_length=20, verbose_name='NID'),
        ),
    ]
