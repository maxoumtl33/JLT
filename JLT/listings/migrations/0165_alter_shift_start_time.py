# Generated by Django 5.0.3 on 2024-11-16 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0164_alter_shift_end_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='start_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
