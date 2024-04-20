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
     nom = models.fields.CharField(max_length=100)
     def __str__(self):
        return f'{self.nom}'


        
class Livraison(models.Model):
    choices = (
         ('oui', 'oui'),
         ('non', 'non'))
    choicesaide = (
         ('Osnel', 'Osnel'),
         ('Aucun', 'Aucun'))
    nom = models.fields.CharField(max_length=100, null=True, blank=True,)
    def __str__(self):
        return f'{self.nom}'
    route = models.ForeignKey(Route, null=True, blank=True, on_delete=models.SET_NULL)
    heure_depart = models.fields.CharField(null=True, blank=True, max_length=100)
    heure_livraison = models.fields.CharField(null=True, blank=True, max_length=100)
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.fields.DateField(null=True, blank=True,)
    commentaire = models.fields.CharField(null=True, blank=True, max_length=500)
    details_commande = models.FileField(null=True, blank=True, upload_to='media/commandesdetail/')
    infodetail = models.fields.CharField(null=True, blank=True, max_length=500000)
    livreur = models.ForeignKey(Livreur, null=True, blank=True, on_delete=models.SET_NULL)
    journee = models.ForeignKey(Journee, null=True, blank=True, on_delete=models.SET_NULL)
    aidelivreur = models.fields.CharField(null=True, blank=True, max_length=100, choices=choicesaide)
    checklist = models.fields.CharField(null=True, blank=True, max_length =3, choices=choices)
    retourtraiteur = models.fields.CharField(null=True, blank=True, max_length = 3, choices=choices)
    recuperation = models.fields.CharField(null=True, blank=True, max_length = 3, choices=choices)
    status = models.BooleanField(default=False)
    adress = models.fields.CharField(null=True, blank=True, max_length=100)
    zipcode = models.fields.CharField(null=True, blank=True, max_length=100)
    city = models.fields.CharField(null=True, blank=True, max_length=100, default="Montreal")
    country = models.fields.CharField(null=True, blank=True, max_length=100, default="Canada")
    lat = models.fields.CharField(null=True, blank=True, max_length=200)
    lng = models.fields.CharField(null=True, blank=True, max_length=200)
    place_id = models.fields.CharField(null=True, blank=True, max_length=200)
    convives = models.fields.CharField(null=True, blank=True, max_length=200)
    mode_envoi = models.fields.CharField(null=True, blank=True, max_length=200)
    num_commande = models.fields.CharField(null=True, blank=True, max_length=200)
    nom_client = models.fields.CharField(null=True, blank=True, max_length=200)
    contact_site = models.fields.CharField(null=True, blank=True, max_length=200)


    
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



    




    

        
