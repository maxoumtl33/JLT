# serializers.py
from rest_framework import serializers
from .models import (
    User, Livreur, Conseiller, Md, UserProfile,
    Client, Menu, DeliveryMode, Product, Category, Tacheafaire
)
from rest_framework.permissions import IsAdminUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class LivreurSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    
    class Meta:
        model = Livreur
        fields = '__all__'
        

class ConseillerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Conseiller
        fields = '__all__'
        

class MdSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False, allow_null=True)
    class Meta:
        model = Md
        fields = '__all__'
        


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'

class DeliveryModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMode
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    delivery_modes = DeliveryModeSerializer(many=True, read_only=True)
    class Meta:
        model = Menu
        fields = '__all__'

class TacheafaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tacheafaire
        fields = '__all__'
