# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booktest', '0004_auto_20200306_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaInfo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('atitle', models.CharField(max_length=20)),
                ('aParent', models.ForeignKey(null=True, blank=True, to='booktest.AreaInfo')),
            ],
        ),
        migrations.AlterField(
            model_name='bookinfo',
            name='bbook',
            field=models.CharField(max_length=20),
        ),
    ]
