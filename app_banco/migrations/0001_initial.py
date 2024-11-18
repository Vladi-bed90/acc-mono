# Generated by Django 4.2.3 on 2023-08-01 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(choices=[('CHILE', 'Chile'), ('MEXICO', 'Mexico'), ('COLOMBIA', 'Colombia'), ('USA', 'Usa')], default='CHILE', max_length=20)),
                ('currency', models.CharField(choices=[('USD', 'Usd'), ('CLP', 'Clp'), ('COL', 'Col'), ('MXN', 'Mxn')], default='CLP', max_length=3)),
                ('numero_cuenta', models.CharField(blank=True, max_length=50)),
                ('tipo_cuenta', models.CharField(blank=True, max_length=50)),
            ],
        ),
    ]
