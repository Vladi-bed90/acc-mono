# Generated by Django 4.2.3 on 2023-08-01 17:01

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_banco', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='banco',
            options={'verbose_name': 'banco', 'verbose_name_plural': 'banco'},
        ),
        migrations.CreateModel(
            name='MovimientoBancario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('monto', models.FloatField()),
                ('descripcion', models.CharField(max_length=150)),
                ('cargo_abono', models.CharField(choices=[('C', 'C'), ('A', 'A')], max_length=1)),
                ('detalle_adicional', models.CharField(blank=True, max_length=150)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('banco', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_banco.banco')),
                ('uploaded_by', models.ForeignKey(default=django.contrib.auth.models.User, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'movimiento_bancario',
                'verbose_name_plural': 'movimiento_bancario',
            },
        ),
    ]
