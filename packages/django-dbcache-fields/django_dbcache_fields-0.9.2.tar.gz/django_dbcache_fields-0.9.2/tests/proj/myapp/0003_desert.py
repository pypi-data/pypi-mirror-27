# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20171101_1733'),
    ]

    operations = [
        migrations.CreateModel(
            name='Desert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('base_price', models.DecimalField(null=True, max_digits=5, decimal_places=2)),
                ('_get_price_cached', models.TextField(null=True, blank=True)),
            ],
        ),
    ]
