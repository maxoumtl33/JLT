# Generated by Django 5.0.3 on 2024-09-24 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0137_recupfrigo_filled_at_recupfrigo_filled_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recuplivreuritem',
            name='item_name',
            field=models.CharField(choices=[('plateaux', 'plateaux'), ('bols', 'bols'), ('porcelaine', 'porcelaine'), ('ramequins', 'ramequins'), ('insertion', 'insertion'), ('plateau de bois', 'plateau de bois'), ('paniers', 'paniers'), ('verres', 'verres'), ('thermos', 'thermos'), ('cambro', 'cambro'), ('tempkeep', 'tempkeep'), ('pinces', 'pinces')], max_length=200),
        ),
    ]
