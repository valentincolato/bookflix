# Generated by Django 3.0.6 on 2020-07-10 19:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_libro', '0021_auto_20200710_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='capitulo',
            name='numero_de_capitulo',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
