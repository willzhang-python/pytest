# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booktest', '0002_auto_20200305_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='heroinfo',
            name='isDelete',
            field=models.BooleanField(default=False),
        ),
    ]
