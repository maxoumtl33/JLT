# Generated by Django 5.1.4 on 2025-06-02 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0257_remove_menu_delivery_modes'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='delivery_modes',
            field=models.ManyToManyField(blank=True, to='listings.deliverymode'),
        ),
    ]
