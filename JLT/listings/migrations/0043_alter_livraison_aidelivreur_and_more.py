# Generated by Django 5.0.3 on 2024-04-14 00:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0042_livraison_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livraison',
            name='aidelivreur',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='checklist',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='commentaire',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='details_commande',
            field=models.FileField(blank=True, null=True, upload_to='media/commandesdetail/'),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='heure_depart',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='heure_livraison',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='infodetail',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='journee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.journee'),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='livreur',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.livreur'),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='recuperation',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='retourtraiteur',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='route',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.route'),
        ),
    ]