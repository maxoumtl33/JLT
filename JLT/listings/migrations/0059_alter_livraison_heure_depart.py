# Generated by Django 5.0.3 on 2024-04-21 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0058_alter_livraison_heure_depart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='livraison',
            name='heure_depart',
            field=models.CharField(blank=True, choices=[('06h00', '06h00'), ('06h15', '06h15'), ('06h30', '06h30'), ('06h45', '06h45'), ('07h00', '07h00'), ('07h15', '07h15'), ('07h30', '07h30'), ('07h45', '07h45'), ('08h00', '08h00'), ('08h15', '08h15'), ('08h30', '08h30'), ('08h45', '08h45'), ('09h00', '09h00'), ('09h15', '09h15'), ('09h30', '09h30'), ('09h45', '09h45'), ('10h00', '10h00'), ('10h15', '10h15'), ('10h30', '10h30'), ('10h45', '10h45'), ('11h00', '11h00'), ('11h15', '11h15'), ('11h30', '11h30'), ('11h45', '11h45'), ('12h00', '12h00'), ('12h15', '12h15'), ('12h30', '12h30'), ('12h45', '12h45'), ('13h00', '13h00'), ('13h15', '13h15'), ('13h30', '13h30'), ('13h45', '13h45'), ('14h00', '14h00'), ('14h15', '14h15'), ('14h30', '14h30'), ('14h45', '14h45'), ('15h00', '15h00'), ('15h15', '15h15'), ('15h30', '15h30'), ('15h45', '15h45'), ('16h00', '16h00'), ('16h15', '16h15'), ('16h30', '16h30'), ('16h45', '16h45'), ('17h00', '17h00'), ('17h15', '17h15'), ('17h30', '17h30'), ('17h45', '17h45'), ('18h00', '18h00'), ('18h15', '18h15'), ('18h30', '18h30'), ('18h45', '18h45'), ('19h00', '19h00'), ('19h15', '19h15'), ('19h30', '19h30'), ('19h45', '19h45'), ('20h00', '20h00'), ('h', 'h')], max_length=100, null=True),
        ),
    ]