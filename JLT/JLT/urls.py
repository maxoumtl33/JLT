from django.contrib import admin
from django.urls import path, include
from listings import views
from django.conf import settings
from django.conf.urls.static import static
from listings.views import save_positions
from listings.views import *
urlpatterns = [
path('admin/', admin.site.urls, name ="admin"),
path('livraison/<int:ip>/', views.livraison_detail, name='livraison-detail'),
path('update_position/', save_positions, name='save_position'),
path('', views.home, name='home'),
path('members/', include('members.urls')),
path('members/', include('django.contrib.auth.urls')),
path('livraisons_list/', views.livraisons_list, name = 'livraisons-list'),
path('journees_list/', views.journees_list, name = 'journees-list'),
path('journee/<int:id>/', views.journee_detail, name='journee-detail'),
path('journee/<int:id>/livreur/<int:pk>', views.dashboard, name='dashboard'),
path('livreur_list/', views.livreur_list, name = 'livreur-list'),
path('responsables/journee/<int:id>/', views.responsables, name = 'responsables'),
path('acceuilresp', views.responsableschoixjournee, name = 'acceuilresponsables'),
path('distance', DistanceView.as_view(), name = 'my_distance_view'),
path('map', MapView.as_view(), name = 'my_map_view'),
path('mapmidi', MapMidiView.as_view(), name = 'my_mapmidi_view'),
path('mapaprem', MapApremView.as_view(), name = 'my_mapaprem_view'),
path('maptoday', MapTodayView.as_view(), name = 'my_maptoday_view'),
path('maptodaymidi', MapMidiTodayView.as_view(), name = 'my_maptodaymidi_view'),
path('maptodayaprem', MapApremTodayView.as_view(), name = 'my_maptodayaprem_view'),
path('delete_distance/<str:pk>/', views.deleteDistance, name = 'deletedistance'),
path('livreur/<int:pk>/', views.livreur_detail, name='livreur-detail'),
path('livraisonstomorrow/', views.livraisonstomorrow, name='livraisonstomorrow'),
path('livraisonstoday/', views.livraisonstoday, name='livraisonstoday'),
path('livraisonsresp/', views.livraisonsresp, name='livraisonsresp'),
path('livraisonshier/', views.livraisonshier, name='livraisonshier'),
path('geocoding/<int:pk>/', GeocodingView.as_view(), name='geocoding'),
path('geocodingtoday/<int:pk>/', GeocodingTodayView.as_view(), name='geocodingtoday'),
path('recuptoday/', views.recuptoday, name='recuptoday'),
path('livraisonsventes/<int:pk>/', views.livraisonsventesdetail, name='livraisonventesdetail'),
path("livraisonsdrag/", views.Livraisonsdrag.as_view(), name='livraisonsdrag'),
path('livraisonsdrag/<int:pk>/edit', views.livraison_edit_form, name='livraison-edit-form'),
path('livraisonsdrag/<int:pk>/', views.livraisonsdrag_detail, name='livraisonsdrag-detail'),
path('livraisonsdragtoday/<int:pk>/', views.livraisonsdrag_detailtoday, name='livraisonsdrag-detailtoday'),
path('livraisonsdragtoday/<int:pk>/edit', views.livraison_edit_formtoday, name='livraison-edit-formtoday'),
path("livraisonsdragtoday/", views.Livraisonsdragtoday.as_view(), name='livraisonsdragtoday'),
path('update_status/', views.update_status, name='update_status'),
path('commentcamarche/', views.commentcamarche, name='commentcamarche'),
path('livraisonrespdetail/<int:ip>/', views.livraisonrespdetail, name='livraisonrespdetail'),
path('routedetail/<int:id>/', views.routedetail, name='routedetail'),
path('duplicate/<int:model_id>/', duplicate_model, name='duplicate-model'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



htmx_urlpatterns = [
    path('add-livraison/', views.add_livraison, name='add-livraison'),
    path('add-livraisontoday/', views.add_livraisontoday, name='add-livraisontoday'),
    path('delete-livraison/<int:pk>/', views.delete_livraison, name='delete-livraison'),
    path('sort/', views.sort, name='sort'),
]

urlpatterns += htmx_urlpatterns