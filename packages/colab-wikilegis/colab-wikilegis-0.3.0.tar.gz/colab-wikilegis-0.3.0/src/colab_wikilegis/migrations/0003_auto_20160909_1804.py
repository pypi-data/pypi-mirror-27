# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('colab_wikilegis', '0002_auto_20160909_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wikilegisbill',
            name='reporting_member',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
