# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-02-19 03:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('efsPortfolioApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MutualFund',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scheme_plan', models.CharField(max_length=50)),
                ('acquired_date', models.DateField(default=django.utils.timezone.now)),
                ('investment_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('current_value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('nominee', models.CharField(max_length=30)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mutualfunds', to='efsPortfolioApp.Customer')),
            ],
        ),
    ]