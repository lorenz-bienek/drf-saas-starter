# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-29 08:31
from __future__ import unicode_literals

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('mails', '0006_auto_20170328_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Should be a small string', max_length=100, verbose_name='Template name')),
                ('subject_template', models.CharField(help_text='A python template string for email subject', max_length=200, verbose_name='Email subject line template')),
                ('html_template', tinymce.models.HTMLField(help_text='Use django template syntax; can edit with tinymce in admin site', verbose_name='HTML template (required)')),
                ('text_template', models.TextField(default='', help_text='If not provided, it is generated dynamically from the HTML template.', verbose_name='Text template (optional)')),
            ],
        ),
    ]
