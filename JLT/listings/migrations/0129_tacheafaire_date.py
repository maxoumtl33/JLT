# Generated by Django 5.0.3 on 2024-09-15 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0128_phototaches'),
    ]

    operations = [
        migrations.AddField(
            model_name='tacheafaire',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
