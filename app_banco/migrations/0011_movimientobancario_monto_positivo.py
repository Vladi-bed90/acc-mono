# Generated by Django 4.2.3 on 2023-08-07 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_banco', '0010_remove_movimientobancario_negocio'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientobancario',
            name='monto_positivo',
            field=models.FloatField(blank=True, default=1, null=True),
        ),
    ]
