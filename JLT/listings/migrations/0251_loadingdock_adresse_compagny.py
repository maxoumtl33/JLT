# Generated by Django 5.1.4 on 2025-05-14 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0250_loadingdock_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='loadingdock',
            name='adresse_compagny',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
