# Generated by Django 4.2.3 on 2023-08-23 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_banco', '0023_movimientobancario_rut_chile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mediodepago',
            options={'verbose_name': 'medio de pago', 'verbose_name_plural': 'medio de pago'},
        ),
    ]