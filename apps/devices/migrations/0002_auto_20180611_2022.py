# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-11 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='type_e',
            field=models.CharField(blank=True, max_length=75, null=True, verbose_name='Tipo E'),
        ),
        migrations.AddField(
            model_name='device',
            name='type_f',
            field=models.CharField(blank=True, max_length=75, null=True, verbose_name='Tipo F'),
        ),
        migrations.AddField(
            model_name='device',
            name='type_g',
            field=models.CharField(blank=True, max_length=75, null=True, verbose_name='Tipo G'),
        ),
        migrations.AddField(
            model_name='device',
            name='type_h',
            field=models.CharField(blank=True, max_length=75, null=True, verbose_name='Tipo H'),
        ),
        migrations.AlterField(
            model_name='device',
            name='created_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='device',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Atualizado em'),
        ),
    ]
