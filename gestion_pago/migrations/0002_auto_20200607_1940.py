# Generated by Django 3.0.6 on 2020-06-07 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gestion_pago', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tarjeta',
            name='tipo_suscripcion',
            field=models.CharField(default='regular', max_length=50),
        ),
        migrations.AddField(
            model_name='tarjeta',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
