# Generated by Django 4.2.3 on 2023-08-01 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_contabilidad', '0002_comprobante_year_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprobante',
            name='day_num',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comprobante',
            name='month_num',
            field=models.SmallIntegerField(default=0),
        ),
    ]