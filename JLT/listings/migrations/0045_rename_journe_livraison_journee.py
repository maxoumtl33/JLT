# Generated by Django 5.0.3 on 2024-04-14 05:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0044_rename_journee_livraison_journe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='livraison',
            old_name='journe',
            new_name='journee',
        ),
    ]
