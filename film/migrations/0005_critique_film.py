# Generated by Django 5.0.1 on 2024-01-29 09:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0004_critique'),
    ]

    operations = [
        migrations.AddField(
            model_name='critique',
            name='film',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='film.film'),
        ),
    ]