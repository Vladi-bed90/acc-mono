# Generated by Django 4.2.3 on 2023-08-23 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_contabilidad', '0027_alter_registrocomprobante_comprobante'),
    ]

    operations = [
        migrations.AddField(
            model_name='librocompra',
            name='rut_registro',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]