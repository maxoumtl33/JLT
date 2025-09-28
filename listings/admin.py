from django.contrib import admin
from listings.models import Livraison
from listings.models import Livreur
from listings.models import Client
from listings.models import Inventory
from listings.models import Journee
from listings.models import ItemInv
from listings.models import ChecklistItem
from listings.models import Route
from listings.models import Distances
from listings.models import *
from listings.models import Tacheafaire

from listings.models import Photo, Phototaches
from listings.models import Checklist, Product


from django.contrib.auth.models import User, Group
from import_export.admin import ImportExportModelAdmin
from .models import Livraison
#from listings.models import Route

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)

admin.site.register(UserProfile, UserProfileAdmin)

class ChecklistItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'checklist', 'status', 'quantity', 'is_completed']
    list_filter = ['status', 'checklist']
    search_fields = ['product__name', 'checklist__name']

class LivraisonAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nom', 'date', 'heure_livraison')


class LivreursAdmin(ImportExportModelAdmin):
    list_display = ('nom')

class ItemInvAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'photo', 'description')

class ProductAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name', 'quantity')

class MenuAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name')

class DeliverymodeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'name')

class PlatAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nom')

class ClientAdmin(ImportExportModelAdmin):
    list_display = ('id', 'company_name', 'billing_address', 'contact_person', 'phone', 'email', 'etage', 'ordered_by' )

class InventoryAdmin(ImportExportModelAdmin):
    list_display = ('id', 'item', 'quantity')

class JourneeAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nom', 'date')

class RouteAdmin(ImportExportModelAdmin):
    list_display = ('id', 'nom', 'date')

admin.site.unregister(Group)
admin.site.register(Livraison, LivraisonAdmin)
admin.site.register(Journee, JourneeAdmin)
admin.site.register(Livreur)
admin.site.register(Route, RouteAdmin)
admin.site.register(Task)
admin.site.register(ChecklistItem)
admin.site.register(Distances)
admin.site.register(Photo)
admin.site.register(PhotoRecup)
admin.site.register(RecupfrigoItem)
admin.site.register(RecuplivreurItem)
admin.site.register(Recupfrigo)
admin.site.register(Recuplivreur)
admin.site.register(Tacheafaire)
admin.site.register(Checklist)
admin.site.register(Phototaches)
admin.site.register(Product,ProductAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(ItemInv, ItemInvAdmin)
admin.site.register(ItemCuisine)
admin.site.register(OrderCuisine)
admin.site.register(CategoryCuisine)
admin.site.register(Shift)
admin.site.register(LoadingDock)
admin.site.register(Group)
admin.site.register(Md)
admin.site.register(ChecklistDocument)
admin.site.register(Conseiller)
admin.site.register(Category)
admin.site.register(Vehicle)
admin.site.register(PhotoVehicle)
admin.site.register(Submission)
admin.site.register(Menu, MenuAdmin)
admin.site.register(DeliveryMode, DeliverymodeAdmin)
admin.site.register(Plat, PlatAdmin)
admin.site.register(MenuSubmission)
admin.site.register(Score)
admin.site.register(PaymentMode)
admin.site.register(Notification)
admin.site.register(Commande)
