# Generated by Django 5.0.3 on 2024-05-09 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0073_remove_livraison_details_commande_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livraison',
            name='recuperation',
            field=models.BooleanField(default=False),
        ),
    ]