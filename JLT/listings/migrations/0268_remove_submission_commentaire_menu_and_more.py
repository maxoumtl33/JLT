# Generated by Django 5.1.4 on 2025-06-12 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0267_submission_commentaire_menu'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='commentaire_menu',
        ),
        migrations.AddField(
            model_name='menusubmission',
            name='commentaire_menu',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
