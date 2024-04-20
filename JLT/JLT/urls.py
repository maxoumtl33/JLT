from django.contrib import admin
from django.urls import path, include
from listings import views
from django.conf import settings
from django.conf.urls.static import static
from listings.views import *
urlpatterns = [
path('admin/', admin.site.urls, name ="admin"),
path('', include('django_dyn_dt.urls')),  # <-- NEW: API routing rules
path('livraison/<int:ip>/', views.livraison_detail, name='livraison-detail'),
path('', views.home, name='home'),
path('members/', include('members.urls')),
path('members/', include('django.contrib.auth.urls')),
path('livraisons_list/', views.livraisons_list, name = 'livraisons-list'),
path('journees_list/', views.journees_list, name = 'journees-list'),
path('journee/<int:id>/', views.journee_detail, name='journee-detail'),
path('journee/<int:id>/livreur/<int:pk>', views.dashboard, name='dashboard'),
path('recuperation/<int:id>/', views.recuperation_detail, name='recuperation-detail'),
path('livreur_list/', views.livreur_list, name = 'livreur-list'),
path('responsables/journee/<int:id>/', views.responsables, name = 'responsables'),
path('acceuilresp', views.responsableschoixjournee, name = 'acceuilresponsables'),
path('distance', DistanceView.as_view(), name = 'my_distance_view'),
path('map', MapView.as_view(), name = 'my_map_view'),
path('mapmidi', MapMidiView.as_view(), name = 'my_mapmidi_view'),
path('mapaprem', MapApremView.as_view(), name = 'my_mapaprem_view'),
path('delete_distance/<str:pk>/', views.deleteDistance, name = 'deletedistance'),
path('livreur/<int:pk>/', views.livreur_detail, name='livreur-detail'),
path('livraisonstomorrow/', views.livraisonstomorrow, name='livraisonstomorrow'),
path('geocoding/<int:pk>/', GeocodingView.as_view(), name='geocoding'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



