# Generated by Django 5.0.3 on 2024-04-06 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0039_route_livraison_retourtraiteur_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='livraison',
            name='recuperation',
            field=models.CharField(default='', max_length=3),
            preserve_default=False,
        ),
    ]
