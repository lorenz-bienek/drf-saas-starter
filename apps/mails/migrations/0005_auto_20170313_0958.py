# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 09:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0004_auto_20170313_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='subject',
            field=models.CharField(blank=True, help_text='Subject line for a mail', max_length=500, null=True, verbose_name='Email Subject line'),
        ),
    ]
