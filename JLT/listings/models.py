from django.db import models
from django.contrib.auth.models import User








#class Route(models.Model):
        #nom = models.fields.CharField(max_length=100)
        #def __str__(self):
            #return f'{self.nom}'


class Livreur(models.Model):
        nom = models.fields.CharField(max_length=100)
        def __str__(self):
            return f'{self.nom}'
        user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

class Tacheafaire(models.Model) :
        nom = models.fields.CharField(max_length=100)
        description = models.fields.CharField(max_length=100)
        livreur = models.ForeignKey(Livreur, null=True, on_delete=models.SET_NULL)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done')
    ])


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20, default='pending')

class Client(models.Model):
        nom = models.fields.CharField(null=True, blank=True, max_length=100)
        def __str__(self):
            return f'{self.nom}'
        adresse_lieux = models.fields.CharField(null=True, blank=True, max_length=100)
        adresse_dock = models.fields.CharField(null=True, blank=True, max_length=100)
        contact = models.fields.CharField(null=True, blank=True, max_length=100)

class Message(models.Model):
     nom = models.fields.CharField(max_length=100)
     def __str__(self):
            return f'{self.nom}'
     description = models.fields.CharField(max_length=100)
     livreur = models.ForeignKey(Livreur, null=True, on_delete=models.SET_NULL)
     


class Journee(models.Model):
     nom = models.fields.CharField(max_length=100)
     def __str__(self):
        return f'{self.nom}'
     date = models.DateField()
    


class Route(models.Model):

     choiceheures = (
         ('.', '.'),
         ('06h00', '06h00'),
         ('06h15', '06h15'),
         ('06h30', '06h30'),
         ('06h45', '06h45'),
         ('07h00', '07h00'),
         ('07h15', '07h15'),
         ('07h30', '07h30'),
         ('07h45', '07h45'),
         ('08h00', '08h00'),
         ('08h15', '08h15'),
         ('08h30', '08h30'),
         ('08h45', '08h45'),
         ('09h00', '09h00'),
         ('09h15', '09h15'),
         ('09h30', '09h30'),
         ('09h45', '09h45'),
         ('10h00', '10h00'),
         ('10h15', '10h15'),
         ('10h30', '10h30'),
         ('10h45', '10h45'),
         ('11h00', '11h00'),
         ('11h15', '11h15'),
         ('11h30', '11h30'),
         ('11h45', '11h45'),
         ('12h00', '12h00'),
         ('12h15', '12h15'),
         ('12h30', '12h30'),
         ('12h45', '12h45'),
         ('13h00', '13h00'),
         ('13h15', '13h15'),
         ('13h30', '13h30'),
         ('13h45', '13h45'),
         ('14h00', '14h00'),
         ('14h15', '14h15'),
         ('14h30', '14h30'),
         ('14h45', '14h45'),
         ('15h00', '15h00'),
         ('15h15', '15h15'),
         ('15h30', '15h30'),
         ('15h45', '15h45'),
         ('16h00', '16h00'),
         ('16h15', '16h15'),
         ('16h30', '16h30'),
         ('16h45', '16h45'),
         ('17h00', '17h00'),
         ('17h15', '17h15'),
         ('17h30', '17h30'),
         ('17h45', '17h45'),
         ('18h00', '18h00'),
         ('18h15', '18h15'),
         ('18h30', '18h30'),
         ('18h45', '18h45'),
         ('19h00', '19h00'),
         ('19h15', '19h15'),
         ('19h30', '19h30'),
         ('19h45', '19h45'),
         ('20h00', '20h00'),
     )
     
     nom = models.fields.CharField(max_length=100)
     
     livreur = models.ForeignKey(Livreur, null=True, blank=True, on_delete=models.SET_NULL)
     heure_depart = models.fields.CharField(null=True, blank=True, max_length=100, choices= choiceheures, default=" ")



        
class Livraison(models.Model):
    choices = (
         ('oui', 'oui'),
         ('non', 'non'))
    choicesaide = (
         ('Osnel', 'Osnel'),
         ('Jef', 'Jef'),
         ('Loic', 'Loic'),
         ('Maxime', 'Maxime'),
         ('Mohammad', 'Mohammad'),
         ('Samuel', 'Samuel'),
         ('Anthonny', 'Anthonny'),
         ('Bruno', 'Bruno'),
         ('Dany', 'Dany'),
         ('Rooseph', 'Rooseph'),
         ('Aucun', 'Aucun'),)
    choiceheures = (
         ('.', '.'),
         ('06h00', '06h00'),
         ('06h15', '06h15'),
         ('06h30', '06h30'),
         ('06h45', '06h45'),
         ('07h00', '07h00'),
         ('07h15', '07h15'),
         ('07h30', '07h30'),
         ('07h45', '07h45'),
         ('08h00', '08h00'),
         ('08h15', '08h15'),
         ('08h30', '08h30'),
         ('08h45', '08h45'),
         ('09h00', '09h00'),
         ('09h15', '09h15'),
         ('09h30', '09h30'),
         ('09h45', '09h45'),
         ('10h00', '10h00'),
         ('10h15', '10h15'),
         ('10h30', '10h30'),
         ('10h45', '10h45'),
         ('11h00', '11h00'),
         ('11h15', '11h15'),
         ('11h30', '11h30'),
         ('11h45', '11h45'),
         ('12h00', '12h00'),
         ('12h15', '12h15'),
         ('12h30', '12h30'),
         ('12h45', '12h45'),
         ('13h00', '13h00'),
         ('13h15', '13h15'),
         ('13h30', '13h30'),
         ('13h45', '13h45'),
         ('14h00', '14h00'),
         ('14h15', '14h15'),
         ('14h30', '14h30'),
         ('14h45', '14h45'),
         ('15h00', '15h00'),
         ('15h15', '15h15'),
         ('15h30', '15h30'),
         ('15h45', '15h45'),
         ('16h00', '16h00'),
         ('16h15', '16h15'),
         ('16h30', '16h30'),
         ('16h45', '16h45'),
         ('17h00', '17h00'),
         ('17h15', '17h15'),
         ('17h30', '17h30'),
         ('17h45', '17h45'),
         ('18h00', '18h00'),
         ('18h15', '18h15'),
         ('18h30', '18h30'),
         ('18h45', '18h45'),
         ('19h00', '19h00'),
         ('19h15', '19h15'),
         ('19h30', '19h30'),
         ('19h45', '19h45'),
         ('20h00', '20h00'),
        
         

    )
    statut = models.ForeignKey(Route, null=True, blank=True, on_delete=models.SET_NULL, default=21)
    nom = models.fields.CharField(max_length=100, null=True, blank=True,)
    def __str__(self):
        return f'{self.nom}'
    heure_depart = models.fields.CharField(null=True, blank=True, max_length=100, choices= choiceheures, default=" ")
    heure_livraison = models.fields.CharField(null=True, blank=True, max_length=100, default=" ")
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.fields.DateField(null=True, blank=True)
    commentaire = models.fields.CharField(null=True, blank=True, max_length=500)
    commentairedispatch = models.fields.CharField(null=True, blank=True, max_length=500000, default=" ")
    infodetail = models.fields.CharField(null=True, blank=True, max_length=500000, default=" ")
    livreur = models.ForeignKey(Livreur, null=True, blank=True, on_delete=models.SET_NULL)
    journee = models.ForeignKey(Journee, null=True, blank=True, on_delete=models.SET_NULL, default= 2)
    aidelivreur = models.fields.CharField(null=True, blank=True, max_length=100, choices=choicesaide, default=" ")
    retourtraiteur = models.fields.CharField(null=True, blank=True, max_length = 3, choices=choices, default=" ")
    recuperation = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    adress = models.fields.CharField(null=True, blank=True, max_length=700, default=" ")
    zipcode = models.fields.CharField(null=True, blank=True, max_length=100, default=" ")
    app = models.fields.CharField(null=True, blank=True, max_length=700, default=" ")
    ligne2 = models.fields.CharField(null=True, blank=True, max_length=700, default=" ")
    city = models.fields.CharField(null=True, blank=True, max_length=100, default="Montreal")
    country = models.fields.CharField(null=True, blank=True, max_length=100, default="Canada")
    lat = models.fields.CharField(null=True, blank=True, max_length=200)
    lng = models.fields.CharField(null=True, blank=True, max_length=200)
    place_id = models.fields.CharField(null=True, blank=True, max_length=200)
    convives = models.fields.CharField(null=True, blank=True, max_length=200, default=" ")
    mode_envoi = models.fields.CharField(null=True, blank=True, max_length=200, default=" ")
    num_commande = models.fields.CharField(null=True, blank=True, max_length=200, default=" ")
    nom_client = models.fields.CharField(null=True, blank=True, max_length=200, default=" ")
    contact_site = models.fields.CharField(null=True, blank=True, max_length=200, default=" ")
    vendeur = models.fields.CharField(null=True, blank=True, max_length=200, default=" ")

    position = models.IntegerField(default=0)

    
class Distances(models.Model):
     from_location = models.ForeignKey(Livraison, related_name="from_location", on_delete=models.CASCADE)
     to_location = models.ForeignKey(Livraison, related_name="to", on_delete=models.CASCADE)
     mode = models.fields.CharField(max_length=100, null=True, blank=True)
     distance_km = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
     distance_mins = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
     distance_traffic_mins = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
     created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
     edited_at = models.DateTimeField(auto_now_add=True)

     def __str__(self):
          return self.name




class Recuperation(models.Model):
    nom = models.fields.CharField(max_length=100)
    def __str__(self):
        return f'{self.nom}'
    route = models.ForeignKey(Route, null=True, on_delete=models.SET_NULL)
    heure_depart = models.fields.CharField(max_length=100)
    heure_livraison = models.fields.CharField(max_length=100)
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    date = models.fields.DateField()
    commentaire = models.fields.CharField(max_length=100)
    details_commande = models.FileField(upload_to='commandesdetail/')
    status = models.fields.CharField(max_length=100)
    livreur = models.ForeignKey(Livreur, null=True, on_delete=models.SET_NULL)
    journee = models.ForeignKey(Journee, null=True, on_delete=models.SET_NULL)
    aidelivreur = models.fields.CharField(max_length=100)
    retourtraiteur = models.fields.CharField(max_length = 3)



    




    

        
