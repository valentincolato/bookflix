# Generated by Django 3.0.6 on 2020-07-08 03:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_libro', '0018_auto_20200707_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='numero_de_capitulos',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
