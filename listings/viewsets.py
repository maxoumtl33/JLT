from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .serializers import * 
from .models import *

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class LivreurViewSet(viewsets.ModelViewSet):
    queryset = Livreur.objects.all()
    serializer_class = LivreurSerializer
    permission_classes = [IsAdminUser]

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAdminUser]

class TacheafaireViewSet(viewsets.ModelViewSet):
    queryset = Tacheafaire.objects.all()
    serializer_class = TacheafaireSerializer
    permission_classes = [IsAdminUser]


class MdViewSet(viewsets.ModelViewSet):
    queryset = Md.objects.all()
    serializer_class = MdSerializer
    permission_classes = [IsAdminUser]


class ConseillerViewSet(viewsets.ModelViewSet):
    queryset = Conseiller.objects.all()
    serializer_class = ConseillerSerializer
    permission_classes = [IsAdminUser]


class ModeViewSet(viewsets.ModelViewSet):
    queryset = DeliveryMode.objects.all()
    serializer_class = DeliveryModeSerializer
    permission_classes = [IsAdminUser]


class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminUser]


class ProduitViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]


