# Generated by Django 5.0.3 on 2024-03-26 22:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0031_remove_livreur_livraison_remove_livreur_tacheafaire_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livreur',
            name='livraison',
        ),
        migrations.RemoveField(
            model_name='livreur',
            name='recuperation',
        ),
        migrations.RemoveField(
            model_name='livreur',
            name='tacheafaire',
        ),
        migrations.AddField(
            model_name='livraison',
            name='livreur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.livreur'),
        ),
        migrations.AddField(
            model_name='recuperation',
            name='livreur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.livreur'),
        ),
        migrations.AddField(
            model_name='tacheafaire',
            name='livreur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.livreur'),
        ),
    ]
