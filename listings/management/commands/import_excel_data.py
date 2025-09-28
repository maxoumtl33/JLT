# management/commands/import_excel_data.py
"""
Script d'importation des données Excel pour le système de gestion de recettes
Usage: python manage.py import_excel_data chemin_vers_fichier.xlsx
"""

import pandas as pd
import re
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from listings.models import (
    UniteMesure, Departement, Fournisseur, Ingredient,
    Recette, SousRecette, RecetteIngredient, SousRecetteIngredient
)


class Command(BaseCommand):
    help = 'Importe les données depuis un fichier Excel'

    def add_arguments(self, parser):
        parser.add_argument(
            'excel_file',
            type=str,
            help='Chemin vers le fichier Excel à importer'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Effacer toutes les données existantes avant l\'import'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Exécuter en mode simulation sans sauvegarder'
        )

    def handle(self, *args, **options):
        self.excel_file = options['excel_file']
        self.clear_data = options.get('clear', False)
        self.dry_run = options.get('dry_run', False)
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('🔍 MODE SIMULATION - Aucune donnée ne sera sauvegardée'))
        
        try:
            # Charger le fichier Excel
            self.stdout.write(f'📂 Chargement du fichier: {self.excel_file}')
            self.excel_data = pd.ExcelFile(self.excel_file)
            
            # Afficher les feuilles disponibles
            self.stdout.write('\n📋 Feuilles disponibles:')
            for sheet in self.excel_data.sheet_names:
                self.stdout.write(f'  - {sheet}')
            
            # Traiter les données
            with transaction.atomic():
                # 1. Créer les unités de mesure de base
                self.create_unites_mesure()
                
                # 2. Créer les départements depuis les feuilles
                self.create_departements()
                
                # 3. Créer un fournisseur par défaut
                self.create_fournisseur_default()
                
                # 4. Traiter chaque feuille de recettes
                for sheet_name in self.excel_data.sheet_names:
                    self.process_sheet(sheet_name)
                
                if self.dry_run:
                    self.stdout.write(self.style.WARNING('\n🚫 Transaction annulée (mode simulation)'))
                    transaction.set_rollback(True)
                else:
                    self.stdout.write(self.style.SUCCESS('\n✅ Import terminé avec succès!'))
                    self.print_summary()
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\n❌ Erreur lors de l\'import: {str(e)}'))
            raise

    def create_unites_mesure(self):
        """Créer les unités de mesure de base"""
        self.stdout.write('\n📏 Création des unités de mesure...')
        
        unites = [
            ('Gramme', 'g'),
            ('Kilogramme', 'kg'),
            ('Millilitre', 'ml'),
            ('Litre', 'L'),
            ('Unité', 'un'),
            ('Cuillère à soupe', 'c.s.'),
            ('Cuillère à café', 'c.c.'),
            ('Tasse', 'tasse'),
            ('Feuille', 'feuille'),
            ('Tranche', 'tranche'),
            ('Portion', 'portion'),
        ]
        
        for nom, symbole in unites:
            if not self.dry_run:
                unite, created = UniteMesure.objects.get_or_create(
                    symbole=symbole.upper(),
                    defaults={'nom': nom}
                )
                if created:
                    self.stdout.write(f'  ✅ {nom} ({symbole})')
            else:
                self.stdout.write(f'  [SIMULATION] {nom} ({symbole})')
        
        # Créer un mapping pour faciliter la conversion
        self.unite_mapping = {
            'G': 'g', 'GR': 'g', 'GRAMME': 'g', 'GRAMMES': 'g',
            'KG': 'kg', 'KILO': 'kg', 'KILOGRAMME': 'kg',
            'ML': 'ml', 'MILLILITRE': 'ml',
            'L': 'L', 'LITRE': 'L', 'LITRES': 'L',
            'UN': 'un', 'UNITÉ': 'un', 'UNITE': 'un', 'PCS': 'un',
            'C.S.': 'c.s.', 'CS': 'c.s.', 'CUILLÈRE À SOUPE': 'c.s.',
            'C.C.': 'c.c.', 'CC': 'c.c.', 'CUILLÈRE À CAFÉ': 'c.c.',
            'TASSE': 'tasse', 'TASSES': 'tasse',
            'FEUILLE': 'feuille', 'FEUILLES': 'feuille',
            'TRANCHE': 'tranche', 'TRANCHES': 'tranche',
        }

    def create_departements(self):
        """Créer les départements depuis les noms des feuilles"""
        self.stdout.write('\n🏢 Création des départements...')
        
        # Mapping des noms de feuilles vers les départements
        departement_mapping = {
            'Salade': 'Salades',
            'BANQUETS': 'Banquets',
            'Soir': 'Service du soir',
            'Plateau à partager': 'Plateaux à partager',
            'SANDWICHS': 'Sandwichs',
            'PETIT DÉJEUNER': 'Petit-déjeuner',
            'BOL REPAS': 'Bols repas',
            'CANAPÉS': 'Canapés',
            'Menu Noel': 'Menus spéciaux',
            'Pâtisserie (ARCHIVE)': 'Pâtisserie',
        }
        
        for sheet_name in self.excel_data.sheet_names:
            dept_name = departement_mapping.get(sheet_name, sheet_name)
            if not self.dry_run:
                dept, created = Departement.objects.get_or_create(
                    nom=dept_name,
                    defaults={'description': f'Département {dept_name}'}
                )
                if created:
                    self.stdout.write(f'  ✅ {dept_name}')
            else:
                self.stdout.write(f'  [SIMULATION] {dept_name}')

    def create_fournisseur_default(self):
        """Créer un fournisseur par défaut pour les ingrédients"""
        self.stdout.write('\n🏪 Création du fournisseur par défaut...')
        
        if not self.dry_run:
            self.fournisseur_default, created = Fournisseur.objects.get_or_create(
                nom='Fournisseur Général',
                defaults={
                    'email': 'contact@fournisseur.com',
                    'telephone': '514-000-0000',
                    'adresse': 'À définir',
                    'contact_principal': 'À définir'
                }
            )
            if created:
                self.stdout.write('  ✅ Fournisseur Général créé')
        else:
            self.stdout.write('  [SIMULATION] Fournisseur Général')

    def normalize_unite(self, unite_str):
        """Normalise une unité de mesure"""
        if pd.isna(unite_str):
            return 'un'
        
        unite_str = str(unite_str).strip().upper()
        
        # Chercher dans le mapping
        for key, value in self.unite_mapping.items():
            if unite_str == key:
                return value
        
        # Si non trouvé, retourner 'un' par défaut
        return 'un'

    def parse_quantite(self, quantite_str):
        """Parse une quantité depuis une chaîne"""
        if pd.isna(quantite_str):
            return Decimal('1')
        
        # Nettoyer la chaîne
        quantite_str = str(quantite_str).strip()
        
        # Remplacer les virgules par des points
        quantite_str = quantite_str.replace(',', '.')
        quantite_str = quantite_str.replace(' ', '')
        
        # Essayer de convertir en Decimal
        try:
            # Gérer les fractions simples
            if '/' in quantite_str:
                parts = quantite_str.split('/')
                if len(parts) == 2:
                    return Decimal(parts[0]) / Decimal(parts[1])
            
            return Decimal(quantite_str)
        except:
            # Si échec, retourner 1
            return Decimal('1')

    def process_sheet(self, sheet_name):
        """Traiter une feuille de recettes"""
        self.stdout.write(f'\n📄 Traitement de la feuille: {sheet_name}')
        
        # Lire la feuille
        df = pd.read_excel(self.excel_file, sheet_name=sheet_name)
        
        # Nettoyer les noms de colonnes
        df.columns = [str(col).strip() for col in df.columns]
        
        # Identifier les colonnes importantes
        col_mapping = self.identify_columns(df.columns)
        
        if not col_mapping:
            self.stdout.write(self.style.WARNING(f'  ⚠️ Colonnes non reconnues, feuille ignorée'))
            return
        
        # Obtenir le département
        dept_mapping = {
            'Salade': 'Salades',
            'BANQUETS': 'Banquets',
            'Soir': 'Service du soir',
            'Plateau à partager': 'Plateaux à partager',
            'SANDWICHS': 'Sandwichs',
            'PETIT DÉJEUNER': 'Petit-déjeuner',
            'BOL REPAS': 'Bols repas',
            'CANAPÉS': 'Canapés',
            'Menu Noel': 'Menus spéciaux',
            'Pâtisserie (ARCHIVE)': 'Pâtisserie',
        }
        
        departement_nom = dept_mapping.get(sheet_name, sheet_name)
        if not self.dry_run:
            departement = Departement.objects.get(nom=departement_nom)
        else:
            departement = None
        
        # Traiter les recettes
        current_recette = None
        recette_count = 0
        ingredient_count = 0
        
        for index, row in df.iterrows():
            # Vérifier si c'est une nouvelle recette
            if pd.notna(row.get(col_mapping['id'])) and pd.notna(row.get(col_mapping['nom'])):
                # Créer la nouvelle recette
                nom_recette = str(row[col_mapping['nom']]).strip()
                
                if not self.dry_run:
                    current_recette, created = Recette.objects.get_or_create(
                        nom=nom_recette,
                        defaults={
                            'description': f'Recette importée depuis {sheet_name}',
                            'explication_fabrication': str(row.get(col_mapping.get('preparation', ''), '')),
                            'departement': departement,
                            'portions': self.parse_portions(row.get(col_mapping.get('portions', '1'))),
                        }
                    )
                    if created:
                        recette_count += 1
                else:
                    self.stdout.write(f'  [SIMULATION] Recette: {nom_recette}')
                    recette_count += 1
            
            # Traiter l'ingrédient de cette ligne
            if pd.notna(row.get(col_mapping.get('ingredient'))) and current_recette:
                nom_ingredient = str(row[col_mapping['ingredient']]).strip()
                quantite = self.parse_quantite(row.get(col_mapping.get('quantite', '1')))
                unite_str = row.get(col_mapping.get('unite', 'un'))
                unite_symbole = self.normalize_unite(unite_str)
                
                if not self.dry_run:
                    # Obtenir l'unité de mesure
                    unite = UniteMesure.objects.get(symbole__iexact=unite_symbole)
                    
                    # Créer ou récupérer l'ingrédient
                    ingredient, created = Ingredient.objects.get_or_create(
                        nom=nom_ingredient,
                        defaults={
                            'unite_mesure': unite,
                            'stock_reel': Decimal('0'),
                            'stock_alerte': Decimal('10'),
                            'description': ''
                        }
                    )
                    
                    # Créer la relation recette-ingrédient
                    RecetteIngredient.objects.get_or_create(
                        recette=current_recette,
                        ingredient=ingredient,
                        defaults={'quantite': quantite}
                    )
                    
                    if created:
                        ingredient_count += 1
                        # Créer une entrée dans le catalogue fournisseur
                        from listings.models import CatalogueFournisseur
                        CatalogueFournisseur.objects.get_or_create(
                            fournisseur=self.fournisseur_default,
                            ingredient=ingredient,
                            defaults={
                                'prix': Decimal('10.00'),  # Prix par défaut
                                'date_debut': timezone.now().date(),
                                'conditionnement': f'1 {unite.symbole}',
                                'delai_livraison': 2,
                                'actif': True
                            }
                        )
                else:
                    ingredient_count += 1
        
        self.stdout.write(f'  ✅ {recette_count} recettes, {ingredient_count} ingrédients traités')

    def identify_columns(self, columns):
        """Identifier les colonnes importantes dans le DataFrame"""
        col_mapping = {}
        
        # Patterns pour identifier les colonnes
        patterns = {
            'id': r'id.*recette',
            'nom': r'nom.*recette',
            'departement': r'département|departement|section',
            'ingredient': r'ingrédient|ingredient|items',
            'quantite': r'quantité|quantite|qty',
            'unite': r'poids|vol|un\.|unite|mesure',
            'preparation': r'préparation|preparation|étapes',
            'portions': r'portions?',
        }
        
        for col in columns:
            col_lower = str(col).lower()
            for key, pattern in patterns.items():
                if re.search(pattern, col_lower):
                    col_mapping[key] = col
                    break
        
        # Vérifier qu'on a au moins les colonnes minimales
        if 'ingredient' in col_mapping:
            return col_mapping
        
        return None

    def parse_portions(self, portions_str):
        """Extraire le nombre de portions depuis une chaîne"""
        if pd.isna(portions_str):
            return 1
        
        portions_str = str(portions_str)
        
        # Chercher un nombre dans la chaîne
        import re
        numbers = re.findall(r'\d+', portions_str)
        
        if numbers:
            return int(numbers[0])
        
        return 1

    def print_summary(self):
        """Afficher un résumé de l'import"""
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('📊 RÉSUMÉ DE L\'IMPORT')
        self.stdout.write('=' * 50)
        
        if not self.dry_run:
            from listings.models import (
                UniteMesure, Departement, Ingredient, 
                Recette, RecetteIngredient
            )
            
            self.stdout.write(f'  • Unités de mesure: {UniteMesure.objects.count()}')
            self.stdout.write(f'  • Départements: {Departement.objects.count()}')
            self.stdout.write(f'  • Ingrédients: {Ingredient.objects.count()}')
            self.stdout.write(f'  • Recettes: {Recette.objects.count()}')
            self.stdout.write(f'  • Relations recette-ingrédient: {RecetteIngredient.objects.count()}')
            
            # Afficher quelques exemples
            self.stdout.write('\n📝 Exemples de recettes importées:')
            for recette in Recette.objects.all()[:5]:
                nb_ingredients = recette.recette_ingredients.count()
                self.stdout.write(f'  • {recette.nom} ({nb_ingredients} ingrédients)')
        
        self.stdout.write('=' * 50)