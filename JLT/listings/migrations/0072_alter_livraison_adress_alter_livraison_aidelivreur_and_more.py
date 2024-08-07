# Generated by Django 5.0.3 on 2024-05-09 00:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0071_alter_livraison_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livraison',
            name='adress',
            field=models.CharField(blank=True, default=' ', max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='aidelivreur',
            field=models.CharField(blank=True, choices=[('Osnel', 'Osnel'), ('Jef', 'Jef'), ('Loic', 'Loic'), ('Maxime', 'Maxime'), ('Mohammad', 'Mohammad'), ('Samuel', 'Samuel'), ('Anthonny', 'Anthonny'), ('Bruno', 'Bruno'), ('Dany', 'Dany'), ('Rooseph', 'Rooseph'), ('Aucun', 'Aucun')], default=' ', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='commentaire',
            field=models.CharField(blank=True, default=' ', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='commentairedispatch',
            field=models.CharField(blank=True, default=' ', max_length=500000, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='contact_site',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='convives',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='details_commande',
            field=models.FileField(blank=True, default=' ', null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='heure_depart',
            field=models.CharField(blank=True, choices=[('.', '.'), ('06h00', '06h00'), ('06h15', '06h15'), ('06h30', '06h30'), ('06h45', '06h45'), ('07h00', '07h00'), ('07h15', '07h15'), ('07h30', '07h30'), ('07h45', '07h45'), ('08h00', '08h00'), ('08h15', '08h15'), ('08h30', '08h30'), ('08h45', '08h45'), ('09h00', '09h00'), ('09h15', '09h15'), ('09h30', '09h30'), ('09h45', '09h45'), ('10h00', '10h00'), ('10h15', '10h15'), ('10h30', '10h30'), ('10h45', '10h45'), ('11h00', '11h00'), ('11h15', '11h15'), ('11h30', '11h30'), ('11h45', '11h45'), ('12h00', '12h00'), ('12h15', '12h15'), ('12h30', '12h30'), ('12h45', '12h45'), ('13h00', '13h00'), ('13h15', '13h15'), ('13h30', '13h30'), ('13h45', '13h45'), ('14h00', '14h00'), ('14h15', '14h15'), ('14h30', '14h30'), ('14h45', '14h45'), ('15h00', '15h00'), ('15h15', '15h15'), ('15h30', '15h30'), ('15h45', '15h45'), ('16h00', '16h00'), ('16h15', '16h15'), ('16h30', '16h30'), ('16h45', '16h45'), ('17h00', '17h00'), ('17h15', '17h15'), ('17h30', '17h30'), ('17h45', '17h45'), ('18h00', '18h00'), ('18h15', '18h15'), ('18h30', '18h30'), ('18h45', '18h45'), ('19h00', '19h00'), ('19h15', '19h15'), ('19h30', '19h30'), ('19h45', '19h45'), ('20h00', '20h00')], default=' ', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='heure_livraison',
            field=models.CharField(blank=True, default=' ', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='infodetail',
            field=models.CharField(blank=True, default=' ', max_length=500000, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='lat',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='livreur',
            field=models.ForeignKey(blank=True, default=' ', null=True, on_delete=django.db.models.deletion.SET_NULL, to='listings.livreur'),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='lng',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='mode_envoi',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='nom_client',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='num_commande',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='place_id',
            field=models.CharField(blank=True, default=' ', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='retourtraiteur',
            field=models.CharField(blank=True, choices=[('oui', 'oui'), ('non', 'non')], default=' ', max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='livraison',
            name='zipcode',
            field=models.CharField(blank=True, default=' ', max_length=100, null=True),
        ),
    ]
