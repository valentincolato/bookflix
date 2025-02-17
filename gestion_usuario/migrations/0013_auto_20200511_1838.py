# Generated by Django 3.0.6 on 2020-05-11 21:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestion_usuario', '0012_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='usuario',
            name='tarjeta',
        ),
        migrations.RemoveField(
            model_name='comentario',
            name='usuario',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='foto_perfil',
        ),
        migrations.AddField(
            model_name='comentario',
            name='fecha',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='comentario',
            name='perfil',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_usuario.Profile'),
        ),
        migrations.AddField(
            model_name='favorito',
            name='fecha',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='historial',
            name='fecha',
            field=models.DateField(auto_now=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='favorito',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_usuario.Profile'),
        ),
        migrations.AlterField(
            model_name='historial',
            name='perfil',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_usuario.Profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Perfil',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
