# Generated by Django 5.1.4 on 2025-07-23 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0284_alter_journee_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='billing_postcode',
            field=models.TextField(blank=True, null=True),
        ),
    ]
