# Generated by Django 4.2.3 on 2023-08-28 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_contabilidad', '0028_librocompra_rut_registro'),
    ]

    operations = [
        migrations.AddField(
            model_name='librocompra',
            name='monto_contabilizado',
            field=models.FloatField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='librocompra',
            name='monto_positivo',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
