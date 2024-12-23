# Generated by Django 4.2.3 on 2023-08-01 17:28

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=20)),
                ('country', models.CharField(choices=[('CHILE', 'Chile'), ('MEXICO', 'Mexico'), ('COLOMBIA', 'Colombia'), ('USA', 'Usa')], default='CHILE', max_length=20)),
                ('currency', models.CharField(choices=[('USD', 'Usd'), ('CLP', 'Clp'), ('COL', 'Col'), ('MXN', 'Mxn')], default='CLP', max_length=3)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('created_by', models.ForeignKey(default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
