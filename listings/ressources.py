from import_export import resources
from .models import Livraison
from .models import Client
from .models import Livreur
from .models import ItemInv
from .models import Ingredient, UniteMesure

class LivraisonResource(resources.ModelResource):
    class Meta:
        model = Livraison

class ClientResource(resources.ModelResource):
    class Meta:
        model = Client

class LivreursResource(resources.ModelResource):
    class Meta:
        model = Livreur

class ItemResource(resources.ModelResource):
    class Meta:
        model = ItemInv

class IngredientResource(resources.ModelResource):
    class Meta:
        model = Ingredient
        import_id_fields = ['nom']
        fields = ('nom')

class UniteMesureResource(resources.ModelResource):
    class Meta:
        model = UniteMesure
        import_id_fields = ['nom', 'symbole']
        fields = ('nom', 'symbole')