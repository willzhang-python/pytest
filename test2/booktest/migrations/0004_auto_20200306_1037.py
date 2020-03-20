# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booktest', '0003_heroinfo_isdelete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookinfo',
            name='bbook',
            field=models.CharField(max_length=20, db_column='title'),
        ),
        migrations.AlterField(
            model_name='heroinfo',
            name='hcomment',
            field=models.CharField(null=True, blank=True, max_length=200),
        ),
    ]
