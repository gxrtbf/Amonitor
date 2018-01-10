# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-09 02:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dayAddApi', '0010_flowpaidmoney'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlowC2CFund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member', models.CharField(default=b'credan', max_length=128)),
                ('loanCount', models.IntegerField(default=0)),
                ('loanMoney', models.FloatField(default=0.0)),
                ('loanCountTerm', models.IntegerField(default=0)),
                ('loanCountTermNo', models.IntegerField(default=0)),
                ('delayRate0', models.FloatField(default=0.0)),
                ('allCountTerm', models.IntegerField(default=0)),
                ('delayRate7', models.FloatField(default=0.0)),
                ('CountTerm7', models.IntegerField(default=0)),
                ('createDate', models.DateField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ('createDate',),
            },
        ),
    ]
