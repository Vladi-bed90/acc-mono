# Generated by Django 4.2.3 on 2023-08-28 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_contabilidad', '0029_librocompra_monto_contabilizado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='librocompra',
            name='es_done',
            field=models.BooleanField(default=False),
        ),
    ]
