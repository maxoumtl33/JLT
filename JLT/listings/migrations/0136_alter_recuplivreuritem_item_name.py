# Generated by Django 5.0.3 on 2024-09-17 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0135_alter_recuplivreuritem_item_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recuplivreuritem',
            name='item_name',
            field=models.CharField(choices=[('plateaux', 'plateaux'), ('bols', 'bols'), ('porcelaine', 'porcelaine'), ('ramequins', 'ramequins'), ('verres', 'verres'), ('insertion', 'insertion'), ('plateau de bois', 'plateau de bois'), ('paniers', 'paniers'), ('thermos', 'thermos'), ('cambro', 'cambro'), ('tempkeep', 'tempkeep'), ('pinces', 'pinces')], max_length=200),
        ),
    ]
