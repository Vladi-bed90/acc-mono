# Generated by Django 4.2.3 on 2023-10-26 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_contabilidad', '0034_alter_registrocomprobante_cuenta_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='librocompra',
            name='es_anulado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='libroventa',
            name='es_anulado',
            field=models.BooleanField(default=False),
        ),
    ]
