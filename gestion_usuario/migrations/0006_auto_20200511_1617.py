# Generated by Django 3.0.5 on 2020-05-11 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_usuario', '0005_profile_dob'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='dob',
            new_name='fecha_nacimiento',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='photo',
            new_name='foto_perfil',
        ),
    ]
