# Generated by Django 5.0.3 on 2024-10-31 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0156_remove_checklist_photosrapport_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklistrecupphoto',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
