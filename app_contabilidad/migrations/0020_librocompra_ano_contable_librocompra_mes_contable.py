# Generated by Django 4.2.3 on 2023-08-08 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_contabilidad', '0019_librocompra_detalle'),
    ]

    operations = [
        migrations.AddField(
            model_name='librocompra',
            name='ano_contable',
            field=models.SmallIntegerField(default=2023),
        ),
        migrations.AddField(
            model_name='librocompra',
            name='mes_contable',
            field=models.SmallIntegerField(default=1),
        ),
    ]