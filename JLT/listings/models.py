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
        latitude = models.FloatField()
        longitude = models.FloatField()
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
     def __str__(self):
        return f'{self.nom}'
     date = models.DateField()



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
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
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

    choicesmode = [('assiette', 'Assiette'),
        ('buffet_porcelaine', 'Buffet porcelaine'),
        ('buffet_jetable', 'Buffet jetable'),
        ('coffret', 'Coffret'),
        ('menu', 'Menu')]
    
    name = models.CharField(max_length=30, choices=choicesmode, null=True, blank=True)  # Mode d'envoi

    def __str__(self):
        return self.name

class Plat(models.Model):
    nom = models.CharField(max_length=130)
    nom_english = models.CharField(max_length=130, null=True, blank=True)
    def __str__(self):
        return self.nom
    
    
class Menu(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    allergie = models.TextField(blank=True, null=True)
    delivery_modes = models.ManyToManyField(DeliveryMode, blank=True)

    def __str__(self):
        return self.name
    
from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class Submission(models.Model):
    SUBMISSION_TYPE_CHOICES = [
        ('Soumission événement', 'Soumission_événement'),
        ('Commande événement', 'Commande_événement'),
        ('Soumission BAL/Buffet', 'Soumission_BAL_Buffet'),
        ('Commande BAL/Buffet', 'Commande_BAL_Buffet'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submission_type = models.CharField(max_length=24, choices=SUBMISSION_TYPE_CHOICES)
    
    # New fields
    refusal_comment = models.TextField(null=True, blank=True)
    company_name = models.CharField(max_length=100, null=True, blank=True)  # Company name
    event_location = models.CharField(max_length=200, null=True, blank=True)  # Lieu événement
    contact_person = models.CharField(max_length=100, null=True, blank=True)  # Contact sur place
    ordered_by = models.CharField(max_length=100, null=True, blank=True)  # Commandé par
    phone = models.CharField(max_length=15, null=True, blank=True)  # Telephone
    email = models.EmailField(max_length=100, null=True, blank=True)  # Email
    billing_address = models.CharField(max_length=200, null=True, blank=True)  # Adresse facturation
    commentaire = models.CharField(max_length=200, null=True, blank=True) 
    payment_mode = models.CharField(max_length=20, choices=[
        ('cc', 'Carte de Crédit'),
        ('cheque', 'Chèque'),
        ('interac', 'Interact'),
    ], null=True, blank=True)  # Mode paiement
    date = models.DateField(null=True, blank=True)  # Date
    event_time = models.TimeField(null=True, blank=True)  # Heure événement
    guest_count = models.IntegerField(null=True, blank=True)  # Nombre personne
    delivery_time = models.TimeField(null=True, blank=True)  # Heure livraison
    budget = models.IntegerField(null=True, blank=True)  # Budget
    service_count = models.CharField(max_length=100, null=True, blank=True)  # Nombre de service (as string)
    sub_menus = models.ManyToManyField(Menu, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
        ('envoyé', 'Envoyé'),
    ]

    STATUS_CHOICESS = [
        ('cc', 'Carte de Crédit'),
        ('cheque', 'Chèque'),
        ('interac', 'Interact'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours')

    def save(self, *args, **kwargs):
        # Set created_at to now minus 4 hours
        if not self.created_at:  # If created_at is not already set
            self.created_at = timezone.now() - timedelta(hours=4)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.submission_type} by {self.user} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}. Company: {self.company_name if self.company_name else 'N/A'}"
    

from django.db import models

class MenuSubmission(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='menu_submissions')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    allergies = models.TextField(null=True, blank=True)  # Field to save allergies
    delivery_mode = models.ForeignKey(DeliveryMode, on_delete=models.SET_NULL, null=True, blank=True)  # Link to DeliveryMode

    def __str__(self):
        return f"Menu '{self.menu.name}' for {self.submission.company_name} (ID {self.id})"


from django.shortcuts import render, get_object_or_404
from .models import Submission

def submission_detail(request, submission_id):
    # Get the specific submission instance
    submission = get_object_or_404(Submission, id=submission_id)

    context = {
        'submission': submission,
    }

    return render(request, 'listings/submission_detail.html', context)
    

class ChecklistDocument(models.Model):
    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE, related_name='documents')
    document = models.FileField(upload_to='listings/media/commandesdetail')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document for {self.checklist.name}"



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
    consumed_quantity = models.PositiveIntegerField(default=0)  # Amount that has been consumed
    unconsumed_quantity = models.PositiveIntegerField(default=0)  # Amount that remains unconsumed
    commentaire = models.CharField(max_length=100, null=True)
    com = models.CharField(max_length=100, null=True)
    previous_quantity = models.PositiveIntegerField(default=0)
    previous_status = models.CharField(max_length=100, null=True)
    is_stock_updated = models.BooleanField(default=False)

    # Remove or comment this line if you won't use it
    # skip_inventory_update = False  

    class Meta:
        unique_together = ('checklist', 'product', 'status')

    def clean(self):
        super().clean()
        if ChecklistItem.objects.filter(checklist=self.checklist, product=self.product).exclude(id=self.id).exists():
            raise ValidationError('This product already has a status in this checklist.')

    def save(self, *args, **kwargs):
        if self.commentaire:
            self.commentaire = self.commentaire.lower()

        if self.pk:  # If the object exists, retrieve the previous state
            try:
                original = ChecklistItem.objects.get(pk=self.pk)
            except ChecklistItem.DoesNotExist:
                original = None

            if original:
                self.previous_quantity = original.quantity
                self.previous_status = original.status  # Store previous status

                # If quantity changes, update status to 'pending'
                if self.quantity != original.quantity:
                    self.status = 'pending'  
                    self.com = 'complete'

                    # Log the changes
                    QuantityChangeLog.objects.create(
                        checklist_item=self,
                        previous_quantity=original.quantity,
                        new_quantity=self.quantity,
                        quantity_change=self.quantity - original.quantity,
                        changed_by=getattr(self, '_changed_by', None),
                        previous_status=original.status,  # Log previous status
                    )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.checklist.name}"




    def delete(self, *args, **kwargs):
        if self.product:
            self.product.adjust_quantity(self.quantity) # Optional: Only if you want to handle deletions
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

