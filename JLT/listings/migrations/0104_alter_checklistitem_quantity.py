# Generated by Django 5.0.3 on 2024-07-11 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0103_alter_checklistitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checklistitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
