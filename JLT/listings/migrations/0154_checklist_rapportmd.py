# Generated by Django 5.0.3 on 2024-10-30 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0153_md_phone_md_user_alter_checklist_md'),
    ]

    operations = [
        migrations.AddField(
            model_name='checklist',
            name='rapportmd',
            field=models.TextField(blank=True, null=True),
        ),
    ]
