# Generated by Django 4.2.3 on 2023-08-10 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_contabilidad', '0026_alter_librocompra_id_unico_dte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrocomprobante',
            name='comprobante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_contabilidad.comprobante'),
        ),
    ]
