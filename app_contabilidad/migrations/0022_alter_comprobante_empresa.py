# Generated by Django 4.2.3 on 2023-08-08 19:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_empresa', '0001_initial'),
        ('app_contabilidad', '0021_alter_librocompra_ano_contable_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprobante',
            name='empresa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app_empresa.empresa'),
        ),
    ]
