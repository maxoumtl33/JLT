from django.contrib import admin
from listings.models import Livraison
from listings.models import Livreur
from listings.models import Client
from listings.models import Tacheafaire
from listings.models import Journee
from listings.models import Recuperation
from listings.models import Message
from django.contrib.auth.models import User, Group
#from listings.models import Route

admin.site.unregister(Group)

class LivraisonAdmin(admin.ModelAdmin): 
    list_display = ('nom', 'date', 'route', 'client', 'heure_livraison')

class ClientAdmin(admin.ModelAdmin): 
    list_display = ('nom', 'adresse_lieux', 'adresse_dock', 'contact')

admin.site.register(Livraison, LivraisonAdmin)
admin.site.register(Journee)
admin.site.register(Recuperation)
admin.site.register(Message)
admin.site.register(Livreur)
admin.site.register(Tacheafaire)
admin.site.register(Client, ClientAdmin)
#admin.site.register(Route)
