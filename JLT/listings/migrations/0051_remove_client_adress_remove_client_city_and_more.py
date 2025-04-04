# Generated by Django 5.0.3 on 2024-04-14 23:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0050_rename_adresse_livraison_adress_livraison_city_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='adress',
        ),
        migrations.RemoveField(
            model_name='client',
            name='city',
        ),
        migrations.RemoveField(
            model_name='client',
            name='country',
        ),
        migrations.RemoveField(
            model_name='client',
            name='zipcode',
        ),
        migrations.AlterField(
            model_name='distances',
            name='from_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_location', to='listings.livraison'),
        ),
        migrations.AlterField(
            model_name='distances',
            name='to_location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to', to='listings.livraison'),
        ),
    ]
