# Generated by Django 4.2.3 on 2023-08-02 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_empresa', '0001_initial'),
        ('app_banco', '0008_banco_empresa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banco',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_empresa.empresa'),
        ),
    ]
