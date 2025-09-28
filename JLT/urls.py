from django.contrib import admin
from django.urls import path, include
from listings import views
from django.conf import settings
from django.conf.urls.static import static
from listings.views import save_positions
from listings.views import *
from listings.viewsets import *
from django.urls import path, include
from listings.views import CustomPasswordChangeView, home
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as drf_views

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'livreurs', LivreurViewSet, basename='livreur')
router.register(r'conseillers', ConseillerViewSet, basename='conseiller')
router.register(r'mds', MdViewSet, basename='md')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'modes', ModeViewSet, basename='mode')
router.register(r'categories', CategorieViewSet, basename='categorie')
router.register(r'produits', ProduitViewSet, basename='produit')
router.register(r'taches', TacheafaireViewSet, basename='tache')

urlpatterns = [

path('api/', include(router.urls)),
path('api-token-auth/', drf_views.obtain_auth_token, name='api_token_auth'),
path(
        'members/password_change/',
        CustomPasswordChangeView.as_view(),
        name='password_change',
    ),
path('password_change_done/', TemplateView.as_view(template_name="registration/password_change_done.html"), name='password_change_done'),
path('select2/', include('django_select2.urls')),
path('items/<str:category>/', view_items_by_category, name='view_items_by_category'),
path('validate_checklist/<int:checklist_item_id>/', validate_checklist_item, name='validate_checklist'),
path('adjust-quantity/', views.adjust_product_quantity, name='adjust_product_quantity'),
path('admin/', admin.site.urls, name ="admin"),
path('login/', views.custom_login, name='login'),
path('update_checklist_item_comment/<int:item_id>/', views.update_checklist_item_comment, name='update_checklist_item_comment'),
path('associate_livraison/<int:checklist_id>/', views.associate_livraison, name='associate_livraison'),
path('livraison/<int:ip>/', views.livraison_detail, name='livraison-detail'),
path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
path('update_position/', save_positions, name='save_position'),
path('create-route/', views.CreateRouteView.as_view(), name='create_route'),
path('create-routeaujour/', views.CreateRouteAujourView.as_view(), name='create_routeaujour'),
path('create-routetoday/', views.CreateRouteTodayView.as_view(), name='create_routetoday'),
path('create-routedim/', views.CreateRouteDimView.as_view(), name='create_routedim'),
path('', views.home, name='home'),
path('remettre-stock/', views.remettre_en_stock, name='remettre_stock'),  # Ajoutez cette ligne
path('get_submissions_for_created_at/<int:day>/', views.get_submissions_created_at, name='get_submissions_created_at'),
path('get_submissions_for_day/<int:day>/', views.get_submission_for_day, name='get_submissions_for_day'),
path('get_checklists_for_day/<int:day>/', views.get_checklists_for_day, name='get_checklists_for_day'),
path('members/', include('members.urls')),
path('members/', include('django.contrib.auth.urls')),
path('livraisons_list/', views.livraisons_list, name = 'livraisons-list'),
path('journees_list/', views.journees_list, name = 'journees-list'),
path('journee/<int:id>/', views.journee_detail, name='journee-detail'),
path('api/checklist-items-by-date/', views.api_checklist_items_by_date, name='api_checklist_items_by_date'),
path('api/checklist-items-encours/', views.api_checklist_items_encours, name='api_checklist_items_encours'),
path('journeevente/<int:id>/', views.journeedetailvente, name='journeedetailvente'),
path('vehicle/delete/<int:vehicle_id>/', delete_vehicle, name='delete_vehicle'),  # Add this line
path('journee/<int:id>/livreur/<int:pk>', views.dashboard, name='dashboard'),
path('livreur_list/', views.livreur_list, name = 'livreur-list'),
path('responsables/journee/<int:id>/', views.responsables, name = 'responsables'),
path('acceuilresp', views.responsableschoixjournee, name = 'acceuilresponsables'),
path('distance', DistanceView.as_view(), name = 'my_distance_view'),
path('unauthorized/', views.unauthorized_view, name='unauthorized'),
path('mapaujour', MapAujourView.as_view(), name = 'my_mapaujour_view'),
path('mapmidiaujour', MapMidiAujourView.as_view(), name = 'my_mapmidiaujour_view'),
path('mapapremaujour', MapApremAujourView.as_view(), name = 'my_mapapremaujour_view'),
path('map', MapView.as_view(), name = 'my_map_view'),
path('mapmidi', MapMidiView.as_view(), name = 'my_mapmidi_view'),
path('create-random-task/', create_random_task, name='create_random_task'),
path('mapaprem', MapApremView.as_view(), name = 'my_mapaprem_view'),
path('product/create/', views.create_product, name='create_product'),
path('maptoday', MapTodayView.as_view(), name = 'my_maptoday_view'),
path('maptodaymidi', MapMidiTodayView.as_view(), name = 'my_maptodaymidi_view'),
path('maptodayaprem', MapApremTodayView.as_view(), name = 'my_maptodayaprem_view'),
path('mapdim', MapDimView.as_view(), name = 'my_mapdim_view'),
path('mapdimmidi', MapMidiDimView.as_view(), name = 'my_mapdimmidi_view'),
path('mapdimyaprem', MapApremDimView.as_view(), name = 'my_mapdimaprem_view'),
path('tacheslist', tacheslist, name = 'tacheslist'),
path('delete_distance/<str:pk>/', views.deleteDistance, name = 'deletedistance'),
path('livreur/<int:pk>/', views.livreur_detail, name='livreur-detail'),
path('livraisonstomorrow/', views.livraisonstomorrow, name='livraisonstomorrow'),
path('inline-update-product/', views.product_inline_update, name='product_inline_update'),
path('livraisonstoday/', views.livraisonstoday, name='livraisonstoday'),
path('livraisonsresp/', views.livraisonsresp, name='livraisonsresp'),
path('livraisonshier/', views.livraisonshier, name='livraisonshier'),
path('geocode-all-livraisons/', GeocodeAllLivraisonsView.as_view(), name='geocode_all_livraisons'),path('geocodingtoday/<int:pk>/', GeocodingTodayView.as_view(), name='geocodingtoday'),
path('api/submission/<int:submission_id>/delete-submenu/<int:submenu_id>/', views.delete_menu_submission, name='delete_submenu'),
path('recuptoday/', views.recuptoday, name='recuptoday'),
path('save_score/', views.save_score, name='save_score'),
path('scores/top/', views.top_scores, name='top_scores'),
path('generate-multiple-pdfs/', views.generate_multiple_pdfs, name='generate_multiple_pdfs'),
path('generate-multiple-pdfs-en/', views.generate_multiple_pdfs_en, name='generate_multiple_pdfs_en'),
path('etiquette-tente/', views.etiquette_tente, name='etiquette-tente'),
path('jeux/', views.jeux, name='jeux'),
path('manage/', manage_submissions, name='manage_submissions'),  # For managing submissions
path('api/get_checklist_items_for_date/', views.get_checklist_items_for_date, name='get_checklist_items_for_date'),
path('livraisonsventes/<int:pk>/', views.livraisonsventesdetail, name='livraisonventesdetail'),
path("livraisonsdrag/", views.Livraisonsdrag.as_view(), name='livraisonsdrag'),
path('livraison/edit/<int:livraison_id>/', livraison_edit_form, name='livraison-edit-form'),
path('livraisonsdrag/<int:pk>/', views.livraisonsdrag_detail, name='livraisonsdrag-detail'),
path('delete_photo/<int:photo_id>/', delete_photo_md, name='delete_photo'),
path('livraisonsdragtoday/<int:pk>/', views.livraisonsdrag_detailtoday, name='livraisonsdrag-detailtoday'),
path('livraisonsdragtoday/<int:pk>/edit', views.livraison_edit_formtoday, name='livraison-edit-formtoday'),
path("livraisonsdragtoday/", views.Livraisonsdragtoday.as_view(), name='livraisonsdragtoday'),
path('update_status/', views.update_status, name='update_status'),
path('submit/', submit_request, name='submit_request'),  # For submitting a new Soumission or Contrat
path('submission/<int:submission_id>/', submission_detail, name='submission_detail'),
path('get-conseiller-username/', get_conseiller_username, name='get_conseiller_username'),
path('submission_dashboard/status/update/<int:submission_id>/', update_submission_status_dashboard, name='update_dashboard_submission_status'),
path('update_submission/<int:submission_id>/', update_submission_status, name='update_submission_status'),  # For updating submission status
path('duplicate-recups/', views.duplicate_selected_recups, name='duplicate-selected-recups'),
path('api/submission/<int:submission_id>/update-status/', views.update_submission_status_detail, name='update_submission_status'),
path('associer-toutes_dock/', views.associer_toutes_livraisons_docks, name='associer_toutes_dock'),
path('update-payment-mode/', views.update_payment_mode, name='update_payment_mode'),
path('update-recup/<int:livraison_id>/', views.update_recup_date_journee, name='update_recup'),
path('api/paymentmode/create/', views.create_payment_mode, name='create_payment_mode'),
path('livraisons/statistiques/', livraison_stats_view, name='dashboard_stats'),
path('get_livraisons/<int:journee_id>/', views.get_livraisons, name='get_livraisons'),
path('get_livraisons_chaud/<int:journee_id>/', views.get_livraisons_chaud, name='get_livraisons_chaud'),
path('submission/<int:submission_id>/update/', update_submission, name='update_submission'),
path('get_client_details/<int:client_id>/', views.get_client_details, name='get_client_details'),
path('calendarsubcreate_view/', calendarsubcreate_view, name='calendarsubcreate_view'),
path('calendarsub_view/', calendarsub_view, name='calendarsub_view'),
path('modify-dock/', modify_dock_view, name='modify_dock_view'),  # URL pattern for modify dock
path('save_credit_card/', save_credit_card_info, name='save_credit_card_info'),
path('commentcamarche/', views.commentcamarche, name='commentcamarche'),
path('associate-livraisons/', associate_livraisons_with_docks, name='associate_livraisons_with_docks'),
path('livraisonrespdetail/<int:ip>/', views.livraisonrespdetail, name='livraisonrespdetail'),
path('routedetail/<int:id>/', views.routedetail, name='routedetail'),
path('route/update/<int:pk>/', RouteUpdateView.as_view(), name='route_update'),
path('loading-docks/', loading_docks_view, name='loading_docks_view'),
path('taskdetail/<int:id>/', views.taskdetail, name='taskdetail'),
path('livraison/<int:livraison_id>/validate/', views.validate_livraison, name='validate_livraison'),
path('checklist/<int:checklist_id>/duplicate/', views.duplicate_checklist, name='duplicate-checklist'),
path('duplicate/<int:model_id>/', duplicate_model, name='duplicate-model'),
path('update_photo/<int:pk>/', update_photo, name='update_photo'),
path('inventory/', views.inventory, name='inventory'),
path('upload_document/<int:checklist_id>/', views.upload_document, name='upload_document'),
path('delete_document/<int:document_id>/', views.delete_document, name='delete_document'),
path('update-livraison-positions/', views.update_livraison_positions, name='update-livraison-positions'),
path('get-route-livraisons/<int:route_id>/', views.get_route_livraisons, name='get_route_livraisons'),
path('product/qr/<int:product_id>/', views.generate_qr_code, name='product_qr_code'),
path('recupslist/', views.recupslist, name='recupslist'),
path('journeerecupdetail/<int:id>/', views.journeerecupdetail, name='journeerecupdetail'),
path('recupfrigo/<int:id>/', views.recupfrigo_detail, name='recupfrigo_detail'),
path('recuplivreur/<int:id>/', views.recuplivreur_detail, name='recuplivreur_detail'),
path('product/update/<int:product_id>/', views.update_product_quantity, name='product_quantity_update'),
path('import/', views.import_items, name='import_items'),
path('creerchecklist/', views.creerchecklist, name='creerchecklist'),
path('checklist/<int:checklist_id>/add/', views.add_to_checklist, name='add_to_checklist'),
path('checklist/<int:checklist_id>/add-products/', views.add_products_to_checklist, name='add_products_to_checklist'),
path('checklist/<int:checklist_id>/', views.checklist_products, name='checklist-detail'),
path('iteminv/<int:item_id>/', views.product_detail, name='product_detail'),
path('subtract/<int:checklist_id>/', views.subtract_to_checklist, name='subtract_checklist'),
path('voirchecklist/', views.voir_checklist, name='voir_checklist'),
path('get_products_by_category/', views.get_products_by_category, name='get_products_by_category'),
path('checklistvoir/<int:checklist_id>/', views.checklistvoir_detail, name='checklistvoir-detail'),
path('edit_task_form/<int:task_id>/', views.edit_task_form, name='edit_task_form'),
path('import-xlsx/', import_xlsx, name='import_xlsx'),
path('checklist-item/<int:pk>/delete-ajax/', ChecklistItemDeleteAjaxView.as_view(), name='checklist-item-delete-ajax'),
path('update_livraison/', views.update_livraison, name='update_livraison'),
path('update_livraison_route/', views.update_livraison_route, name='update_livraison_route'),
path('create_routes/', create_routes, name='create_routes'),
path('create_routesnext/', create_routesn, name='create_routesn'),
path('create_routesnextnext/', create_routesnn, name='create_routesnn'),
path('products/', views.product_list, name='product_list'),
path('create_shift/', views.create_shift, name='create-shift'),
path('responsablelist/', responsable_list, name='responsablelist'),
path('success/', views.success_page, name='success_page'),
path('checklist/<int:checklist_id>/en_cours/', views.checklist_en_cours_view, name='checklist_en_cours'),
path('api/checklist-items-encours/', views.checklist_items_encours_par_date, name='checklist_items_encours_par_date'),
path('geocode_all_livraisons/', views.geocode_all_livraisons, name='geocode_all_livraisons'),
path('faq/', faq, name='faq'),
path('livraisons/group/', group_livraisons, name='group_livraisons'),
path('checklists/associate-all/', associate_all_livraisons, name='associate_all_livraisons'),
path('create_journee/', create_journee, name='create_journee'),
path('delete_livraison/<int:livraison_id>/', delete_livraison, name='delete_livraison'),  # ✅ Add this
path('bulk_edit_livraisons/', bulk_edit_livraisons, name='bulk_edit_livraisons'),
path('update_checklist_status/<int:checklist_id>/', views.update_checklist_status, name='update_checklist_status'),
path('update_checklist_item/', views.update_checklist_item, name='update_checklist_item'),  # New URL for updating
path('update-checklist-item-vente/<int:item_id>/', views.update_checklist_item_quantity, name='update_checklist_item_quantity'),path('livraisons_without_date/', livraisons_without_date, name='livraisons_without_date'),
path('product/<int:product_id>/change-logs/', views.view_quantity_change_logs, name='view_quantity_change_logs'),
path('checklist/<int:checklist_id>/save_breuvages_report/', views.save_breuvages_report, name='save_breuvages_report'),
path('checklist/<int:checklist_id>/breuvages/', views.get_breuvages_products, name='get_breuvages_products'),
path('checklist/<int:checklist_id>/search_productsbase/', views.search_productsbase, name='search_productsbase'),
path('checklist/<int:checklist_id>/search_productsjetable/', views.search_productsjetable, name='search_productsjetable'),
path('checklist/<int:checklist_id>/search_productsbar/', views.search_productsbar, name='search_productsbar'),
path('checklist/<int:checklist_id>/search_productsdecor/', views.search_productsdecor, name='search_productsdecor'),
path('checklist/<int:checklist_id>/search_productscafe/', views.search_productscafe, name='search_productscafe'),
path('checklist/<int:checklist_id>/search_productstable/', views.search_productstable, name='search_productstable'),
path('checklist/<int:checklist_id>/search_productsverre/', views.search_productsverre, name='search_productsverre'),
path('checklist/<int:checklist_id>/search_productsporcelaine/', views.search_productsporcelaine, name='search_productsporcelaine'),
path('checklist/<int:checklist_id>/search_productscanape/', views.search_productscanape, name='search_productscanape'),
path('checklist/<int:checklist_id>/search_productscuisson/', views.search_productscuisson, name='search_productscuisson'),
path('checklist/<int:checklist_id>/search_productsservice/', views.search_productsservice, name='search_productsservice'),
path('checklist/<int:checklist_id>/search_productsdivers/', views.search_productsdivers, name='search_productsdivers'),
path('checklist/<int:checklist_id>/search_productsalcoolfort/', views.search_productsalcoolfort, name='search_productsalcoolfort'),
path('checklist/<int:checklist_id>/search_productsbieres/', views.search_productsbieres, name='search_productsbieres'),
path('checklist/<int:checklist_id>/search_productsvins/', views.search_productsvins, name='search_productsvins'),
path('checklist/<int:checklist_id>/search_productssansalcool/', views.search_productssansalcool, name='search_productssansalcool'),
path('submission/<int:submission_id>/change-user/', views.change_submission_user, name='change-user'),
path('submission/<int:submission_id>/duplicate/', duplicate_submission, name='duplicate_submission'),
path('submission/<int:submission_id>/duplicate-without-menus/', duplicate_submission_without_menus, name='duplicate_submission_without_menus'),
path('notification/read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
path('checklist/<int:checklist_id>/search_productscfcdn/', views.search_productscfcdn, name='search_productscfcdn'),
path('md_dashboard/', views.md_dashboard, name='md_dashboard'),
path('conseiller-dashboard/', views.conseiller_dashboard, name='conseiller_dashboard'),
path('submission/<int:submission_id>/add-note/', views.add_note, name='add_note'),
path('submissions/date/<str:date>/', views.submissions_by_date, name='submissions_by_date'),
path('shifts/', views.view_shifts_by_date, name='view_shifts_by_date'),
path('create-loading-dock/', create_loading_dock, name='create_loading_dock'),
path('routesfrigo/', routesfrigo, name='routesfrigo'),
path('checklistmd/<int:pk>/', ChecklistmdDetailView, name='checklistmd_detail'),  # Adjust the URL pattern as needed
path('update-task/<int:pk>/', views.update_task, name='update_task'),
path('create-recupfrigo/', create_recupfrigo, name='create_recupfrigo'),
path('create-recuplivreur/<int:livraison_id>/', create_recuplivreur, name='create_recuplivreur'),
path('create_order_cuisine/', views.create_ordercuisine, name='create_order_cuisine'),
path('orders_cuisine/', views.order_listcuisine, name='order_list_cuisine'),
path('orders_cuisine/<int:order_id>/done/', views.mark_order_donecuisine, name='mark_order_done_cuisine'),
path('orders_cuisine/<int:order_id>/delivered/', views.mark_order_deliveredcuisine, name='mark_order_delivered_cuisine'),
path('user/orders/', views.user_order_list, name='user_order_list'),
path('order/<int:order_id>/update/', views.update_order_cuisine, name='update_order_cuisine'),
path('order/<int:order_id>/delete/', views.delete_order_cuisine, name='delete_order_cuisine'),
path('route/delete/<int:route_id>/', delete_route, name='delete_route'),


    # Dashboard
    path('dashboard_commande/', views.dashboard_commande, name='dashboard_commande'),
    
    # Unités de mesure
    path('unites/', views.UniteMesureListView.as_view(), name='unite_mesure_list'),
    path('unites/create/', views.UniteMesureCreateView.as_view(), name='unite_mesure_create'),
    path('unites/<int:pk>/update/', views.UniteMesureUpdateView.as_view(), name='unite_mesure_update'),
    path('unites/<int:pk>/delete/', views.UniteMesureDeleteView.as_view(), name='unite_mesure_delete'),
    
    # Départements
    path('departements/', views.DepartementListView.as_view(), name='departement_list'),
    path('departements/create/', views.DepartementCreateView.as_view(), name='departement_create'),
    path('departements/<int:pk>/update/', views.DepartementUpdateView.as_view(), name='departement_update'),
    path('departements/<int:pk>/delete/', views.DepartementDeleteView.as_view(), name='departement_delete'),
    
    # Fournisseurs
    path('fournisseurs/', views.FournisseurListView.as_view(), name='fournisseur_list'),
    path('fournisseurs/create/', views.FournisseurCreateView.as_view(), name='fournisseur_create'),
    path('fournisseurs/<int:pk>/update/', views.FournisseurUpdateView.as_view(), name='fournisseur_update'),
    path('fournisseurs/<int:pk>/delete/', views.FournisseurDeleteView.as_view(), name='fournisseur_delete'),
    
    # Ingrédients
    path('ingredients/', views.IngredientListView.as_view(), name='ingredient_list'),
    path('ingredients/create/', views.IngredientCreateView.as_view(), name='ingredient_create'),
    path('ingredients/<int:pk>/update/', views.IngredientUpdateView.as_view(), name='ingredient_update'),
    path('ingredients/<int:pk>/delete/', views.IngredientDeleteView.as_view(), name='ingredient_delete'),
    
    # Catalogue fournisseurs
    path('catalogue/', views.CatalogueFournisseurListView.as_view(), name='catalogue_list'),
    path('catalogue/create/', views.CatalogueFournisseurCreateView.as_view(), name='catalogue_create'),
    path('catalogue/<int:pk>/update/', views.CatalogueFournisseurUpdateView.as_view(), name='catalogue_update'),
    path('catalogue/<int:pk>/delete/', views.CatalogueFournisseurDeleteView.as_view(), name='catalogue_delete'),
    path('catalogue/import/', views.import_catalogue, name='catalogue_import'),
    
    # Recettes
    path('recettes/', views.RecetteListView.as_view(), name='recette_list'),
    path('recettes/create/', views.recette_create, name='recette_create'),
    path('recettes/<int:pk>/', views.RecetteDetailView.as_view(), name='recette_detail'),
    path('recettes/<int:pk>/update/', views.recette_update, name='recette_update'),
    path('recettes/<int:pk>/delete/', views.RecetteDeleteView.as_view(), name='recette_delete'),
    path('recettes/<int:pk>/duplicate/', views.recette_duplicate, name='recette_duplicate'),
    
    # Sous-recettes
    path('recettes/<int:recette_pk>/sous-recettes/create/', views.sous_recette_create, name='sous_recette_create'),
    path('sous-recettes/<int:pk>/update/', views.sous_recette_update, name='sous_recette_update'),
    path('sous-recettes/<int:pk>/delete/', views.sous_recette_delete, name='sous_recette_delete'),
    
    # Commandes
    path('commandes/', views.CommandeListView.as_view(), name='commande_list'),
    path('commandes/create/', views.commande_create, name='commande_create'),
    path('commandes/calendar/', views.commande_calendar, name='commande_calendar'),
    path('commandes/<int:pk>/', views.commande_detail, name='commande_detail'),
    path('commandes/<int:pk>/print/', views.commande_print, name='commande_print'),
    path('commandes/<int:pk>/cancel/', views.commande_cancel, name='commande_cancel'),
    path('commandes/<int:pk>/edit/', CommandeUpdateView.as_view(), name='commande_edit'),
    path('commandes/<int:pk>/delete/', CommandeDeleteView.as_view(), name='commande_delete'),
    # API endpoints pour AJAX
    path('api/ingredients/search/', views.api_ingredients_search, name='api_ingredients_search'),
    path('api/ingredients/<int:ingredient_id>/fournisseurs/', views.api_fournisseurs_ingredient, name='api_fournisseurs_ingredient'),
    path('api/recettes/departements/', views.api_recettes_departements, name='api_recettes_departements'),
    path('api/stock/update/', views.api_stock_update, name='api_stock_update'),
    
    # Exports
    path('exports/ingredients/', views.export_ingredients, name='export_ingredients'),
    path('exports/recettes/', views.export_recettes, name='export_recettes'),
    path('exports/commandes/', views.export_commandes, name='export_commandes'),

    path('api/fournisseur/<int:fournisseur_id>/ingredients/', 
         FournisseurIngredientsAPIView.as_view(), 
         name='api_fournisseur_ingredients'),

    path('catalogue/import/hector/', views.import_hector_larivee, name='import_hector_larivee'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



htmx_urlpatterns = [
    path('sort/', views.sort, name='sort'),
    path('edit/<int:pk>/', views.edit_item, name='edit_item'),
]

urlpatterns += htmx_urlpatterns