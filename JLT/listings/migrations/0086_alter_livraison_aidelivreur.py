# Generated by Django 5.0.3 on 2024-05-31 00:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0085_livraison_vendeur'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livraison',
            name='aidelivreur',
            field=models.CharField(blank=True, choices=[('Osnel', 'Osnel'), ('Jef', 'Jef'), ('Loic', 'Loic'), ('Maxime', 'Maxime'), ('Mohammad', 'Mohammad'), ('Samuel', 'Samuel'), ('Anthonny', 'Anthonny'), ('Antoine', 'Antoine'), ('Dany', 'Dany'), ('Rooseph', 'Rooseph'), ('Aucun', 'Aucun')], default=' ', max_length=100, null=True),
        ),
    ]
