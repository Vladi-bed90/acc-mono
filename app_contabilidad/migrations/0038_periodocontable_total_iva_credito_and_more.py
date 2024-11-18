# Generated by Django 4.2.3 on 2024-11-18 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_contabilidad', '0037_periodocontable'),
    ]

    operations = [
        migrations.AddField(
            model_name='periodocontable',
            name='total_iva_credito',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='periodocontable',
            name='total_iva_debito',
            field=models.FloatField(default=0),
        ),
    ]