# Generated by Django 5.0.3 on 2024-11-26 00:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0172_alter_checklist_conseillere_conseiller'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklist',
            name='conseillere',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.conseiller'),
        ),
    ]
