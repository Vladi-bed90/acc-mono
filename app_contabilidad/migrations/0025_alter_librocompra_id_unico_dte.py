# Generated by Django 4.2.3 on 2023-08-08 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_contabilidad', '0024_librocompra_id_unico_dte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librocompra',
            name='id_unico_dte',
            field=models.CharField(default='d', max_length=50, unique=True),
        ),
    ]
