# Generated by Django 5.1.4 on 2025-04-28 01:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0224_livraison_loading_dock'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklist',
            name='commentairemd',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='loading_dock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='livraisons', to='listings.loadingdock'),
        ),
    ]
