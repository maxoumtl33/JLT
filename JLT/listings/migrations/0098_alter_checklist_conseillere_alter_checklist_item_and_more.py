# Generated by Django 5.0.3 on 2024-07-08 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0097_checklist_added_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='conseillere',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='item',
            field=models.ManyToManyField(blank=True, to='listings.iteminv'),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='lieu',
            field=models.CharField(blank=True, max_length=10000),
        ),
        migrations.AlterField(
            model_name='checklist',
            name='livraison',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.livraison'),
        ),
    ]