# Generated by Django 3.0.5 on 2020-05-11 16:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_usuario', '0007_auto_20200511_1618'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='fecha_de_nacimiento',
            new_name='fecha_nacimiento',
        ),
    ]
