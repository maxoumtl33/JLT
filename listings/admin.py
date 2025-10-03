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
admin.site.register(Score1)
admin.site.register(PaymentMode)
admin.site.register(Notification)
admin.site.register(Commande)
from .ressources import IngredientResource, UniteMesureResource

@admin.register(Ingredient)
class IngredientAdmin(ImportExportModelAdmin):
    resource_class = IngredientResource
    list_display = ('nom', 'unite_mesure', 'stock_reel', 'stock_alerte', 'description')
    search_fields = ('nom',)

@admin.register(UniteMesure)
class UniteMesureAdmin(ImportExportModelAdmin):
    resource_class = UniteMesureResource
    list_display = ('nom', 'symbole')
    search_fields = ('nom', 'symbole')


# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Sum, Avg
from .models import (
    Character, BallSkin, PlayerSkin, PowerUp, DifficultyLevel,
    UserProfile, Purchase, Score, Leaderboard
)

# Custom Admin Site Configuration
admin.site.site_header = "Free Kick Master - Administration"
admin.site.site_title = "Free Kick Master Admin"
admin.site.index_title = "Gestion du Jeu"


@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ['display_character', 'name', 'display_stats', 'price', 'is_premium', 'is_active', 'order']
    list_filter = ['is_active', 'is_premium', 'price']
    list_editable = ['order', 'is_active', 'price']
    search_fields = ['name', 'description']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Informations Générales', {
            'fields': ('name', 'description', 'emoji', 'image')
        }),
        ('Statistiques', {
            'fields': ('power', 'precision', 'luck', 'curve'),
            'description': 'Toutes les valeurs doivent être entre 0 et 100'
        }),
        ('Prix et Disponibilité', {
            'fields': ('price', 'is_premium', 'is_active')
        }),
        ('Caractéristiques', {
            'fields': ('strengths', 'weaknesses'),
            'classes': ('collapse',)
        }),
        ('Ordre', {
            'fields': ('order',)
        })
    )
    
    def display_character(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius: 5px;"> {} {}',
                obj.image.url, obj.emoji, obj.name
            )
        return format_html('{} {}', obj.emoji, obj.name)
    display_character.short_description = 'Personnage'
    
    def display_stats(self, obj):
        overall = obj.overall_rating
        color = '#4CAF50' if overall >= 80 else '#FFC107' if overall >= 60 else '#F44336'
        return format_html(
            '<div style="display: flex; gap: 5px;">'
            '<span title="Puissance">⚡{}</span>'
            '<span title="Précision">🎯{}</span>'
            '<span title="Chance">🍀{}</span>'
            '<span title="Courbe">🌀{}</span>'
            '<span style="background: {}; color: white; padding: 2px 6px; border-radius: 3px;">OVR: {}</span>'
            '</div>',
            obj.power, obj.precision, obj.luck, obj.curve, color, overall
        )
    display_stats.short_description = 'Statistiques'


@admin.register(BallSkin)
class BallSkinAdmin(admin.ModelAdmin):
    list_display = ['display_ball', 'name', 'price', 'has_particles', 'trail_color_preview', 'is_active', 'order']
    list_filter = ['is_active', 'has_particles', 'price']
    list_editable = ['order', 'is_active', 'price']
    search_fields = ['name', 'description']
    ordering = ['order', 'price']
    
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'description', 'emoji', 'image')
        }),
        ('Prix', {
            'fields': ('price',)
        }),
        ('Effets Visuels', {
            'fields': ('trail_color', 'has_particles')
        }),
        ('Paramètres', {
            'fields': ('is_active', 'order')
        })
    )
    
    def display_ball(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="30" height="30"> {} {}',
                obj.image.url, obj.emoji, obj.name
            )
        return format_html('{} {}', obj.emoji, obj.name)
    display_ball.short_description = 'Ballon'
    
    def trail_color_preview(self, obj):
        return format_html(
            '<div style="width: 30px; height: 30px; background: {}; border-radius: 50%; border: 2px solid #ccc;"></div>',
            obj.trail_color
        )
    trail_color_preview.short_description = 'Couleur Traînée'


# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import PlayerSkin

@admin.register(PlayerSkin)
class PlayerSkinAdmin(admin.ModelAdmin):
    list_display = ['name', 'character', 'emoji', 'price', 'display_colors', 'is_active']
    list_filter = ['character', 'is_active', 'price']
    search_fields = ['name', 'description']
    
    def display_colors(self, obj):
        """Affiche un aperçu des couleurs"""
        return format_html(
            '<span style="background-color: {}; padding: 3px 10px; margin-right: 5px;">&nbsp;</span>'
            '<span style="background-color: {}; padding: 3px 10px;">&nbsp;</span>',
            obj.primary_color,
            obj.secondary_color
        )
    display_colors.short_description = 'Couleurs' 
@admin.register(PowerUp)
class PowerUpAdmin(admin.ModelAdmin):
    list_display = ['display_powerup', 'name', 'powerup_type', 'price', 'duration', 'effect_value', 'is_active']
    list_filter = ['is_active', 'powerup_type', 'price']
    list_editable = ['price', 'duration', 'effect_value', 'is_active']
    search_fields = ['name', 'description']
    ordering = ['order', 'price']
    
    fieldsets = (
        ('Informations', {
            'fields': ('name', 'powerup_type', 'description', 'emoji', 'image')
        }),
        ('Prix et Durée', {
            'fields': ('price', 'duration')
        }),
        ('Effets', {
            'fields': ('effect_value',),
            'description': 'Valeur multiplicateur ou valeur de l\'effet'
        }),
        ('Paramètres', {
            'fields': ('is_active', 'order')
        })
    )
    
    def display_powerup(self, obj):
        return format_html('{} {}', obj.emoji, obj.name)
    display_powerup.short_description = 'Power-up'


@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ['display_difficulty', 'name', 'distance', 'wall_status', 'target_count', 'score_multiplier', 'coin_multiplier']
    list_filter = ['difficulty_id', 'wall_enabled']
    search_fields = ['name', 'description']
    ordering = ['order', 'difficulty_id']
    
    fieldsets = (
        ('Informations', {
            'fields': ('difficulty_id', 'name', 'description', 'emoji')
        }),
        ('Configuration du Gardien', {
            'fields': ('goalkeeper_speed', 'goalkeeper_size')
        }),
        ('Configuration du Jeu', {
            'fields': ('distance', 'wall_enabled', 'wall_players', 'wall_jump_probability')
        }),
        ('Cibles', {
            'fields': ('target_count', 'target_size')
        }),
        ('Multiplicateurs', {
            'fields': ('score_multiplier', 'coin_multiplier')
        }),
        ('Visuel', {
            'fields': ('background_color',)
        }),
        ('Ordre', {
            'fields': ('order',)
        })
    )
    
    def display_difficulty(self, obj):
        return format_html('{} {}', obj.emoji, obj.name)
    display_difficulty.short_description = 'Difficulté'
    
    def wall_status(self, obj):
        if obj.wall_enabled:
            return format_html(
                '<span style="color: green;">✓ {} joueurs</span>',
                obj.wall_players
            )
        return format_html('<span style="color: red;">✗</span>')
    wall_status.short_description = 'Mur'


@admin.register(UserProfileFoot)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'level', 'display_currency', 'total_goals', 'total_games', 'win_rate', 'best_score']
    list_filter = ['level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'win_rate']
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user',)
        }),
        ('Monnaie', {
            'fields': ('coins', 'gems')
        }),
        ('Progression', {
            'fields': ('level', 'experience')
        }),
        ('Équipement Sélectionné', {
            'fields': ('selected_character', 'selected_ball_skin', 'selected_player_skin')
        }),
        ('Statistiques', {
            'fields': ('total_goals', 'total_games', 'best_score', 'total_targets_hit', 'win_rate'),
            'classes': ('collapse',)
        }),
        ('Achievements', {
            'fields': ('achievements',),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('last_daily_bonus', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def display_currency(self, obj):
        return format_html(
            '<span style="margin-right: 10px;">🪙 {}</span>'
            '<span>💎 {}</span>',
            obj.coins, obj.gems
        )
    display_currency.short_description = 'Monnaie'
    
    actions = ['add_coins', 'add_gems', 'reset_daily_bonus']
    
    def add_coins(self, request, queryset):
        for profile in queryset:
            profile.coins += 100
            profile.save()
        self.message_user(request, f"100 pièces ajoutées à {queryset.count()} profil(s)")
    add_coins.short_description = "Ajouter 100 pièces"
    
    def add_gems(self, request, queryset):
        for profile in queryset:
            profile.gems += 10
            profile.save()
        self.message_user(request, f"10 gemmes ajoutées à {queryset.count()} profil(s)")
    add_gems.short_description = "Ajouter 10 gemmes"
    
    def reset_daily_bonus(self, request, queryset):
        queryset.update(last_daily_bonus=None)
        self.message_user(request, f"Bonus quotidien réinitialisé pour {queryset.count()} profil(s)")
    reset_daily_bonus.short_description = "Réinitialiser bonus quotidien"


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'display_item', 'price', 'currency', 'purchased_at']
    list_filter = ['currency', 'purchased_at']
    search_fields = ['user__username']
    date_hierarchy = 'purchased_at'
    readonly_fields = ['purchased_at']
    
    def display_item(self, obj):
        item = obj.character or obj.ball_skin or obj.player_skin or obj.powerup
        if item:
            emoji = getattr(item, 'emoji', '')
            return format_html('{} {}', emoji, item.name)
        return '-'
    display_item.short_description = 'Article'
    
    def has_add_permission(self, request):
        return False  # Disable manual creation


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ['player', 'score', 'difficulty', 'character', 'accuracy_display', 'coins_earned', 'date']
    list_filter = ['difficulty', 'date']
    search_fields = ['player__username']
    date_hierarchy = 'date'
    readonly_fields = ['date', 'accuracy']
    
    fieldsets = (
        ('Joueur et Partie', {
            'fields': ('player', 'character', 'difficulty', 'date')
        }),
        ('Résultats', {
            'fields': ('score', 'coins_earned', 'exp_earned')
        }),
        ('Statistiques', {
            'fields': ('total_shots', 'successful_shots', 'targets_hit', 'perfect_shots', 'max_combo', 'accuracy')
        }),
        ('Power-ups', {
            'fields': ('powerups_used',),
            'classes': ('collapse',)
        })
    )
    
    def accuracy_display(self, obj):
        accuracy = obj.accuracy
        color = '#4CAF50' if accuracy >= 80 else '#FFC107' if accuracy >= 50 else '#F44336'
        return format_html(
            '<span style="background: {}; color: white; padding: 2px 6px; border-radius: 3px;">{}%</span>',
            color, accuracy
        )
    accuracy_display.short_description = 'Précision'
    
    def has_add_permission(self, request):
        return False


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'period', 'rank', 'score', 'games_played', 'reward_claimed', 'period_dates']
    list_filter = ['period', 'reward_claimed', 'period_start']
    search_fields = ['user__username']
    ordering = ['period', 'rank']
    
    def period_dates(self, obj):
        return format_html(
            '{} → {}',
            obj.period_start.strftime('%d/%m'),
            obj.period_end.strftime('%d/%m')
        )
    period_dates.short_description = 'Période'
    
    actions = ['claim_rewards']
    
    def claim_rewards(self, request, queryset):
        for entry in queryset.filter(reward_claimed=False):
            # Award rewards based on rank
            profile = entry.user.game_profile
            if entry.rank == 1:
                profile.gems += 100
            elif entry.rank <= 3:
                profile.gems += 50
            elif entry.rank <= 10:
                profile.gems += 25
            elif entry.rank <= 50:
                profile.coins += 500
            elif entry.rank <= 100:
                profile.coins += 200
            else:
                profile.coins += 50
            
            profile.save()
            entry.reward_claimed = True
            entry.save()
        
        self.message_user(request, f"Récompenses distribuées pour {queryset.count()} entrée(s)")
    claim_rewards.short_description = "Distribuer les récompenses"


# Dashboard personnalisé
class GameStats:
    """Custom dashboard for game statistics"""
    pass

# Register custom admin views here if needed