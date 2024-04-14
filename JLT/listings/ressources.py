from import_export import resources
from .models import Livraison

class LivraisonResource(resources.ModelResource):
    class Meta:
        model = Livraison