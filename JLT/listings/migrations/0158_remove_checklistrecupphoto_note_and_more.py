# Generated by Django 5.0.3 on 2024-10-31 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0157_checklistrecupphoto_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='checklistrecupphoto',
            name='note',
        ),
        migrations.AddField(
            model_name='checklist',
            name='rapportrecup',
            field=models.TextField(blank=True, null=True),
        ),
    ]
