# Generated by Django 5.0.3 on 2024-09-17 03:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0129_tacheafaire_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recupfrigo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('livraison', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livraison_recupfrigo', to='listings.livraison')),
            ],
        ),
        migrations.CreateModel(
            name='RecupfrigoItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(choices=[('plateaux', 'plateaux'), ('bols', 'bols'), ('pinces', 'pinces'), ('ramequins', 'ramequins'), ('verres', 'verres'), ('paniers', 'paniers'), ('thermos', 'thermos'), ('cambro', 'cambro'), ('tempkeep', 'tempkeep')], max_length=200)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('recupfrigo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_frigo', to='listings.recupfrigo')),
            ],
        ),
        migrations.CreateModel(
            name='Recuplivreur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('livraison', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='livraison_recuplivreur', to='listings.livraison')),
            ],
        ),
        migrations.CreateModel(
            name='RecuplivreurItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(choices=[('plateaux', 'plateaux'), ('bols', 'bols'), ('pinces', 'pinces'), ('ramequins', 'ramequins'), ('verres', 'verres'), ('paniers', 'paniers'), ('thermos', 'thermos'), ('cambro', 'cambro'), ('tempkeep', 'tempkeep')], max_length=200)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('recuplivreur', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='items_livreur', to='listings.recuplivreur')),
            ],
        ),
    ]