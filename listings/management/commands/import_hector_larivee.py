# management/commands/import_hector_larivee.py
"""
Script d'importation spécifique pour les fichiers du fournisseur Hector Larivée
Usage: python manage.py import_hector_larivee "Liste prix Price list.xlsx"
"""

import pandas as pd
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone
from listings.models import (
    UniteMesure, Fournisseur, Ingredient, CatalogueFournisseur
)


class Command(BaseCommand):
    help = 'Importe le catalogue du fournisseur Hector Larivée'
    
    def add_arguments(self, parser):
        parser.add_argument(
            'fichier',
            type=str,
            help='Chemin vers le fichier Excel du fournisseur'
        )
        parser.add_argument(
            '--date-debut',
            type=str,
            default=None,
            help='Date de début de validité (YYYY-MM-DD). Par défaut: aujourd\'hui'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Mode simulation - affiche ce qui sera importé sans sauvegarder'
        )

    def handle(self, *args, **options):
        self.fichier = options['fichier']
        self.dry_run = options.get('dry_run', False)
        
        # Date de début
        if options.get('date_debut'):
            from datetime import datetime
            self.date_debut = datetime.strptime(options['date_debut'], '%Y-%m-%d').date()
        else:
            self.date_debut = timezone.now().date()
        
        if self.dry_run:
            self.stdout.write(self.style.WARNING('🔍 MODE SIMULATION - Aucune donnée ne sera sauvegardée'))
        
        try:
            self.import_catalogue()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Erreur: {str(e)}'))
            raise
    
    def import_catalogue(self):
        """Importer le catalogue Hector Larivée"""
        
        self.stdout.write(f'📂 Lecture du fichier: {self.fichier}')
        
        # Lire le fichier Excel
        # Les vraies données commencent à la ligne 3 (index 2)
        df = pd.read_excel(self.fichier, header=2)
        
        # Renommer les colonnes pour correspondre à notre format
        df.columns = ['code_produit', 'description', 'format', 'provenance', 'prix']
        
        # Nettoyer les données
        df = df[df['code_produit'].notna()]  # Enlever les lignes vides
        df = df[~df['code_produit'].astype(str).str.contains('produit', case=False)]  # Enlever la ligne d'en-tête si présente
        
        self.stdout.write(f'📊 {len(df)} produits trouvés dans le fichier')
        
        # Créer ou récupérer le fournisseur
        if not self.dry_run:
            fournisseur, created = Fournisseur.objects.get_or_create(
                nom='Hector Larivée',
                defaults={
                    'email': 'commandes@hectorlarivee.com',
                    'telephone': '514-000-0000',
                    'adresse': 'Montréal, QC',
                    'contact_principal': 'Service commercial'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS('✅ Fournisseur Hector Larivée créé'))
            else:
                self.stdout.write('ℹ️ Fournisseur Hector Larivée existant')
        
        # Créer les unités de mesure nécessaires
        self.create_unites()
        
        # Statistiques
        ingredients_crees = 0
        ingredients_mis_a_jour = 0
        prix_ajoutes = 0
        prix_desactives = 0
        erreurs = []
        
        with transaction.atomic():
            for index, row in df.iterrows():
                try:
                    # Extraire les données
                    code_produit = str(row['code_produit']).strip()
                    description = str(row['description']).strip()
                    format_produit = str(row['format']).strip() if pd.notna(row['format']) else ''
                    prix = Decimal(str(row['prix']).replace(',', '.'))
                    
                    # Normaliser le nom de l'ingrédient
                    nom_ingredient = self.normaliser_nom(description)
                    
                    # Déterminer l'unité depuis le format
                    unite = self.extraire_unite(format_produit)
                    
                    if not self.dry_run:
                        # Créer ou récupérer l'ingrédient
                        ingredient, created = Ingredient.objects.get_or_create(
                            nom__iexact=nom_ingredient,
                            defaults={
                                'nom': nom_ingredient,
                                'unite_mesure': unite,
                                'stock_reel': Decimal('0'),
                                'stock_alerte': Decimal('10'),
                                'description': f'Code fournisseur: {code_produit}'
                            }
                        )
                        
                        if created:
                            ingredients_crees += 1
                        else:
                            # Mettre à jour la description avec le code si nécessaire
                            if code_produit not in (ingredient.description or ''):
                                ingredient.description = f'{ingredient.description or ""} | Code: {code_produit}'.strip(' |')
                                ingredient.save()
                            ingredients_mis_a_jour += 1
                        
                        # Désactiver les anciens prix
                        anciens = CatalogueFournisseur.objects.filter(
                            fournisseur=fournisseur,
                            ingredient=ingredient,
                            actif=True
                        )
                        nb_desactives = anciens.update(
                            actif=False,
                            date_fin=self.date_debut
                        )
                        prix_desactives += nb_desactives
                        
                        # Créer le nouveau prix
                        CatalogueFournisseur.objects.create(
                            fournisseur=fournisseur,
                            ingredient=ingredient,
                            prix=prix,
                            date_debut=self.date_debut,
                            reference_fournisseur=code_produit,
                            conditionnement=format_produit,
                            actif=True,
                            delai_livraison=2
                        )
                        prix_ajoutes += 1
                    else:
                        # Mode simulation
                        self.stdout.write(
                            f'  [SIM] {nom_ingredient} - {prix}$ - {format_produit}'
                        )
                        
                except Exception as e:
                    erreurs.append(f"Ligne {index + 4}: {str(e)}")  # +4 car on commence à la ligne 3
                    continue
            
            if self.dry_run:
                self.stdout.write(self.style.WARNING('\n🚫 Transaction annulée (mode simulation)'))
                transaction.set_rollback(True)
        
        # Afficher le résumé
        self.stdout.write('\n' + '=' * 50)
        self.stdout.write('📊 RÉSUMÉ DE L\'IMPORT')
        self.stdout.write('=' * 50)
        
        if not self.dry_run:
            self.stdout.write(f'✅ {ingredients_crees} nouveaux ingrédients créés')
            self.stdout.write(f'🔄 {ingredients_mis_a_jour} ingrédients existants mis à jour')
            self.stdout.write(f'💰 {prix_ajoutes} nouveaux prix ajoutés')
            self.stdout.write(f'🔒 {prix_desactives} anciens prix désactivés')
        else:
            self.stdout.write(f'📝 {len(df)} lignes analysées')
        
        if erreurs:
            self.stdout.write(self.style.ERROR(f'\n⚠️ {len(erreurs)} erreurs:'))
            for err in erreurs[:10]:
                self.stdout.write(f'  • {err}')
        
        self.stdout.write('=' * 50)
    
    def create_unites(self):
        """Créer les unités de mesure nécessaires"""
        if self.dry_run:
            return
        
        unites = [
            ('Unité', 'UN'),
            ('Caisse', 'CS'),
            ('Boîte', 'BTE'),
            ('Paquet', 'PQT'),
            ('Kilogramme', 'KG'),
            ('Gramme', 'G'),
            ('Litre', 'L'),
            ('Millilitre', 'ML'),
        ]
        
        for nom, symbole in unites:
            UniteMesure.objects.get_or_create(
                symbole=symbole,
                defaults={'nom': nom}
            )
    
    def normaliser_nom(self, description):
        """Normaliser le nom d'un ingrédient"""
        # Enlever les codes et numéros au début
        nom = description
        
        # Enlever les dimensions (ex: 19x13x10)
        nom = re.sub(r'\d+x\d+(?:x\d+)?', '', nom)
        
        # Enlever les codes comme 275C
        nom = re.sub(r'\b\d+[A-Z]\b', '', nom)
        
        # Capitaliser correctement
        nom = nom.strip().title()
        
        # Corrections spécifiques
        remplacements = {
            'Boite': 'Boîte',
            'Etiquette': 'Étiquette',
            'Temperature': 'Température',
            'Enregistreur De': 'Enregistreur de',
        }
        
        for ancien, nouveau in remplacements.items():
            nom = nom.replace(ancien, nouveau)
        
        return nom.strip()
    
    def extraire_unite(self, format_str):
        """Extraire l'unité de mesure depuis le format"""
        if self.dry_run:
            return None
        
        format_upper = format_str.upper()
        
        # Mapping des formats vers les unités
        if 'CS' in format_upper or 'CAISSE' in format_upper:
            return UniteMesure.objects.get(symbole='CS')
        elif 'KG' in format_upper:
            return UniteMesure.objects.get(symbole='KG')
        elif 'G' in format_upper and 'KG' not in format_upper:
            return UniteMesure.objects.get(symbole='G')
        elif 'L' in format_upper and 'ML' not in format_upper:
            return UniteMesure.objects.get(symbole='L')
        elif 'ML' in format_upper:
            return UniteMesure.objects.get(symbole='ML')
        elif 'BTE' in format_upper or 'BOITE' in format_upper:
            return UniteMesure.objects.get(symbole='BTE')
        else:
            return UniteMesure.objects.get(symbole='UN')


# Script alternatif pour utilisation directe dans le shell
def import_hector_quick(file_path, dry_run=False):
    """
    Import rapide pour le shell Django
    
    Usage:
        from listings.management.commands.import_hector_larivee import import_hector_quick
        import_hector_quick('Liste prix Price list.xlsx')
    """
    import re
    
    print(f"📂 Lecture du fichier: {file_path}")
    
    # Lire le fichier
    df = pd.read_excel(file_path, header=2)
    df.columns = ['code_produit', 'description', 'format', 'provenance', 'prix']
    df = df[df['code_produit'].notna()]
    
    print(f"📊 {len(df)} produits trouvés")
    
    if dry_run:
        print("\n🔍 MODE SIMULATION - Aperçu des 10 premiers produits:")
        for _, row in df.head(10).iterrows():
            print(f"  • {row['description']} - {row['prix']}$ ({row['format']})")
        return
    
    # Créer le fournisseur
    fournisseur, _ = Fournisseur.objects.get_or_create(
        nom='Hector Larivée',
        defaults={
            'email': 'commandes@hectorlarivee.com',
            'telephone': '514-000-0000'
        }
    )
    
    # Créer l'unité par défaut
    unite_default, _ = UniteMesure.objects.get_or_create(
        symbole='UN',
        defaults={'nom': 'Unité'}
    )
    
    created = 0
    updated = 0
    
    with transaction.atomic():
        for _, row in df.iterrows():
            try:
                # Nettoyer le nom
                nom = str(row['description']).strip().title()
                prix = Decimal(str(row['prix']))
                code = str(row['code_produit']).strip()
                
                # Créer ou mettre à jour l'ingrédient
                ingredient, is_new = Ingredient.objects.get_or_create(
                    nom__iexact=nom,
                    defaults={
                        'nom': nom,
                        'unite_mesure': unite_default,
                        'stock_reel': Decimal('0'),
                        'stock_alerte': Decimal('10')
                    }
                )
                
                if is_new:
                    created += 1
                else:
                    updated += 1
                
                # Désactiver les anciens prix
                CatalogueFournisseur.objects.filter(
                    fournisseur=fournisseur,
                    ingredient=ingredient,
                    actif=True
                ).update(actif=False)
                
                # Créer le nouveau prix
                CatalogueFournisseur.objects.create(
                    fournisseur=fournisseur,
                    ingredient=ingredient,
                    prix=prix,
                    reference_fournisseur=code,
                    conditionnement=str(row.get('format', '')),
                    actif=True
                )
                
            except Exception as e:
                print(f"  ⚠️ Erreur: {e}")
    
    print(f"\n✅ Import terminé!")
    print(f"  • {created} ingrédients créés")
    print(f"  • {updated} ingrédients mis à jour")
    print(f"  • {len(df)} prix importés")
    
    return created, updated