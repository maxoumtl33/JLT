from django.contrib import admin
from listings.models import Livraison
from listings.models import Livreur
from listings.models import Client
from listings.models import Tacheafaire
from listings.models import Journee
from listings.models import Recuperation
from listings.models import Message
from listings.models import Route
from listings.models import Distances

from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin
from .models import Livraison
#from listings.models import Route

class LivraisonAdmin(ImportExportModelAdmin):
    list_display = ('nom', 'date', 'client', 'heure_livraison')

class LivreursAdmin(ImportExportModelAdmin):
    list_display = ('nom')

class ClientAdmin(ImportExportModelAdmin):
    list_display = ('nom', 'adresse_lieux', 'adresse_dock', 'contact')

admin.site.unregister(Group)




admin.site.register(Livraison, LivraisonAdmin)
admin.site.register(Journee)
admin.site.register(Livreur)
admin.site.register(Route)
admin.site.register(Distances)
admin.site.register(Client, ClientAdmin)
#admin.site.register(Route)
