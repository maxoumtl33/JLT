from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import date
from datetime import timedelta
from decimal import Decimal


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    force_password_change = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile  # Import your UserProfile model

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class ItemInv(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='listings/media/commandesdetail', blank=True, null=True)
    quantity = models.IntegerField(default=0)


    def __str__(self):
        return self.name


class Livreur(models.Model):
        nom = models.fields.CharField(max_length=100)
        def __str__(self):
            return f'{self.nom}'
        user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
        latitude = models.FloatField(null=True)
        longitude = models.FloatField(null=True)
        phone = models.fields.CharField(max_length=100)




class Tacheafaire(models.Model) :
        nom = models.fields.CharField(max_length=100)
        description = models.fields.CharField(max_length=100)
        livreur = models.ForeignKey(Livreur, null=True, on_delete=models.SET_NULL)
        status = models.BooleanField(default=False)
        photo = models.ImageField(upload_to='listings/media/commandesdetail', blank=True, null=True)
        date = models.fields.DateField(null=True, blank=True)
        commentaire = models.fields.CharField(null=True, blank=True, max_length=500)




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



class Message(models.Model):
     nom = models.fields.CharField(max_length=100)
     def __str__(self):
            return f'{self.nom}'
     description = models.fields.CharField(max_length=100)
     livreur = models.ForeignKey(Livreur, null=True, on_delete=models.SET_NULL)

class LoadingDock(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=255)
    adresse_compagny = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='listings/media/commandesdetail', blank=True, null=True)
    description = models.TextField(blank=True)
    link = models.URLField(max_length=350, blank=True, null=True)
    place_id = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return f'{self.name}'

class Journee(models.Model):
     nom = models.fields.CharField(max_length=100)
     date = models.DateField(unique=True)
     def __str__(self):
        return f'{self.nom}'
     



from django.db import models
from django.utils import timezone

# Assuming 'Livreur' is defined elsewhere
class Vehicle(models.Model):
    choicename = (
        ('KingKong', 'KingKong'),
        ('Yeti', 'Yeti'),
        ('Pro Noir', 'Pro Noir'),
        ('Pro Gris', 'Pro Gris'),
        ('Transit Noir', 'Transit Noir'),
        ('Petit Blanc', 'Petit Blanc'),
        ('Econoline', 'Econoline'),
        ('Caravane', 'Caravane'),
    )
    name = models.CharField(max_length=100, choices= choicename)
    photos = models.ImageField(upload_to='listings/media/commandesdetail', blank=True, null=True)
    routes = models.ManyToManyField('Route', related_name='vehicles_list', blank=True)
    commentaire = models.fields.CharField(null=True, blank=True, max_length=500)

    def __str__(self):
        return self.name

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
    livreur = models.ManyToManyField('Livreur', blank=True, related_name='routes')
    heure_depart = models.fields.CharField(null=True, blank=True, max_length=100, choices= choiceheures, default=" ")
    date = models.DateField(default=date.today)
    vehicles = models.ManyToManyField(Vehicle, related_name='routes_vehicules', blank=True)
    commentaire = models.fields.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.nom}'

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

class Shift(models.Model):
    livreur = models.ForeignKey(Livreur, on_delete=models.CASCADE)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    date = models.DateField(default=date.today)


    def __str__(self):
        return f"{self.livreur.nom} Shift from {self.start_time} to {self.end_time}"




class PhotoVehicle(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, related_name='vehicle_photos')
    image = models.ImageField(upload_to='listings/media/commandesdetail')
    video = models.FileField(upload_to='listings/media/videos', blank=True, null=True)
    caption = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'Photo for {self.vehicle.name} - {self.caption or "No Caption"}'




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
         ('Mohamed', 'Mohamed'),
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
    statut = models.ForeignKey(Route, null=True, blank=True,related_name='livraisons', on_delete=models.SET_NULL, default=21)
    nom = models.fields.CharField(max_length=100, null=True, blank=True,)
    heure_depart = models.fields.CharField(null=True, blank=True, max_length=100, choices= choiceheures, default=" ")
    heure_livraison = models.fields.CharField(null=True, blank=True, max_length=100, default=".")
    heure_livraison_classement = models.fields.CharField(null=True, blank=True, max_length=100, default=".")
    date = models.fields.DateField(null=True, blank=True)
    period = models.CharField(max_length=20, choices=[("matin", "Matin"), ("midi", "Midi"), ("apres_midi", "Après-midi")], null=True, blank=True)
    loading_docks = models.ManyToManyField(LoadingDock, blank=True, related_name='livraisons_dock')
    date_livraison = models.fields.DateField(null=True, blank=True)
    commentaire = models.fields.CharField(null=True, blank=True, max_length=500)
    commentairedispatch = models.fields.CharField(null=True, blank=True, max_length=350)
    infodetail = models.fields.CharField(null=True, blank=True, max_length=350)
    livreur = models.ManyToManyField('Livreur', blank=True, related_name='livraisons')
    journee = models.ForeignKey(Journee, null=True, blank=True, on_delete=models.SET_NULL)
    aidelivreur = models.fields.CharField(null=True, blank=True, max_length=100, choices=choicesaide, default=" ")
    retourtraiteur = models.fields.CharField(null=True, blank=True, max_length = 3, choices=choices, default="non")
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
    nom_client_signature = models.CharField(max_length=255, null=True, blank=True)
    date_signature = models.DateField(null=True, blank=True)
    signature = models.TextField(blank=True, null=True)  # Stores Base64 string
    photo = models.ImageField(upload_to='listings/media/commandesdetail', blank=True, null=True)
    photo_recup = models.ImageField(upload_to='listings/media/commandesdetail', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Avant de sauver, faire l’association si c’est une nouvelle instance ou si besoin
        super().save(*args, **kwargs)  # Sauvegarde la livraison pour avoir un ID

        # Si l’association n’est pas encore faite, ou si tu veux la mettre à jour à chaque sauvegarde :
        if self.nom:
            docks = LoadingDock.objects.filter(name__icontains=self.nom)
            if docks.exists():
                self.loading_docks.set(docks)

    def __str__(self):
        return f'{self.nom}'
    





class Photo(models.Model):
    livraison = models.ForeignKey('Livraison', on_delete=models.CASCADE, related_name='livraison_photos')
    image = models.ImageField(upload_to='listings/media/commandesdetail')
    caption = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'Photo for {self.livraison.nom} - {self.caption or "No Caption"}'

class PhotoRecup(models.Model):
    livraison = models.ForeignKey('Livraison', on_delete=models.CASCADE, related_name='livraison_photos_recups')
    image = models.ImageField(upload_to='listings/media/commandesdetail')
    caption = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'Photo for {self.livraison.nom} - {self.caption or "No Caption"}'

class Phototaches(models.Model):
    tache = models.ForeignKey('Tacheafaire', on_delete=models.CASCADE, related_name='tache_photos')
    image = models.ImageField(upload_to='listings/media/commandesdetail')
    caption = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'Photo for {self.tache.nom} - {self.caption or "No Caption"}'


class Category(models.Model):
    choices = (
        ('ÉQUIPEMENT DE BASE', 'ÉQUIPEMENT DE BASE'),
        ('JETABLE', 'JETABLE'),
        ('ACCESSOIRES DE DÉCOR', 'ACCESSOIRES DE DÉCOR'),
        ('ÉQUIPEMENT DE BAR', 'ÉQUIPEMENT DE BAR'),
        ('ÉQUIPEMENT POUR SERVICE CAFÉ','ÉQUIPEMENT POUR SERVICE CAFÉ'),
        ('ITEMS DIVERS', 'ITEMS DIVERS'),
        ('TABLE ET LINGE DE TABLE','TABLE ET LINGE DE TABLE'),
        ('VERRERIE','VERRERIE'),
        ('PORCELAINE ET COUTELLERIE','PORCELAINE ET COUTELLERIE'),
        ('ÉQUIPEMENT POUR MONTAGE CANAPÉS','ÉQUIPEMENT POUR MONTAGE CANAPÉS'),
        ('ÉQUIPEMENT DE CUISSON','ÉQUIPEMENT DE CUISSON'),
        ('USTENSILES DE SERVICE','USTENSILES DE SERVICE'),
        ('ALCOOL FORT','ALCOOL FORT'),
        ('BIERES','BIERES'),
        ('VINS','VINS'),
        ('SANS ALCOOL','SANS ALCOOL'),
        ('CFCDN', 'CFCDN'),
        ('SOUMISSIONS', 'SOUMISSIONS'),
    )
    name = models.CharField(max_length=100, choices=choices, unique=True)

    def __str__(self):
        return self.name
        
class Product(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Changed to DecimalField
    category = models.ManyToManyField(Category)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def adjust_quantity(self, quantity_change):
        self.quantity += Decimal(quantity_change)  # Ensure quantity_change is a Decimal
        self.save()

    def __str__(self):
        return self.name

class ProductLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='logs')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Product: {self.product.name}, Created by: {self.created_by.username if self.created_by else 'Unknown'} at {self.created_at}"

class Md(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name
    
class Conseiller(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

from datetime import timedelta
from django.utils.timezone import now

def four_hours_ago():
    return now() - timedelta(hours=5)

class Checklist(models.Model):
    STATUS_CHOICES = [
        
        ('en_cours', 'En cours'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        
    ]

    STATUS_RO_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('modifié', 'Modifié'),
        ('verifié', 'Verifié')

    ]

    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='ChecklistItem')
    livraison = models.ForeignKey(Livraison, null=True, on_delete=models.SET_NULL, blank=True)
    date = models.fields.DateField(null=True, blank=True)
    lieu = models.CharField(max_length=10000, blank=True)
    num_contrat = models.fields.CharField(null=True, blank=True, max_length=200, default=" ")
    nb_convive = models.fields.CharField(null=True, blank=True, max_length=200, default=" ")
    heure_livraison = models.fields.CharField(null=True, blank=True, max_length=100, default=" ")
    md = models.ForeignKey(Md, null=True, on_delete=models.SET_NULL, blank=True)
    added_on = models.DateTimeField(default=four_hours_ago)    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours')
    statusro = models.CharField(max_length=20, choices=STATUS_RO_CHOICES, default='nouveau')
    previous_statusro = models.CharField(max_length=100, null=True)
    rapportmd = models.TextField(blank=True, null=True)
    rapportrecup = models.TextField(blank=True, null=True)
    commentairevente = models.TextField(blank=True, null=True)
    commentairemd = models.TextField(blank=True, null=True)
    type_service = models.TextField(blank=True, null=True)
    occasion = models.TextField(blank=True, null=True)
    depart_traiteur = models.TextField(blank=True, null=True)
    heure_arrive = models.TextField(blank=True, null=True)
    heure_convives = models.TextField(blank=True, null=True)
    debut_cocktail = models.TextField(blank=True, null=True)
    debut_repas = models.TextField(blank=True, null=True)
    fin_evenement = models.TextField(blank=True, null=True)
    commodite = models.TextField(blank=True, null=True)
    fourni_client = models.TextField(blank=True, null=True)
    fourni_salle = models.TextField(blank=True, null=True)
    notechecklist = models.TextField(blank=True, null=True)
    conseillere = models.ForeignKey(Conseiller, on_delete=models.CASCADE, related_name='checklists', null=True, blank=True)
    is_active = models.BooleanField(default=True)  # New field
    created = models.BooleanField(default=False)
    modified = models.BooleanField(default=False)

    def update_status(self):
        # Exclude ChecklistItems where quantity is 0
        non_zero_items = self.checklistitem_set.exclude(quantity=0)
        
        valid_items = non_zero_items.filter(status__in=['valide', 'complete'])
        refused_items = non_zero_items.filter(status__in=['refuse', 'denied', 'deniedprevious'])

        # If all non-zero quantity items are 'valide' or 'complete', set checklist status to 'valide'
        if valid_items.count() == non_zero_items.count() and non_zero_items.exists():
            self.status = 'valide'
        # If any non-zero quantity item is 'refuse' or similar, set checklist status to 'refuse'
        elif refused_items.exists():
            self.status = 'refuse'
        else:
            self.status = 'en_cours'  # Default status if neither fully valid nor refused

        self.save()


    def save(self, *args, **kwargs):
        # If the instance already exists in the database, retrieve its current state
        if self.pk is not None:
            original = Checklist.objects.get(pk=self.pk)
            self.previous_statusro = original.statusro

        # Prepend 'CMD-' to num_contrat if not already present
        if self.num_contrat and not self.num_contrat.startswith('CMD-'):
            self.num_contrat = 'CMD-' + self.num_contrat

        # For new checklists, set statusro to 'nouveau'
        if self.pk is None:
            self.statusro = 'nouveau'

        # Check the condition and set statusro accordingly
        if self.statusro == 'modifié' and self.previous_statusro == 'nouveau':
            self.statusro = 'nouveau'
        

        super(Checklist, self).save(*args, **kwargs)

    def __str__(self):
        return self.name





    


class QuantityProductChangeLog(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    previous_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Change for {self.product.name} by {self.user.username} on {self.timestamp}"

    





class ChecklistMDPhoto(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listings/media/commandesdetail')
    video = models.FileField(upload_to='listings/media/commandesdetail', blank=True, null=True)
    caption = models.CharField(max_length=200, null=True, blank=True)

class ChecklistRecupPhoto(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='listings/media/commandesdetail')
    video = models.FileField(upload_to='listings/media/commandesdetail', blank=True, null=True)

    caption = models.CharField(max_length=200, null=True, blank=True)

class DeliveryMode(models.Model):    
    name = models.CharField(max_length=30, null=True, blank=True)  # Mode d'envoi

    def __str__(self):
        return self.name

class Plat(models.Model):
    nom = models.CharField(max_length=160)
    nom_english = models.CharField(max_length=160, null=True, blank=True)
    def __str__(self):
        return self.nom
    
    
class Menu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    allergie = models.TextField(blank=True, null=True)
    delivery_modes = models.ManyToManyField(DeliveryMode, blank=True)

    def __str__(self):
        return self.name
    


    

class PaymentMode(models.Model):

    SUBMISSION_TYPE_CHOICES = [
        ('Carte de crédit', 'Carte de crédit'),
        ('Chèque', 'Chèque'),
        ('Transfert bancaire', 'Transfert bancaire'),
        ('Facturation', 'Facturation'),
    ]
    name = models.CharField(max_length=50, choices=SUBMISSION_TYPE_CHOICES)
    code = models.CharField(max_length=20, unique=True)  # Identifier unique, par ex. 'cc'
    details = models.TextField(blank=True, null=True)  # Informations complémentaires

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Notification(models.Model):
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    message = models.TextField()
    link = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.recipient.username}'

    def get_absolute_url(self):
        return reverse('submission_detail', args=[self.link.split('/')[-2]])


class Client(models.Model):
    company_name = models.CharField(max_length=100, null=True, blank=True)  # Company name
    contact_person = models.CharField(max_length=100, null=True, blank=True)  # Contact sur place
    ordered_by = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)  # Telephone
    email = models.EmailField(max_length=100, null=True, blank=True)  # Email
    billing_address = models.CharField(max_length=200, null=True, blank=True)  # Adresse facturation
    etage = models.CharField(max_length=200, null=True, blank=True)
    event_location = models.CharField(max_length=200, null=True, blank=True)
    dock_livraison = models.CharField(max_length=200, null=True, blank=True)
    escalier = models.BooleanField(default=False)
    ascenseur = models.BooleanField(default=False)
    carte_dock = models.BooleanField(default=False)
    payment_mode = models.ForeignKey(PaymentMode, on_delete=models.SET_NULL, null=True, blank=True)

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse

TYPE_PRISE_DE_COMMANDE_CHOICES = [
    ('Téléphone', 'Téléphone'),
    ('En ligne', 'En ligne'),
    ('Courriel', 'Courriel'),
]

class Submission(models.Model):
    SUBMISSION_TYPE_CHOICES = [
        ('Soumission événement', 'Soumission_événement'),
        ('Commande événement', 'Commande_événement'),
        ('Soumission BAL/Buffet', 'Soumission_BAL_Buffet'),
        ('Commande BAL/Buffet', 'Commande_BAL_Buffet'),
    ]

    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('envoyé', 'Envoyé'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_type = models.CharField(max_length=24, choices=SUBMISSION_TYPE_CHOICES)
    
    # New fields
    type_prise_de_commande = models.CharField(
        max_length=10,
        choices=TYPE_PRISE_DE_COMMANDE_CHOICES,
        null=True,
        blank=True
    )
    refusal_comment = models.TextField(null=True, blank=True)
    commentaire_boissons = models.TextField(blank=True, null=True)
    commentaire_items = models.TextField(null=True, blank=True)
    document = models.FileField(upload_to='listings/media/commandesdetail', null=True, blank=True)
    event_postcode = models.TextField(null=True, blank=True)
    billing_postcode = models.TextField(null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)  # Company name
    event_location = models.CharField(max_length=200, null=True, blank=True)  # Lieu événement
    contact_person = models.CharField(max_length=100, null=True, blank=True)  # Contact sur place
    ordered_by = models.CharField(max_length=100, null=True, blank=True)  # Commandé par
    phone = models.CharField(max_length=15, null=True, blank=True)  # Telephone
    email = models.EmailField(max_length=100, null=True, blank=True)  # Email
    billing_address = models.CharField(max_length=200, null=True, blank=True)  # Adresse facturation
    etage = models.CharField(max_length=200, null=True, blank=True)
    dock_livraison = models.CharField(max_length=200, null=True, blank=True)
    escalier = models.BooleanField(default=False)
    ascenseur = models.BooleanField(default=False)
    carte_dock = models.BooleanField(default=False)
    note = models.TextField(blank=True, null=True)
    avec_service = models.BooleanField(default=False)
    avec_service_md = models.BooleanField(default=False)
    avec_alcool = models.BooleanField(default=False)
    language = models.TextField(null=True, blank=True)
    location_materiel = models.BooleanField(default=False)
    commentaire = models.CharField(max_length=2000, null=True, blank=True) 
    payment_mode = models.CharField(max_length=200, null=True, blank=True) 
    client = models.ForeignKey('Client', null=True, blank=True, on_delete=models.SET_NULL, related_name='submissions_client')
    date = models.DateField(null=True, blank=True)  # Date événement
    event_time = models.TimeField(null=True, blank=True)  # Heure événement
    guest_count = models.IntegerField(null=True, blank=True)  # Nombre personne
    delivery_time = models.TimeField(null=True, blank=True)  # Heure livraison
    budget = models.IntegerField(null=True, blank=True)  # Budget
    service_count = models.CharField(max_length=100, null=True, blank=True)  # Nombre de service (as string)
    sub_menus = models.ManyToManyField('Menu', blank=True)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # NOUVEAUX CHAMPS AJOUTÉS
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Date d'envoi")
    status_history = models.JSONField(default=list, blank=True, verbose_name="Historique des statuts")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours')

    def save(self, *args, **kwargs):
        # NOUVELLE LOGIQUE : Logger automatiquement quand le statut passe à "envoyé"
        if self.pk:  # Si l'objet existe déjà (mise à jour)
            try:
                old_instance = Submission.objects.get(pk=self.pk)
                old_status = old_instance.status
                
                # Si le statut change vers "envoyé" et sent_at n'est pas défini
                if old_status != 'envoyé' and self.status == 'envoyé' and not self.sent_at:
                    self.sent_at = timezone.now()
                    
                    # Ajouter à l'historique des statuts
                    if not self.status_history:
                        self.status_history = []
                    self.status_history.append({
                        'status': 'envoyé',
                        'date': timezone.now().isoformat(),
                        'user': self.user.username if self.user else None,
                        'old_status': old_status
                    })
                    
            except Submission.DoesNotExist:
                pass
        
       
        
        # Logique existante pour le client
        if not self.client:
            # Préparer les données du client à partir des champs de la soumission
            client_data = {
                'company_name': self.company_name,
                'contact_person': self.contact_person,
                'ordered_by': self.ordered_by,
                'phone': self.phone,
                'email': self.email,
                'billing_address': self.billing_address,
                'etage': self.etage,
                'event_location': self.event_location,
                'dock_livraison': self.dock_livraison,
                'escalier': self.escalier,
                'ascenseur': self.ascenseur,
                'carte_dock': self.carte_dock,
            }

            # Vérifier si au moins un champ utile est rempli
            if any(client_data[field] for field in ['company_name', 'contact_person', 'email', 'phone', 'billing_address']):
                # Essayer de récupérer un client existant avec les mêmes données
                from .models import Client  # Import local pour éviter les imports circulaires
                client_qs = Client.objects.filter(
                    company_name=client_data['company_name'],
                    contact_person=client_data['contact_person'],
                    email=client_data['email'],
                    phone=client_data['phone']
                )
                if client_qs.exists():
                    self.client = client_qs.first()
                else:
                    # Créer un nouveau client si au moins un champ est rempli
                    new_client = Client(**client_data)
                    new_client.save()
                    self.client = new_client
            else:
                # Aucun champ utile rempli, ne pas créer de client
                self.client = None

        # Convertir None en chaîne vide pour certains champs de texte
        text_fields = [
            'company_name', 'refusal_comment', 'commentaire_items', 'commentaire_boissons',
            'event_postcode', 'event_location', 'contact_person', 'ordered_by', 'phone',
            'email', 'billing_address', 'etage', 'dock_livraison', 'commentaire', 'service_count', 
            'payment_mode', 'billing_postcode'
        ]
        for field in text_fields:
            value = getattr(self, field)
            if value is None:
                setattr(self, field, '')

        # Si pas de created_at, définir l'heure
        if not self.created_at:
            self.created_at = timezone.now() - timedelta(hours=4)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Assurez que 'submission_detail' correspond à votre nom d'URL
        return reverse('submission_detail', args=[self.id])
    
    def __str__(self):
        return f"{self.submission_type} by {self.user} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}. Company: {self.company_name if self.company_name else 'N/A'}"

from django.db import models

class MenuSubmission(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='menu_submissions')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    allergies = models.TextField(null=True, blank=True)  # Field to save allergies
    service_count = models.CharField(max_length=100, null=True, blank=True)  # Nombre de service (as string)
    delivery_mode = models.ForeignKey(DeliveryMode, on_delete=models.SET_NULL, null=True, blank=True, default ="Valeur non définie")  # Link to DeliveryMode
    commentaire_menu = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Menu '{self.menu.name}' for {self.submission.company_name} (ID {self.id})"

    
class ChecklistDocument(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='listings/media/commandesdetail')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.checklist.name}"



class Score1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.score}"

from django.core.exceptions import ValidationError
from django.db import models

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.utils import timezone

class ChecklistItem(models.Model):
    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('pending', 'pending'),
        ('complete', 'complete')
    ]

    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True)
    is_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours')
    consumed_quantity = models.PositiveIntegerField(default=0)
    unconsumed_quantity = models.PositiveIntegerField(default=0)
    commentaire = models.CharField(max_length=100, null=True, blank=True)
    com = models.CharField(max_length=100, null=True, blank=True)
    previous_quantity = models.PositiveIntegerField(default=0)
    previous_status = models.CharField(max_length=100, null=True, blank=True)
    is_stock_updated = models.BooleanField(default=False)

    class Meta:
        unique_together = ('checklist', 'product')

    def save(self, *args, **kwargs):
        if self.commentaire:
            self.commentaire = self.commentaire.lower()

        if self.pk:  # Si l'objet existe déjà
            try:
                original = ChecklistItem.objects.get(pk=self.pk)
                
                # Stocker les valeurs précédentes
                self.previous_quantity = original.quantity
                self.previous_status = original.status

                # Cas 1: Changement EXPLICITE de statut (depuis l'interface admin ou modal)
                if hasattr(self, '_explicit_status_change') and self._explicit_status_change:
                    # Garder le nouveau statut tel quel
                    pass
                
                # Cas 2: Changement de quantité
                elif self.quantity != original.quantity:
                    # TOUJOURS changer le statut en 'pending' quand la quantité change
                    # Peu importe le statut précédent
                    self.status = 'pending'
                    self.com = 'complete'

                    # Log des changements
                    QuantityChangeLog.objects.create(
                        checklist_item=self,
                        previous_quantity=original.quantity,
                        new_quantity=self.quantity,
                        quantity_change=self.quantity - original.quantity,
                        changed_by=getattr(self, '_changed_by', None),
                        previous_status=original.status,
                    )
                
                # Cas 3: Aucun changement de quantité et pas de changement explicite
                else:
                    # Si le statut a changé mais pas la quantité, c'est un changement manuel
                    if self.status != original.status:
                        # Permettre le changement de statut
                        pass
                    else:
                        # Garder tout tel quel
                        self.status = original.status
                        
            except ChecklistItem.DoesNotExist:
                pass

        super().save(*args, **kwargs)
        
        # Après la sauvegarde, mettre à jour le statut du checklist parent
        if self.checklist:
            self.checklist.update_status()
        
        # Nettoyer l'attribut temporaire
        if hasattr(self, '_explicit_status_change'):
            delattr(self, '_explicit_status_change')

    def __str__(self):
        return f"{self.product.name} - {self.checklist.name}"

    def delete(self, *args, **kwargs):
        if self.product:
            self.product.adjust_quantity(self.quantity)
        super().delete(*args, **kwargs)

class QuantityChangeLog(models.Model):
    checklist_item = models.ForeignKey(ChecklistItem, on_delete=models.CASCADE)
    previous_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    quantity_change = models.IntegerField()  # The difference between previous and new quantity
    previous_status = models.CharField(max_length=20, null=True, blank=True)  # Log the previous status
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Change log for {self.checklist_item.product.name} - {self.timestamp}"



class ChecklistItemChangeLog(models.Model):
    ACTION_CHOICES = [
        ('added', 'Added'),
        ('modified', 'Modified'),
        ('deleted', 'Deleted'),
    ]
    
    checklist_item = models.ForeignKey(ChecklistItem, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    previous_quantity = models.IntegerField(null=True, blank=True)
    previous_status = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"{self.action} - {self.checklist_item.product.name} on {self.timestamp}"

class ChecklistChangeLog(models.Model):
    ACTION_CHOICES = [
        ('added', 'Added'),
        ('modified', 'Modified'),
        ('deleted', 'Deleted'),
    ]
    
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - Checklist ID {self.checklist.id} on {self.timestamp}"

class Inventory(models.Model):
    item = models.ForeignKey(ItemInv, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True, default=0)
    # other fields as needed

    def __str__(self):
        return f"{self.item.name} - Quantity: {self.quantity}"

class ProductPhoto(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='product_photos')
    image = models.ImageField(upload_to='listings/media/products')
    caption = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'Photo for {self.product.name} - {self.caption or "No Caption"}'


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



class Recupfrigo(models.Model):
    livraison = models.ForeignKey(Livraison, on_delete=models.CASCADE, related_name='livraison_recupfrigo', default=None)
    def __str__(self):
        return f'Recupfrigo for {self.livraison}'
    date = models.DateField(null=True)
    filled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    filled_at = models.DateTimeField(default=timezone.now)



class RecupfrigoItem(models.Model):
    recupfrigo = models.ForeignKey(Recupfrigo, on_delete=models.CASCADE, related_name='items_frigo', default=None)
    item_name = models.CharField(max_length=200, choices=[
        ('plateaux', 'plateaux'),
        ('bols', 'bols'),
        ('pinces', 'pinces'),
        ('ramequins', 'ramequins'),
        ('verres', 'verres'),
        ('paniers', 'paniers'),
        ('thermos', 'thermos'),
        ('cambro', 'cambro'),
        ('tempkeep', 'tempkeep'),
    ])
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f'{self.item_name} - {self.quantity}'

class Recuplivreur(models.Model):
        livraison = models.ForeignKey(Livraison, on_delete=models.CASCADE, related_name='livraison_recuplivreur', default=None)
        def __str__(self):
            return f'Recuplivreur for {self.livraison}'
        date = models.DateField(null=True)
        filled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
        filled_at = models.DateTimeField(default=timezone.now)


class RecuplivreurItem(models.Model):
    recuplivreur = models.ForeignKey(Recuplivreur, on_delete=models.CASCADE, related_name='items_livreur', null=True)
    item_name = models.CharField(max_length=200, choices=[
        ('plateaux', 'plateaux'),
        ('bols', 'bols'),
        ('porcelaine', 'porcelaine'),
        ('ramequins', 'ramequins'),
        ('insertion', 'insertion'),
        ('plateau de bois', 'plateau de bois'),
        ('paniers', 'paniers'),
        ('verres', 'verres'),
        ('thermos', 'thermos'),
        ('cambro', 'cambro'),
        ('tempkeep', 'tempkeep'),
        ('pinces', 'pinces'),

    ])
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.item_name} - {self.quantity}'
    



class CategoryCuisine(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ItemCuisine(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(CategoryCuisine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    photo = models.ImageField(upload_to='listings/media/commandesdetail', blank=True, null=True)


    def __str__(self):
        return f'{self.name}'

class OrderCuisine(models.Model):
    item = models.ForeignKey(ItemCuisine, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    ordered_quantity = models.IntegerField()
    is_done = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    date_added = models.DateField(default=timezone.now)


    def __str__(self):
       return f"{self.item.name} ordered by {self.user.username}"

# models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class UniteMesure(models.Model):
    nom = models.CharField(max_length=50, unique=True)
    symbole = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Unité de mesure"
        verbose_name_plural = "Unités de mesure"
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.symbole})"

class Departement(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

# models.py - Version étendue (optionnel)

class Fournisseur(models.Model):
    nom = models.CharField(max_length=200, unique=True)
    email = models.EmailField(blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    adresse = models.TextField(blank=True)
    contact_principal = models.CharField(max_length=100, blank=True)
    
    # Champs supplémentaires pour stocker plus d'infos
    type_produits = models.TextField(blank=True, help_text="Types de produits fournis")
    procedure_commande = models.TextField(blank=True, help_text="Procédure et horaires de commande")
    notes = models.TextField(blank=True, help_text="Informations supplémentaires")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nom']
    
    def __str__(self):
        return self.nom

class Ingredient(models.Model):
    nom = models.CharField(max_length=200, unique=True)
    unite_mesure = models.ForeignKey(UniteMesure, on_delete=models.PROTECT, related_name='ingredients')
    stock_reel = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock_alerte = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nom']
    
    def __str__(self):
        return f"{self.nom} ({self.unite_mesure.symbole})"
    
    @property
    def besoin_reappro(self):
        return self.stock_reel <= self.stock_alerte

class CatalogueFournisseur(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.CASCADE, related_name='catalogues')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='catalogues')
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    date_debut = models.DateField(default=timezone.now)
    date_fin = models.DateField(null=True, blank=True)
    reference_fournisseur = models.CharField(max_length=100, blank=True)
    conditionnement = models.CharField(max_length=100, blank=True)
    delai_livraison = models.IntegerField(default=1, help_text="Délai en jours")
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Catalogue fournisseur"
        verbose_name_plural = "Catalogues fournisseurs"
        ordering = ['-date_debut']
        unique_together = [['fournisseur', 'ingredient', 'date_debut']]
    
    def __str__(self):
        return f"{self.fournisseur.nom} - {self.ingredient.nom} - {self.prix}€"

class Recette(models.Model):
    nom = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    explication_fabrication = models.TextField()
    photo = models.ImageField(upload_to='recettes/', blank=True, null=True)
    departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, related_name='recettes')
    temps_preparation = models.IntegerField(default=0, help_text="Temps en minutes")
    temps_cuisson = models.IntegerField(default=0, help_text="Temps en minutes")
    portions = models.IntegerField(default=1)
    cout_calcule = models.DecimalField(max_digits=10, decimal_places=2, default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['nom']
    
    def __str__(self):
        return self.nom
    
    def calculer_cout(self):
        cout_total = Decimal('0')
        # Coût des ingrédients directs
        for ri in self.recette_ingredients.all():
            if ri.ingredient.catalogues.filter(actif=True).exists():
                prix = ri.ingredient.catalogues.filter(actif=True).first().prix
                cout_total += prix * ri.quantite
        # Coût des sous-recettes
        for sr in self.sous_recettes.all():
            cout_total += sr.calculer_cout() * sr.quantite
        self.cout_calcule = cout_total
        self.save(update_fields=['cout_calcule'])
        return cout_total

class SousRecette(models.Model):
    nom = models.CharField(max_length=200)
    recette_parent = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name='sous_recettes')
    explication_fabrication = models.TextField()
    quantite = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Sous-recette"
        verbose_name_plural = "Sous-recettes"
        ordering = ['nom']
        unique_together = [['nom', 'recette_parent']]
    
    def __str__(self):
        return f"{self.nom} (de {self.recette_parent.nom})"
    
    def calculer_cout(self):
        cout_total = Decimal('0')
        for sri in self.sousrecette_ingredients.all():
            if sri.ingredient.catalogues.filter(actif=True).exists():
                prix = sri.ingredient.catalogues.filter(actif=True).first().prix
                cout_total += prix * sri.quantite
        return cout_total

class RecetteIngredient(models.Model):
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE, related_name='recette_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='recette_ingredients')
    quantite = models.DecimalField(max_digits=10, decimal_places=3)
    
    class Meta:
        verbose_name = "Ingrédient de recette"
        verbose_name_plural = "Ingrédients de recette"
        unique_together = [['recette', 'ingredient']]
    
    def __str__(self):
        return f"{self.ingredient.nom} - {self.quantite} {self.ingredient.unite_mesure.symbole}"

class SousRecetteIngredient(models.Model):
    sous_recette = models.ForeignKey(SousRecette, on_delete=models.CASCADE, related_name='sousrecette_ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='sousrecette_ingredients')
    quantite = models.DecimalField(max_digits=10, decimal_places=3)
    
    class Meta:
        verbose_name = "Ingrédient de sous-recette"
        verbose_name_plural = "Ingrédients de sous-recette"
        unique_together = [['sous_recette', 'ingredient']]
    
    def __str__(self):
        return f"{self.ingredient.nom} - {self.quantite} {self.ingredient.unite_mesure.symbole}"

# models.py - Modèle Commande corrigé

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal
from datetime import date

class Commande(models.Model):
    STATUT_CHOICES = [
        ('BROUILLON', 'Brouillon'),
        ('CONFIRMEE', 'Confirmée'),
        ('EN_COURS', 'En cours'),
        ('LIVREE', 'Livrée'),
        ('ANNULEE', 'Annulée'),
    ]
    
    numero = models.CharField(max_length=50, unique=True, blank=True)
    fournisseur = models.ForeignKey('Fournisseur', on_delete=models.PROTECT, related_name='commandes')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='BROUILLON')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_livraison_prevue = models.DateField(null=True, blank=True)
    date_livraison_reelle = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    notes_validation = models.TextField(blank=True)
    montant_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Champs de validation - IMPORTANT: null=True, blank=True
    signature = models.TextField(blank=True, null=True)  # Changé pour permettre NULL
    validee_par = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    commande_parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sous_commandes')
    
    # Champ JSON optionnel pour stocker les détails de validation
    validation_details = models.JSONField(default=dict, blank=True, null=True)
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"
    
    def __str__(self):
        return f"Commande {self.numero} - {self.fournisseur.nom}"
    
    def save(self, *args, **kwargs):
        # Mise à jour automatique du statut si date_livraison_prevue = aujourd'hui
        if self.date_livraison_prevue and self.date_livraison_prevue == date.today():
            # Ne change le statut que si la commande n'est pas déjà livrée ou annulée
            if self.statut not in ['LIVREE', 'ANNULEE']:
                self.statut = 'EN_COURS'
        
        # Génération du numéro de commande si nécessaire
        if not self.numero:
            # Générer un numéro unique
            last_commande = Commande.objects.filter(
                date_creation__year=timezone.now().year
            ).order_by('-id').first()
            
            if last_commande and last_commande.numero:
                try:
                    # Extraire le numéro de la dernière commande
                    last_num = int(last_commande.numero.split('-')[-1])
                    new_num = last_num + 1
                except (ValueError, IndexError):
                    new_num = 1
            else:
                new_num = 1
            
            self.numero = f"CMD-{timezone.now().year}-{new_num:05d}"
        
        super().save(*args, **kwargs)
    
    def calculer_total(self):
        """Calcule et met à jour le montant total de la commande"""
        from django.db.models import Sum, F
        
        total = self.lignes.aggregate(
            total=Sum(F('quantite') * F('prix_unitaire'))
        )['total'] or Decimal('0')
        
        self.montant_total = total
        self.save(update_fields=['montant_total'])
        return total
    
    @property
    def nombre_lignes(self):
        """Retourne le nombre de lignes dans la commande"""
        return self.lignes.count()
    
    @property
    def est_modifiable(self):
        """Vérifie si la commande peut être modifiée"""
        return self.statut not in ['LIVREE', 'ANNULEE']
    
    @classmethod
    def update_statuts_du_jour(cls):
        """
        Méthode de classe pour mettre à jour toutes les commandes 
        dont la date de livraison prévue est aujourd'hui.
        À appeler via une tâche cron ou celery.
        """
        cls.objects.filter(
            date_livraison_prevue=date.today(),
            statut__in=['BROUILLON', 'CONFIRMEE']  # Ne met à jour que ces statuts
        ).update(statut='EN_COURS')

from decimal import Decimal, InvalidOperation
from django.db import models

from django.db import models
from decimal import Decimal, InvalidOperation

class LigneCommande(models.Model):
    # Champs existants
    commande = models.ForeignKey('Commande', on_delete=models.CASCADE, related_name='lignes')
    ingredient = models.ForeignKey('Ingredient', on_delete=models.PROTECT)
    quantite = models.DecimalField(max_digits=10, decimal_places=3)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    sous_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    notes = models.TextField(blank=True, null=True)
    
    # NOUVEAUX CHAMPS pour la validation
    quantite_recue = models.DecimalField(
        max_digits=10, 
        decimal_places=3,
        null=True,
        blank=True,
        help_text="Quantité réellement reçue lors de la validation"
    )
    
    qualite_validation = models.CharField(
        max_length=20,
        choices=[
            ('OK', 'Qualité OK'),
            ('PROBLEME', 'Problème qualité'),
            ('NON_VERIFIE', 'Non vérifié'),
        ],
        default='NON_VERIFIE',
        blank=True,
        help_text="Statut de la qualité lors de la réception"
    )
    
    date_validation = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date et heure de validation de cette ligne"
    )

    class Meta:
        verbose_name = "Ligne de commande"
        verbose_name_plural = "Lignes de commande"
        unique_together = [['commande', 'ingredient']]

    def __str__(self):
        unite = ''
        if hasattr(self.ingredient, 'unite_mesure') and self.ingredient.unite_mesure:
            unite = f" {self.ingredient.unite_mesure.symbole}"
        return f"{self.ingredient.nom} - {self.quantite}{unite}"

    def save(self, *args, **kwargs):
        # Forcer la conversion en Decimal pour éviter float * Decimal
        try:
            quantite_decimal = Decimal(str(self.quantite)) if not isinstance(self.quantite, Decimal) else self.quantite
        except (InvalidOperation, TypeError):
            quantite_decimal = Decimal('0')

        try:
            prix_decimal = Decimal(str(self.prix_unitaire)) if not isinstance(self.prix_unitaire, Decimal) else self.prix_unitaire
        except (InvalidOperation, TypeError):
            prix_decimal = Decimal('0')

        self.sous_total = quantite_decimal * prix_decimal
        super().save(*args, **kwargs)
    
    # NOUVELLES PROPRIÉTÉS pour faciliter l'utilisation
    @property
    def sous_total_reel(self):
        """Calcule le sous-total réel basé sur la quantité reçue"""
        if self.quantite_recue is not None:
            try:
                qte = Decimal(str(self.quantite_recue))
                prix = Decimal(str(self.prix_unitaire))
                return (qte * prix).quantize(Decimal('0.01'))
            except:
                return self.sous_total
        return self.sous_total
    
    @property
    def difference_quantite(self):
        """Calcule la différence entre quantité commandée et reçue"""
        if self.quantite_recue is not None:
            try:
                return Decimal(str(self.quantite_recue)) - Decimal(str(self.quantite))
            except:
                return Decimal('0')
        return Decimal('0')
    
    @property
    def a_probleme_qualite(self):
        """Vérifie si cette ligne a un problème de qualité"""
        return self.qualite_validation == 'PROBLEME'
    
    @property
    def a_difference_quantite(self):
        """Vérifie s'il y a une différence de quantité"""
        return self.quantite_recue is not None and self.quantite_recue != self.quantite



class ProductionPrevue(models.Model):
    """Pour stocker temporairement les prévisions de production lors de la création de commande"""
    recette = models.ForeignKey(Recette, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    date_production = models.DateField()
    session_key = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Production prévue"
        verbose_name_plural = "Productions prévues"


# models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Sum

class Character(models.Model):
    """Modèle pour les personnages jouables"""
    name = models.CharField(max_length=100, verbose_name="Nom du personnage")
    description = models.TextField(verbose_name="Description")
    emoji = models.CharField(max_length=5, default="⚽", verbose_name="Emoji représentatif")
    
    # Image du personnage
    image = models.ImageField(
        upload_to='characters/', 
        null=True, 
        blank=True,
        verbose_name="Image du personnage",
        help_text="Image du personnage (format recommandé: 200x200px)"
    )
    
    # Statistiques du personnage (0-100)
    power = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Puissance de tir",
        help_text="Force du tir (0-100)"
    )
    precision = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Précision",
        help_text="Précision du tir (0-100)"
    )
    luck = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Chance",
        help_text="Probabilité de marquer malgré le gardien (0-100)"
    )
    curve = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Effet/Courbe",
        help_text="Capacité à donner de l'effet au ballon (0-100)",
        default=50
    )
    
    # Prix et disponibilité
    price = models.IntegerField(
        default=0,
        verbose_name="Prix en pièces",
        help_text="0 = Gratuit/Débloqué par défaut"
    )
    is_premium = models.BooleanField(
        default=False,
        verbose_name="Premium",
        help_text="Personnage premium nécessitant un achat"
    )
    
    # Atouts et défauts
    strengths = models.TextField(
        verbose_name="Atouts",
        help_text="Points forts du personnage",
        blank=True
    )
    weaknesses = models.TextField(
        verbose_name="Défauts", 
        help_text="Points faibles du personnage",
        blank=True
    )
    
    # Métadonnées
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        verbose_name = "Personnage"
        verbose_name_plural = "Personnages"
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.emoji} {self.name}"
    
    @property
    def overall_rating(self):
        """Calcule la note globale du personnage"""
        return (self.power + self.precision + self.luck + self.curve) // 4


class BallSkin(models.Model):
    """Skins pour les ballons"""
    name = models.CharField(max_length=100, verbose_name="Nom du skin")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(
        upload_to='ball_skins/',
        verbose_name="Image du ballon",
        help_text="Image du skin de ballon"
    )
    price = models.IntegerField(
        default=100,
        verbose_name="Prix en pièces"
    )
    emoji = models.CharField(max_length=5, default="⚽", verbose_name="Emoji")
    
    # Effets visuels
    trail_color = models.CharField(
        max_length=7,
        default="#FFFFFF",
        verbose_name="Couleur de la traînée",
        help_text="Code couleur hexadécimal"
    )
    has_particles = models.BooleanField(
        default=False,
        verbose_name="Effets de particules"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        verbose_name = "Skin de ballon"
        verbose_name_plural = "Skins de ballons"
        ordering = ['order', 'price']
    
    def __str__(self):
        return f"{self.emoji} {self.name} - {self.price} pièces"


class PlayerSkin(models.Model):
    """Skins pour les joueurs"""
    name = models.CharField(max_length=100, verbose_name="Nom du skin")
    description = models.TextField(blank=True, verbose_name="Description")
    character = models.ForeignKey(
        Character,
        on_delete=models.CASCADE,
        related_name='skins',
        verbose_name="Personnage associé",
        null=True,  # Temporaire pour la migration
        blank=True
    )

    image = models.ImageField(
        upload_to='player_skins/',
        verbose_name="Image du skin",
        help_text="Image du skin de joueur"
    )
    price = models.IntegerField(
        default=200,
        verbose_name="Prix en pièces"
    )
    emoji = models.CharField(max_length=5, default="👕", verbose_name="Emoji")
    
    # Couleurs du maillot
    primary_color = models.CharField(
        max_length=7,
        default="#FF0000",
        verbose_name="Couleur principale",
        help_text="Code couleur hexadécimal"
    )
    secondary_color = models.CharField(
        max_length=7,
        default="#FFFFFF",
        verbose_name="Couleur secondaire",
        help_text="Code couleur hexadécimal"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")

    
    
    class Meta:
        verbose_name = "Skin de joueur"
        verbose_name_plural = "Skins de joueurs"
        ordering = ['order', 'price']
    
    def __str__(self):
        return f"{self.emoji} {self.name} - {self.price} pièces"


class PowerUp(models.Model):
    """Power-ups et objets bonus"""
    POWERUP_TYPES = [
        ('precision', 'Précision améliorée'),
        ('power', 'Puissance accrue'),
        ('slowmo', 'Ralenti'),
        ('multiball', 'Multi-ballon'),
        ('giant_target', 'Cibles géantes'),
        ('freeze_keeper', 'Gardien figé'),
        ('golden_ball', 'Ballon doré (x2 points)'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nom du power-up")
    powerup_type = models.CharField(
        max_length=20,
        choices=POWERUP_TYPES,
        verbose_name="Type de power-up"
    )
    description = models.TextField(verbose_name="Description")
    emoji = models.CharField(max_length=5, default="⭐", verbose_name="Emoji")
    
    # Image
    image = models.ImageField(
        upload_to='powerups/',
        null=True,
        blank=True,
        verbose_name="Image du power-up"
    )
    
    # Prix et durée
    price = models.IntegerField(
        default=50,
        verbose_name="Prix en pièces"
    )
    duration = models.IntegerField(
        default=30,
        verbose_name="Durée (secondes)",
        help_text="Durée de l'effet en secondes"
    )
    
    # Effets
    effect_value = models.FloatField(
        default=1.5,
        verbose_name="Valeur de l'effet",
        help_text="Multiplicateur ou valeur de l'effet"
    )
    
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        verbose_name = "Power-up"
        verbose_name_plural = "Power-ups"
        ordering = ['order', 'price']
    
    def __str__(self):
        return f"{self.emoji} {self.name} - {self.price} pièces"


class UserProfileFoot(models.Model):
    """Profil étendu de l'utilisateur pour le jeu"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='game_profile'
    )
    
    # Monnaie du jeu
    coins = models.IntegerField(
        default=100,
        verbose_name="Pièces",
        validators=[MinValueValidator(0)]
    )
    gems = models.IntegerField(
        default=0,
        verbose_name="Gemmes",
        validators=[MinValueValidator(0)]
    )
    
    # Niveau et expérience
    level = models.IntegerField(default=1, verbose_name="Niveau")
    experience = models.IntegerField(default=0, verbose_name="Expérience")
    
    # Personnage sélectionné
    selected_character = models.ForeignKey(
        Character,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Personnage sélectionné"
    )
    selected_ball_skin = models.ForeignKey(
        BallSkin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Skin de ballon sélectionné"
    )
    selected_player_skin = models.ForeignKey(
        PlayerSkin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Skin de joueur sélectionné"
    )
    
    # Statistiques globales
    total_goals = models.IntegerField(default=0, verbose_name="Buts totaux")
    total_games = models.IntegerField(default=0, verbose_name="Parties jouées")
    best_score = models.IntegerField(default=0, verbose_name="Meilleur score")
    total_targets_hit = models.IntegerField(default=0, verbose_name="Cibles touchées")
    
    # Achievements
    achievements = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Succès débloqués"
    )
    
    # Dernière connexion
    last_daily_bonus = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Dernier bonus quotidien"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Profil de joueur"
        verbose_name_plural = "Profils de joueurs"
    
    def __str__(self):
        return f"Profil de {self.user.username} - Niveau {self.level}"
    
    @property
    def win_rate(self):
        """Calcule le taux de réussite"""
        if self.total_games == 0:
            return 0
        return round((self.total_goals / (self.total_games * 5)) * 100, 1)  # Assuming 5 shots per game


class Purchase(models.Model):
    """Historique des achats"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='purchases'
    )
    
    # Type d'achat (polymorphique)
    character = models.ForeignKey(
        Character,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ball_skin = models.ForeignKey(
        BallSkin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    player_skin = models.ForeignKey(
        PlayerSkin,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    powerup = models.ForeignKey(
        PowerUp,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Prix et monnaie
    price = models.IntegerField(verbose_name="Prix payé")
    currency = models.CharField(
        max_length=10,
        choices=[('coins', 'Pièces'), ('gems', 'Gemmes')],
        default='coins',
        verbose_name="Monnaie utilisée"
    )
    
    purchased_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Achat"
        verbose_name_plural = "Achats"
        ordering = ['-purchased_at']
    
    def __str__(self):
        item = self.character or self.ball_skin or self.player_skin or self.powerup
        return f"{self.user.username} - {item} - {self.price} {self.currency}"


class DifficultyLevel(models.Model):
    """Modèle pour les niveaux de difficulté"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Facile'),
        ('medium', 'Moyen'),
        ('hard', 'Difficile'),
        ('extreme', 'Extrême'),
        ('impossible', 'Impossible'),
    ]
    
    difficulty_id = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        unique=True,
        verbose_name="Type de difficulté"
    )
    name = models.CharField(max_length=100, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    emoji = models.CharField(max_length=5, default="⚽", verbose_name="Emoji")
    
    # Configuration du gardien
    goalkeeper_speed = models.IntegerField(
        default=500,
        verbose_name="Vitesse du gardien (ms)",
        help_text="Temps entre chaque mouvement du gardien en millisecondes"
    )
    goalkeeper_size = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.5), MaxValueValidator(3.0)],
        verbose_name="Taille du gardien",
        help_text="Multiplicateur de taille (1.0 = normal)"
    )
    
    # Distance du coup franc
    distance = models.IntegerField(
        default=20,
        validators=[MinValueValidator(10), MaxValueValidator(50)],
        verbose_name="Distance (mètres)",
        help_text="Distance du coup franc en mètres"
    )
    
    # Mur de défenseurs
    wall_enabled = models.BooleanField(
        default=False,
        verbose_name="Mur de défenseurs",
        help_text="Active le mur de défenseurs"
    )
    wall_players = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(6)],
        verbose_name="Nombre de joueurs dans le mur"
    )
    wall_jump_probability = models.FloatField(
        default=0.5,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Probabilité de saut du mur",
        help_text="Probabilité que le mur saute (0-1)"
    )
    
    # Cibles bonus
    target_count = models.IntegerField(
        default=3,
        validators=[MinValueValidator(0), MaxValueValidator(9)],
        verbose_name="Nombre de cibles",
        help_text="Nombre de cibles bonus dans le but"
    )
    target_size = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.5), MaxValueValidator(2.0)],
        verbose_name="Taille des cibles",
        help_text="Multiplicateur de taille des cibles"
    )
    
    # Bonus de score et récompenses
    score_multiplier = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.5), MaxValueValidator(10.0)],
        verbose_name="Multiplicateur de score",
        help_text="Bonus de points pour cette difficulté"
    )
    coin_multiplier = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.5), MaxValueValidator(5.0)],
        verbose_name="Multiplicateur de pièces",
        help_text="Bonus de pièces pour cette difficulté"
    )
    
    # Configuration visuelle
    background_color = models.CharField(
        max_length=7,
        default="#90EE90",
        verbose_name="Couleur de fond",
        help_text="Code couleur hexadécimal"
    )
    
    # AJOUTEZ CE CHAMP
    is_active = models.BooleanField(
        default=True,
        verbose_name="Actif",
        help_text="Difficulté disponible pour les joueurs"
    )
    
    # Ordre d'affichage
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    
    class Meta:
        verbose_name = "Niveau de difficulté"
        verbose_name_plural = "Niveaux de difficulté"
        ordering = ['order', 'difficulty_id']
    
    def __str__(self):
        return f"{self.emoji} {self.name} ({self.get_difficulty_id_display()})"


class Score(models.Model):
    """Modèle pour enregistrer les scores"""
    player = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Joueur",
        related_name='game_scores',
        null=True,  # Ajoutez temporairement null=True
        blank=True  # Ajoutez blank=True pour l'admin
    )
    character = models.ForeignKey(
        Character,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Personnage utilisé"
    )
    difficulty = models.ForeignKey(
        DifficultyLevel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Difficulté"
    )
    
    # Score et récompenses
    score = models.IntegerField(verbose_name="Score", default=0)
    coins_earned = models.IntegerField(default=0, verbose_name="Pièces gagnées")
    exp_earned = models.IntegerField(default=0, verbose_name="Expérience gagnée")
    
    # Statistiques détaillées
    total_shots = models.IntegerField(default=0, verbose_name="Tirs totaux")
    successful_shots = models.IntegerField(default=0, verbose_name="Tirs réussis")
    targets_hit = models.IntegerField(default=0, verbose_name="Cibles touchées")
    perfect_shots = models.IntegerField(default=0, verbose_name="Tirs parfaits")
    max_combo = models.IntegerField(default=0, verbose_name="Combo maximum")
    
    # Power-ups utilisés
    powerups_used = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Power-ups utilisés"
    )
    
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    
    class Meta:
        verbose_name = "Score"
        verbose_name_plural = "Scores"
        ordering = ['-score', '-date']
    
    def __str__(self):
        player_name = self.player.username if self.player else "Anonyme"
        return f"{player_name} - {self.score} pts ({self.difficulty.name if self.difficulty else 'N/A'})"
    
    @property
    def accuracy(self):
        """Calcule le pourcentage de réussite"""
        if self.total_shots == 0:
            return 0
        return round((self.successful_shots / self.total_shots) * 100, 1)

class Leaderboard(models.Model):
    """Classement global"""
    PERIOD_CHOICES = [
        ('daily', 'Quotidien'),
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuel'),
        ('alltime', 'Tous les temps'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='leaderboard_entries'
    )
    period = models.CharField(
        max_length=10,
        choices=PERIOD_CHOICES,
        verbose_name="Période"
    )
    score = models.IntegerField(verbose_name="Score total")
    rank = models.IntegerField(verbose_name="Rang")
    games_played = models.IntegerField(default=0, verbose_name="Parties jouées")
    
    # Récompenses de classement
    reward_claimed = models.BooleanField(
        default=False,
        verbose_name="Récompense réclamée"
    )
    
    period_start = models.DateTimeField(verbose_name="Début de la période")
    period_end = models.DateTimeField(verbose_name="Fin de la période")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Classement"
        verbose_name_plural = "Classements"
        ordering = ['period', 'rank']
        unique_together = ['user', 'period', 'period_start']
    
    def __str__(self):
        return f"{self.user.username} - Rang {self.rank} ({self.get_period_display()})"