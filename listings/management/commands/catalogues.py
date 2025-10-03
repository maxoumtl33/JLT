"""
Commande Django pour générer les catalogues fournisseurs
Fichier: listings/management/commands/catalogues.py
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from datetime import datetime
import random

# Import your models - adjust based on your actual model locations
from listings.models import Ingredient, Fournisseur, CatalogueFournisseur, UniteMesure


class Command(BaseCommand):
    help = 'Génère les catalogues fournisseurs automatiquement'

    def add_arguments(self, parser):
        parser.add_argument(
            '--fournisseur',
            type=str,
            help='Nom du fournisseur spécifique (optionnel)',
        )
        parser.add_argument(
            '--action',
            type=str,
            default='create',
            choices=['create', 'list', 'reset'],
            help='Action à effectuer: create (créer catalogues), list (lister), reset (réinitialiser)',
        )

    def handle(self, *args, **options):
        action = options['action']
        
        if action == 'create':
            self.create_catalogues(options)
        elif action == 'list':
            self.list_catalogues(options)
        elif action == 'reset':
            self.reset_catalogues(options)

    def categorize_ingredient(self, ingredient_name):
        """Catégorise un ingrédient basé sur son nom."""
        ingredient_lower = ingredient_name.lower()
        
        # Définir les mots-clés pour chaque catégorie
        categories = {
            'Fruits': ['pomme', 'poire', 'orange', 'citron', 'lime', 'banane', 'fraise', 'framboise', 
                      'bleuet', 'mûre', 'cerise', 'pêche', 'abricot', 'prune', 'raisin', 'mangue', 
                      'ananas', 'melon', 'kiwi', 'fruit', 'canneberge', 'coulis'],
            'Légumes': ['tomate', 'concombre', 'carotte', 'céleri', 'oignon', 'ail', 'poivron', 'brocoli', 
                       'chou', 'laitue', 'épinard', 'haricot', 'pois', 'maïs', 'pomme de terre', 'patate', 
                       'courge', 'zucchini', 'aubergine', 'radis', 'navet', 'betterave', 'fenouil', 
                       'asperge', 'artichaut', 'poireau', 'légume', 'champignon', 'endive'],
            'Viandes': ['bœuf', 'boeuf', 'porc', 'veau', 'agneau', 'poulet', 'dinde', 'canard', 'lapin', 
                       'viande', 'bacon', 'jambon', 'saucisse', 'foie', 'steak', 'filet', 'rôti', 
                       'pancetta', 'longe', 'escalope', 'haché', 'effiloché'],
            'Poissons': ['saumon', 'truite', 'thon', 'morue', 'sole', 'bar', 'dorade', 'crevette', 
                        'homard', 'crabe', 'huître', 'moule', 'calamar', 'pétoncle', 'poisson', 
                        'fruits de mer', 'anchois', 'sardine'],
            'Laitiers': ['lait', 'crème', 'fromage', 'yogourt', 'yaourt', 'beurre', 'mascarpone', 
                        'ricotta', 'mozzarella', 'parmesan', 'cheddar', 'gruyère', 'philadelphia', 
                        'cottage', 'feta'],
            'Épices': ['sel', 'poivre', 'thym', 'romarin', 'basilic', 'origan', 'persil', 'coriandre', 
                      'aneth', 'menthe', 'sauge', 'laurier', 'cannelle', 'muscade', 'cumin', 'paprika', 
                      'curry', 'curcuma', 'gingembre', 'épice', 'herbe'],
            'Pâtisserie': ['farine', 'sucre', 'levure', 'cacao', 'chocolat', 'vanille', 'brioche', 
                          'pain', 'baguette', 'cake', 'gâteau', 'biscuit', 'croissant', 'pâte', 
                          'tarte', 'fondant'],
            'Huiles': ['huile', 'vinaigre'],
            'Sauces': ['sauce', 'mayo', 'moutarde', 'ketchup', 'aïoli', 'pesto', 'salsa'],
            'Noix': ['amande', 'noix', 'noisette', 'pistache', 'graine', 'sésame'],
            'Pâtes': ['pâte', 'riz', 'quinoa', 'couscous', 'avoine']
        }
        
        for category, keywords in categories.items():
            if any(keyword in ingredient_lower for keyword in keywords):
                return category
        
        return 'Autres'

    def get_suppliers_for_category(self, category):
        """Retourne les fournisseurs appropriés pour une catégorie."""
        mapping = {
            'Fruits': ['Can-Am', 'J-G fruit et légumes', 'Hector Larivée'],
            'Légumes': ['Can-Am', 'J-G fruit et légumes', 'Hector Larivée'],
            'Viandes': ['Gordon GFS', 'Maison du rôti', 'Can-Am'],
            'Poissons': ['Vaskin', 'Gordon GFS', 'Noreff'],
            'Laitiers': ['Gordon GFS', 'Sysco', 'Hector Larivée'],
            'Épices': ['Gordon GFS', 'Sysco'],
            'Pâtisserie': ['Hector Larivée', 'Gordon GFS'],
            'Huiles': ['Gordon GFS', 'Sysco', 'Aubut'],
            'Sauces': ['Gordon GFS', 'Sysco'],
            'Noix': ['Gordon GFS', 'Aubut'],
            'Pâtes': ['Gordon GFS', 'Sysco', 'Aubut'],
            'Autres': ['Gordon GFS', 'Sysco']
        }
        return mapping.get(category, ['Gordon GFS', 'Sysco'])

    def generate_price(self, category):
        """Génère un prix réaliste basé sur la catégorie."""
        price_ranges = {
            'Fruits': (2.99, 8.99),
            'Légumes': (1.99, 6.99),
            'Viandes': (8.99, 39.99),
            'Poissons': (12.99, 49.99),
            'Laitiers': (3.99, 14.99),
            'Épices': (2.99, 9.99),
            'Pâtisserie': (1.99, 12.99),
            'Huiles': (4.99, 19.99),
            'Sauces': (2.99, 9.99),
            'Noix': (5.99, 24.99),
            'Pâtes': (2.99, 8.99),
            'Autres': (3.99, 15.99)
        }
        min_price, max_price = price_ranges.get(category, (5.00, 20.00))
        return round(random.uniform(min_price, max_price), 2)

    def create_catalogues(self, options):
        """Crée les catalogues pour tous les ingrédients."""
        self.stdout.write(self.style.SUCCESS('\n🚀 Début de la création des catalogues...'))
        self.stdout.write('-' * 60)
        
        # Créer les fournisseurs de base (structure simplifiée)
        fournisseurs_data = [
            ('Can-Am', '514-655-0355'),
            ('Gordon GFS', '438-332-0343'),
            ('Hector Larivée', '514-521-8331'),
            ('J-G fruit et légumes', '514-792-9987'),
            ('Sysco', '514-531-6717'),
            ('Vaskin', '438-401-5938'),
            ('Maison du rôti', '514-521-2448'),
            ('Noreff', '514-803-9390'),
            ('Marché PA', '514-000-0001'),
            ('H-Mart', '514-000-0002'),
            ('Aubut', '514-000-0003'),
            ('Carrousel', '450-655-2025'),
            ('ABCembaluxe', '514-808-5176')
        ]
        
        self.stdout.write(self.style.MIGRATE_HEADING('📦 Création des fournisseurs...'))
        
        for nom, telephone in fournisseurs_data:
            # Créer le fournisseur avec les champs minimaux requis
            defaults = {'nom': nom}
            
            # Ajouter les champs optionnels s'ils existent dans le modèle
            try:
                # Tenter d'ajouter le téléphone si le champ existe
                test_fournisseur = Fournisseur()
                if hasattr(test_fournisseur, 'telephone'):
                    defaults['telephone'] = telephone
                if hasattr(test_fournisseur, 'tel'):
                    defaults['tel'] = telephone
                if hasattr(test_fournisseur, 'phone'):
                    defaults['phone'] = telephone
                if hasattr(test_fournisseur, 'email'):
                    defaults['email'] = f"{nom.lower().replace(' ', '.')}@fournisseur.ca"
            except:
                pass
            
            # Utiliser uniquement le nom pour la recherche
            fournisseur, created = Fournisseur.objects.get_or_create(
                nom=nom,
                defaults=defaults
            )
            
            if created:
                self.stdout.write(f"  ✅ Créé: {nom}")
            else:
                self.stdout.write(f"  ℹ️  Existe: {nom}")
        
        self.stdout.write('-' * 60)
        
        # Traiter les ingrédients
        with transaction.atomic():
            ingredients = Ingredient.objects.all()
            total = ingredients.count()
            
            if total == 0:
                self.stdout.write(self.style.ERROR('❌ Aucun ingrédient trouvé dans la base de données'))
                return
            
            self.stdout.write(self.style.MIGRATE_HEADING(f'🔄 Traitement de {total} ingrédients...'))
            
            # Filtrer par fournisseur si spécifié
            target_fournisseur = options.get('fournisseur')
            if target_fournisseur:
                self.stdout.write(f"  Fournisseur ciblé: {target_fournisseur}")
            
            created_count = 0
            updated_count = 0
            skipped_count = 0
            
            for i, ingredient in enumerate(ingredients, 1):
                # Déterminer la catégorie
                category = self.categorize_ingredient(ingredient.nom)
                
                # Obtenir les fournisseurs pour cette catégorie
                supplier_names = self.get_suppliers_for_category(category)
                
                # Filtrer si un fournisseur spécifique est demandé
                if target_fournisseur:
                    if target_fournisseur not in supplier_names:
                        skipped_count += 1
                        continue
                    supplier_names = [target_fournisseur]
                
                # Créer les catalogues (limiter à 2 fournisseurs principaux par ingrédient)
                for supplier_name in supplier_names[:2]:
                    try:
                        fournisseur = Fournisseur.objects.get(nom=supplier_name)
                        
                        # Générer un prix
                        prix = self.generate_price(category)
                        
                        # Créer ou mettre à jour le catalogue
                        catalogue, created = CatalogueFournisseur.objects.update_or_create(
                            fournisseur=fournisseur,
                            ingredient=ingredient,
                            defaults={
                                'prix': Decimal(str(prix)),
                                'quantite_par_unite': Decimal('1'),
                                'date_debut': datetime.now().date(),
                                'actif': True,
                                'devise': 'CAD',
                                'reference_fournisseur': f"{supplier_name[:3].upper()}-{ingredient.id:04d}"
                            }
                        )
                        
                        # Ajouter l'unité si elle existe et si le champ existe dans le modèle
                        if hasattr(catalogue, 'unite'):
                            if hasattr(ingredient, 'unite_mesure') and ingredient.unite_mesure:
                                catalogue.unite = ingredient.unite_mesure
                            elif hasattr(ingredient, 'unite_achat') and ingredient.unite_achat:
                                catalogue.unite = ingredient.unite_achat
                            elif hasattr(ingredient, 'unite') and ingredient.unite:
                                catalogue.unite = ingredient.unite
                            try:
                                catalogue.save()
                            except:
                                pass
                        
                        if created:
                            created_count += 1
                        else:
                            updated_count += 1
                            
                    except Fournisseur.DoesNotExist:
                        self.stdout.write(self.style.WARNING(f"  ⚠️  Fournisseur non trouvé: {supplier_name}"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(f"  ❌ Erreur pour {ingredient.nom}: {str(e)}"))
                
                # Afficher la progression
                if i % 50 == 0 or i == total:
                    percent = (i / total) * 100
                    self.stdout.write(f"  Progression: {i}/{total} ({percent:.1f}%)")
            
            self.stdout.write('-' * 60)
            self.stdout.write(self.style.SUCCESS('✨ RÉSUMÉ:'))
            self.stdout.write(f"  • {created_count} catalogues créés")
            self.stdout.write(f"  • {updated_count} catalogues mis à jour")
            if skipped_count > 0:
                self.stdout.write(f"  • {skipped_count} ingrédients ignorés (fournisseur non correspondant)")
            
            # Afficher les statistiques par fournisseur
            self.stdout.write('-' * 60)
            self.stdout.write(self.style.MIGRATE_HEADING('📊 Statistiques par fournisseur:'))
            
            for fournisseur in Fournisseur.objects.all():
                count = CatalogueFournisseur.objects.filter(
                    fournisseur=fournisseur,
                    actif=True
                ).count()
                if count > 0:
                    self.stdout.write(f"  • {fournisseur.nom}: {count} produits")

    def list_catalogues(self, options):
        """Liste les catalogues existants."""
        self.stdout.write(self.style.SUCCESS('\n📋 Liste des catalogues actifs:'))
        self.stdout.write('-' * 60)
        
        target_fournisseur = options.get('fournisseur')
        
        queryset = CatalogueFournisseur.objects.filter(actif=True)
        if target_fournisseur:
            queryset = queryset.filter(fournisseur__nom=target_fournisseur)
        
        total = queryset.count()
        
        if total == 0:
            self.stdout.write(self.style.WARNING('Aucun catalogue actif trouvé'))
            return
        
        # Grouper par fournisseur
        fournisseurs = {}
        for catalogue in queryset.select_related('fournisseur', 'ingredient'):
            nom_fournisseur = catalogue.fournisseur.nom
            if nom_fournisseur not in fournisseurs:
                fournisseurs[nom_fournisseur] = []
            fournisseurs[nom_fournisseur].append(catalogue)
        
        for fournisseur_nom, catalogues in fournisseurs.items():
            self.stdout.write(f"\n{self.style.MIGRATE_HEADING(fournisseur_nom)} ({len(catalogues)} produits)")
            
            # Afficher les 5 premiers produits comme exemple
            for catalogue in catalogues[:5]:
                self.stdout.write(
                    f"  • {catalogue.ingredient.nom}: "
                    f"{catalogue.prix} {catalogue.devise} "
                    f"(Réf: {catalogue.reference_fournisseur or 'N/A'})"
                )
            if len(catalogues) > 5:
                self.stdout.write(f"  ... et {len(catalogues) - 5} autres produits")
        
        self.stdout.write('-' * 60)
        self.stdout.write(f"Total: {total} catalogues actifs")

    def reset_catalogues(self, options):
        """Réinitialise les catalogues (supprime tout)."""
        self.stdout.write(self.style.WARNING('\n⚠️  ATTENTION: Cette action va supprimer tous les catalogues!'))
        
        confirm = input("Êtes-vous sûr? Tapez 'OUI' pour confirmer: ")
        if confirm != 'OUI':
            self.stdout.write(self.style.ERROR('Opération annulée'))
            return
        
        target_fournisseur = options.get('fournisseur')
        
        if target_fournisseur:
            count = CatalogueFournisseur.objects.filter(
                fournisseur__nom=target_fournisseur
            ).delete()[0]
            self.stdout.write(self.style.SUCCESS(f'✅ {count} catalogues supprimés pour {target_fournisseur}'))
        else:
            count = CatalogueFournisseur.objects.all().delete()[0]
            self.stdout.write(self.style.SUCCESS(f'✅ {count} catalogues supprimés au total'))