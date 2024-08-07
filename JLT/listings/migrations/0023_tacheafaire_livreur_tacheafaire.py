# Generated by Django 5.0.3 on 2024-03-25 04:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0022_remove_livreur_tacheafaire'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tacheafaire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='livreur',
            name='tacheafaire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.tacheafaire'),
        ),
    ]
