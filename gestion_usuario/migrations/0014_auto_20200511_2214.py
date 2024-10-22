# Generated by Django 3.0.6 on 2020-05-12 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_libro', '0002_auto_20200511_2214'),
        ('gestion_usuario', '0013_auto_20200511_1838'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorito',
            name='pagina',
        ),
        migrations.AddField(
            model_name='profile',
            name='soyPrincipal',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='texto',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='historial',
            name='pagina',
            field=models.PositiveIntegerField(),
        ),
        migrations.CreateModel(
            name='Puntaje',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now=True)),
                ('estrellas', models.PositiveIntegerField()),
                ('libro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion_libro.Libro')),
                ('perfil', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gestion_usuario.Profile')),
            ],
        ),
    ]
