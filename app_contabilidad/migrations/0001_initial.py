# Generated by Django 4.2.3 on 2023-08-01 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comprobante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_comprobante', models.IntegerField()),
                ('fecha', models.DateField()),
                ('tipo', models.CharField(choices=[('I', 'INGRESO'), ('E', 'EGRESO'), ('T', 'TRASPASO')], max_length=20)),
                ('glosa', models.TextField(blank=True)),
                ('suma_debe', models.IntegerField(default=0, editable=False)),
                ('suma_haber', models.IntegerField(default=0, editable=False)),
                ('es_cuadrado', models.BooleanField(default=True)),
                ('es_done', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroComprobante',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]
