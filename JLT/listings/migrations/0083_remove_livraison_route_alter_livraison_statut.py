# Generated by Django 5.0.3 on 2024-05-16 02:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0082_route_heure_depart_route_livreur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livraison',
            name='route',
        ),
        migrations.AlterField(
            model_name='livraison',
            name='statut',
            field=models.ForeignKey(blank=True, default='todo', null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.route'),
        ),
    ]
