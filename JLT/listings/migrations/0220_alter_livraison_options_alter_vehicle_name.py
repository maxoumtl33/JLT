# Generated by Django 5.1.4 on 2025-04-04 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0219_alter_livraison_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='livraison',
            options={},
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='name',
            field=models.CharField(choices=[('KingKong', 'KingKong'), ('Yeti', 'Yeti'), ('Pro Noir', 'Pro Noir'), ('Pro Gris', 'Pro Gris'), ('Transit Noir', 'Transit Noir'), ('Petit Blanc', 'Petit Blanc'), ('Econoline', 'Econoline'), ('Caravane', 'Caravane')], max_length=100),
        ),
    ]
