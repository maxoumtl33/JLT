# Generated by Django 5.1.4 on 2025-07-28 03:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0289_alter_menusubmission_delivery_mode'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('ÉQUIPEMENT DE BASE', 'ÉQUIPEMENT DE BASE'), ('JETABLE', 'JETABLE'), ('ACCESSOIRES DE DÉCOR', 'ACCESSOIRES DE DÉCOR'), ('ÉQUIPEMENT DE BAR', 'ÉQUIPEMENT DE BAR'), ('ÉQUIPEMENT POUR SERVICE CAFÉ', 'ÉQUIPEMENT POUR SERVICE CAFÉ'), ('ITEMS DIVERS', 'ITEMS DIVERS'), ('TABLE ET LINGE DE TABLE', 'TABLE ET LINGE DE TABLE'), ('VERRERIE', 'VERRERIE'), ('PORCELAINE ET COUTELLERIE', 'PORCELAINE ET COUTELLERIE'), ('ÉQUIPEMENT POUR MONTAGE CANAPÉS', 'ÉQUIPEMENT POUR MONTAGE CANAPÉS'), ('ÉQUIPEMENT DE CUISSON', 'ÉQUIPEMENT DE CUISSON'), ('USTENSILES DE SERVICE', 'USTENSILES DE SERVICE'), ('ALCOOL FORT', 'ALCOOL FORT'), ('BIERES', 'BIERES'), ('VINS', 'VINS'), ('SANS ALCOOL', 'SANS ALCOOL'), ('CFCDN', 'CFCDN'), ('SOUMISSIONS', 'SOUMISSIONS')], max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('link', models.URLField(blank=True, null=True)),
                ('is_read', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
