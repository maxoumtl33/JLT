# Generated by Django 5.0.3 on 2024-05-04 21:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0061_livraison_important'),
    ]

    operations = [
        migrations.RenameField(
            model_name='livraison',
            old_name='important',
            new_name='commentairedispatch',
        ),
        migrations.RemoveField(
            model_name='livraison',
            name='checklist',
        ),
        migrations.AlterField(
            model_name='livraison',
            name='recuperation',
            field=models.CharField(blank=True, choices=[('oui', 'oui'), ('non', 'non')], default='non', max_length=3, null=True),
        ),
    ]