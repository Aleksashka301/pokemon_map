# Generated by Django 5.1.6 on 2025-03-15 12:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0006_pokemon_previous_evolution'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='previous_evolution',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_evolutions', to='pokemon_entities.pokemon'),
        ),
    ]
