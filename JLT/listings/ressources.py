from import_export import resources
from .models import Livraison
from .models import Client
from .models import Livreur

class LivraisonResource(resources.ModelResource):
    class Meta:
        model = Livraison

class ClientResource(resources.ModelResource):
    class Meta:
        model = Client

class LivreursResource(resources.ModelResource):
    class Meta:
        model = Livreur