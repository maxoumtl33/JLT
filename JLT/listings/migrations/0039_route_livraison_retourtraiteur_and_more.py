# Generated by Django 5.0.3 on 2024-04-04 14:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0038_alter_livraison_details_commande'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='livraison',
            name='retourtraiteur',
            field=models.CharField(default='', max_length=3),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recuperation',
            name='retourtraiteur',
            field=models.CharField(default='', max_length=3),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='livraison',
            name='route',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.route'),
        ),
        migrations.AlterField(
            model_name='recuperation',
            name='route',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.route'),
        ),
    ]