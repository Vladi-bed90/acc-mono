# Generated by Django 4.2.3 on 2023-08-28 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_contabilidad', '0030_librocompra_es_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='librocompra',
            name='es_pagado',
            field=models.BooleanField(default=False),
        ),
    ]
