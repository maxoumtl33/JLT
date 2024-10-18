from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime
from datetime import date








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
     date = models.DateField(default=date.today)




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
    client = models.ForeignKey(Client, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.fields.DateField(null=True, blank=True)
    date_livraison = models.fields.DateField(null=True, blank=True)
    commentaire = models.fields.CharField(null=True, blank=True, max_length=500)
    commentairedispatch = models.fields.CharField(null=True, blank=True, max_length=500000, default=" ")
    infodetail = models.fields.CharField(null=True, blank=True, max_length=500000, default=".")
    livreur = models.ForeignKey(Livreur, null=True, blank=True, on_delete=models.SET_NULL)
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
    photo = models.ImageField(upload_to='listings/media/commandesdetail', blank=True, null=True)
    def __str__(self):
        return f'{self.nom}'


class Photo(models.Model):
    livraison = models.ForeignKey('Livraison', on_delete=models.CASCADE, related_name='livraison_photos')
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



class Product(models.Model):
    choices = (
         ('ÉQUIPEMENT DE BASE', 'ÉQUIPEMENT DE BASE'),
         ('JETABLE', 'JETABLE'),
         ('ACCESSOIRES DE DÉCOR', 'ACCESSOIRES DE DÉCOR'),
         ('ÉQUIPEMENT DE BAR', 'ÉQUIPEMENT DE BAR'),
         ('ÉQUIPEMENT POUR SERVICE CAFÉ','ÉQUIPEMENT POUR SERVICE CAFÉ'),
         ('TABLE ET LINGE DE TABLE','TABLE ET LINGE DE TABLE'),
         ('VERRERIE','VERRERIE'),
         ('PORCELAINE ET COUTELLERIE','PORCELAINE ET COUTELLERIE'),
         ('ÉQUIPEMENT POUR MONTAGE CANAPÉS','ÉQUIPEMENT POUR MONTAGE CANAPÉS'),
         ('ÉQUIPEMENT DE CUISSON','ÉQUIPEMENT DE CUISSON'),
         ('USTENSILES DE SERVICE','USTENSILES DE SERVICE'),
         ('ITEMS DIVERS','ITEMS DIVERS'))


    name = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    category = models.CharField(max_length=100, choices= choices)

    def adjust_quantity(self, amount):
        """Adjust the product quantity."""
        self.quantity += amount
        self.save()


    def __str__(self):
        return self.name

class Checklist(models.Model):

    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
    ]


    name = models.CharField(max_length=100)
    products = models.ManyToManyField(Product, through='ChecklistItem')
    livraison = models.ForeignKey(Livraison, null=True, on_delete=models.SET_NULL, blank=True)
    date = models.fields.DateField(null=True, blank=True)
    lieu = models.CharField(max_length=10000, blank=True)
    num_contrat = models.fields.CharField(null=True, blank=True, max_length=200, default=" ")
    conseillere = models.CharField(max_length=100, blank=True)
    nb_convive = models.fields.CharField(null=True, blank=True, max_length=200, default=" ")
    heure_livraison = models.fields.CharField(null=True, blank=True, max_length=100, default=" ")
    md = models.fields.CharField(null=True, blank=True, max_length=100, default=" ")
    added_on = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours')


    def update_status(self):
        # Check if all items are 'valide'
        if self.checklistitem_set.filter(status='valide').count() == self.checklistitem_set.count():
            self.status = 'valide'
        elif self.checklistitem_set.filter(status='refuse').exists():
            self.status = 'refuse'
        else:
            self.status = 'en_cours'

        self.save()

    def __str__(self):
        return self.name


class ChecklistItem(models.Model):

    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('valide', 'Validé'),
        ('refuse', 'Refusé'),
    ]

    checklist = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=0, null=True)
    is_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours')

    class Meta:
        unique_together = ('checklist', 'product', 'status')  # Assure qu'un produit ne peut avoir qu'un seul statut dans une checklist


    def clean(self):
        super().clean()
        if ChecklistItem.objects.filter(checklist=self.checklist, product=self.product).exclude(id=self.id).exists():
            raise ValidationError('This product already has a status in the same checklist.')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update checklist status whenever this item is saved
        self.checklist.update_status()

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





