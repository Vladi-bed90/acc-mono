# Generated by Django 4.2.3 on 2023-11-08 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_coa', '0001_initial'),
        ('app_empresa', '0007_remove_empresa_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='afecta_iva',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='empresa',
            name='plan_de_cuentas',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='app_coa.coaname'),
        ),
    ]
