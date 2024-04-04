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
        nom = models.fields.CharField(max_length=100)
        def __str__(self):
            return f'{self.nom}'
        adresse_lieux = models.fields.CharField(max_length=100)
        adresse_dock = models.fields.CharField(max_length=100)
        contact = models.fields.CharField(max_length=100)

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





        
class Livraison(models.Model):
    nom = models.fields.CharField(max_length=100)
    def __str__(self):
        return f'{self.nom}'
    route = models.fields.CharField(max_length=100)
    heure_depart = models.fields.CharField(max_length=100)
    heure_livraison = models.fields.CharField(max_length=100)
    client = models.ForeignKey(Client, null=True, on_delete=models.SET_NULL)
    date = models.fields.DateField()
    commentaire = models.fields.CharField(max_length=100)
    details_commande = models.FileField(upload_to='media/commandesdetail/')
    status = models.fields.CharField(max_length=100)
    livreur = models.ForeignKey(Livreur, null=True, on_delete=models.SET_NULL)
    journee = models.ForeignKey(Journee, null=True, on_delete=models.SET_NULL)
    aidelivreur = models.fields.CharField(max_length=100)
    checklist = models.fields.CharField(max_length =3)

class Recuperation(models.Model):
    nom = models.fields.CharField(max_length=100)
    def __str__(self):
        return f'{self.nom}'
    route = models.fields.CharField(max_length=100)
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


    




    

        
