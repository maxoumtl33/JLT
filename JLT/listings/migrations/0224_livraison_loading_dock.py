# Generated by Django 5.1.4 on 2025-04-23 02:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0223_photovehicle_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='livraison',
            name='loading_dock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='livraisons', to='listings.loadingdock'),
        ),
    ]
