# Generated by Django 4.2.3 on 2024-04-15 01:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_empresa', '0012_alter_empresa_random_short_uuid'),
        ('app_contabilidad', '0036_clienteproveedor_pais'),
    ]

    operations = [
        migrations.CreateModel(
            name='PeriodoContable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mes', models.SmallIntegerField()),
                ('anio', models.SmallIntegerField()),
                ('es_cerrado', models.BooleanField(default=False)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_empresa.empresa')),
            ],
        ),
    ]