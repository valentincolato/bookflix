# Generated by Django 3.0.6 on 2020-06-16 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_libro', '0008_libro_ocultar'),
        ('gestion_noticia', '0006_auto_20200616_1819'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Trailers',
            new_name='Trailer',
        ),
    ]
