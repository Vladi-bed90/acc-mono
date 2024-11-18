# Generated by Django 4.2.3 on 2023-09-12 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_upload_files', '0002_uploadcompraschile'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadVentasChile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.FileField(upload_to='upload_file')),
                ('uploaded', models.DateTimeField(auto_now_add=True)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
    ]