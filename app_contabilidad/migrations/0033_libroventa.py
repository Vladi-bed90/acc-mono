# Generated by Django 4.2.3 on 2023-09-12 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_empresa', '0007_remove_empresa_currency'),
        ('app_contabilidad', '0032_registrocomprobante_numero_documento'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibroVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folio', models.IntegerField()),
                ('fecha_documento', models.DateField()),
                ('monto_exento', models.FloatField()),
                ('monto_neto', models.FloatField()),
                ('monto_iva', models.FloatField()),
                ('monto_total', models.FloatField()),
                ('detalle', models.CharField(blank=True, max_length=120, null=True)),
                ('rut_registro', models.CharField(blank=True, max_length=50)),
                ('mes_contable', models.SmallIntegerField()),
                ('ano_contable', models.SmallIntegerField()),
                ('es_cuadrado', models.BooleanField(default=False)),
                ('monto_positivo', models.FloatField(blank=True, default=0)),
                ('es_done', models.BooleanField(default=False)),
                ('monto_contabilizado', models.FloatField(blank=True, default=0)),
                ('es_pagado', models.BooleanField(default=False)),
                ('id_unico_dte', models.CharField(max_length=50, unique=True)),
                ('comprobante', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_contabilidad.comprobante')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_empresa.empresa')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_contabilidad.clienteproveedor')),
                ('tipo_documento', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_contabilidad.tipodocumentotributario')),
            ],
        ),
    ]