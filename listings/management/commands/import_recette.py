"""
Commande Django pour importer les recettes depuis Excel
Usage: python manage.py import_recette
"""

import pandas as pd
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.db import transaction
from collections import defaultdict
from difflib import SequenceMatcher
from listings.models import (
    Recette, SousRecette, RecetteIngredient, 
    SousRecetteIngredient, Ingredient, UniteMesure, Departement
)

class Command(BaseCommand):
    help = 'Importe les recettes depuis les fichiers Excel'
    
    # Configuration des fichiers
    FICHIER_RECETTES = 'final recette.xlsx'
    FICHIER_INGREDIENTS_EXISTANTS = 'Uniteingredient.xlsx'
    
    # Liste des mots-clés pour identifier les sous-recettes
    MOTS_CLES_SOUS_RECETTES = [
        'vinaigrette', 'sauce', 'appareil', 'coulis', 'glaçage', 
        'crème', 'mayonnaise', 'émulsion', 'trempette', 'tahini', 
        'tzatziki', 'aïoli', 'pesto', 'chutney', 'salsa', 'houmous',
        'beurre blanc', 'réduction', 'marinade', 'laque'
    ]
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--recettes-file',
            type=str,
            default='final recette.xlsx',
            help='Chemin vers le fichier Excel des recettes'
        )
        parser.add_argument(
            '--ingredients-file',
            type=str,
            default='Uniteingredient.xlsx',
            help='Chemin vers le fichier Excel des ingrédients existants'
        )
        parser.add_argument(
            '--debug',
            action='store_true',
            help='Mode debug avec plus de détails'
        )
        parser.add_argument(
            '--similarity-threshold',
            type=float,
            default=0.85,
            help='Seuil de similarité pour la correspondance des ingrédients (0.0-1.0)'
        )
    
    def handle(self, *args, **options):
        self.FICHIER_RECETTES = options['recettes_file']
        self.FICHIER_INGREDIENTS_EXISTANTS = options['ingredients_file']
        self.debug = options.get('debug', False)
        self.similarity_threshold = options.get('similarity_threshold', 0.85)
        
        # Dictionnaire des ingrédients existants pour normalisation
        self.ingredients_normalises = {}
        
        self.stdout.write(self.style.SUCCESS('='*60))
        self.stdout.write(self.style.SUCCESS('IMPORTATION DES RECETTES DEPUIS EXCEL'))
        self.stdout.write(self.style.SUCCESS('='*60))
        
        # Charger et normaliser les ingrédients
        self.charger_et_normaliser_ingredients()
        
        # Importer les recettes
        self.importer_recettes_optimise()
        
        self.stdout.write(self.style.SUCCESS('\n✅ Importation terminée!'))
    
    def nettoyer_quantite(self, quantite):
        """Nettoie et convertit la quantité en Decimal"""
        if pd.isna(quantite) or quantite == 0:
            return Decimal('0.001')
        try:
            return Decimal(str(quantite))
        except:
            return Decimal('0.001')
    
    def nettoyer_texte(self, texte):
        """Nettoie le texte en supprimant les espaces superflus"""
        if pd.isna(texte):
            return ""
        return str(texte).strip()
    
    def normaliser_nom_ingredient(self, nom):
        """Normalise le nom d'un ingrédient pour la comparaison"""
        if pd.isna(nom) or nom == "":
            return ""
        
        nom = str(nom).lower().strip()
        
        # Supprimer les mots inutiles
        mots_a_supprimer = [
            'frais', 'fraîche', 'haché', 'hachée', 'émincé', 'émincée',
            'en dés', 'en cubes', 'en julienne', 'en tranches', 'tranché',
            'cuit', 'cuite', 'crus', 'crue', 'fin', 'finement', 'gros',
            'grossièrement', 'pelé', 'pelée', 'lavé', 'lavée', 'séché',
            'séchée', 'congelé', 'congelée', 'surgelé', 'surgelée'
        ]
        
        for mot in mots_a_supprimer:
            nom = nom.replace(mot, '').strip()
        
        # Normaliser les espaces multiples
        nom = ' '.join(nom.split())
        
        return nom
    
    def trouver_ingredient_similaire(self, nom):
        """Trouve un ingrédient existant similaire"""
        nom_normalise = self.normaliser_nom_ingredient(nom)
        
        if not nom_normalise:
            return None
        
        # Recherche exacte après normalisation
        if nom_normalise in self.ingredients_normalises:
            return self.ingredients_normalises[nom_normalise]
        
        # Recherche par similarité
        meilleur_score = 0
        meilleur_match = None
        
        for nom_existant, ingredient_obj in self.ingredients_normalises.items():
            # Calcul de similarité
            score = SequenceMatcher(None, nom_normalise, nom_existant).ratio()
            
            # Bonus si l'un contient l'autre
            if nom_normalise in nom_existant or nom_existant in nom_normalise:
                score += 0.1
            
            if score > meilleur_score and score >= self.similarity_threshold:
                meilleur_score = score
                meilleur_match = ingredient_obj
        
        if meilleur_match and self.debug:
            self.stdout.write(f"    ℹ️ '{nom}' → '{meilleur_match['nom']}' (score: {meilleur_score:.2f})")
        
        return meilleur_match
    
    def obtenir_ou_creer_unite_mesure(self, symbole):
        """Obtient ou crée une unité de mesure"""
        if pd.isna(symbole) or symbole == "":
            symbole = "unité"
        
        symbole = str(symbole).strip().lower()
        
        # Mapping complet des unités
        mapping_unites = {
            'g': ('Gramme', 'g'),
            'kg': ('Kilogramme', 'kg'),
            'l': ('Litre', 'L'),
            'ml': ('Millilitre', 'mL'),
            'unité': ('Unité', 'unité'),
            'unite': ('Unité', 'unité'),
            'un': ('Unité', 'unité'),
            'cl': ('Centilitre', 'cL'),
            'tasse': ('Tasse', 'tasse'),
            'c. à soupe': ('Cuillère à soupe', 'c. à soupe'),
            'c. à thé': ('Cuillère à thé', 'c. à thé'),
            'cui.the': ('Cuillère à thé', 'c. à thé'),
            'cuillère a the': ('Cuillère à thé', 'c. à thé'),
            'cuil. thé': ('Cuillère à thé', 'c. à thé'),
            'tranches': ('Tranche', 'tranche'),
            'tr': ('Tranche', 'tranche'),
            'livres': ('Livre', 'lb'),
            'lb': ('Livre', 'lb'),
            'p.p.': ('Par personne', 'p.p.'),
            'pot': ('Pot', 'pot'),
            'sacs': ('Sac', 'sac'),
            'filet': ('Filet', 'filet'),
            'poignée': ('Poignée', 'poignée'),
            'pâte': ('Pâte', 'pâte'),
            'cup': ('Tasse', 'tasse'),
            'grs': ('Gramme', 'g'),
            'q.s': ('Quantité suffisante', 'q.s.'),
            'q.s.': ('Quantité suffisante', 'q.s.'),
            'pm': ('Pièce', 'pce'),
            'boit': ('Boîte', 'boîte'),
            'p': ('Pièce', 'pce'),
        }
        
        if symbole in mapping_unites:
            nom, symbole_formate = mapping_unites[symbole]
        else:
            nom = symbole.upper() if len(symbole) <= 3 else symbole.capitalize()
            symbole_formate = symbole
        
        try:
            unite = UniteMesure.objects.get(symbole=symbole_formate)
            return unite
        except UniteMesure.DoesNotExist:
            pass
        
        try:
            unite, created = UniteMesure.objects.get_or_create(
                symbole=symbole_formate,
                defaults={'nom': nom}
            )
            if created and self.debug:
                self.stdout.write(f"  ✓ Unité créée: {nom} ({symbole_formate})")
        except:
            nom_modifie = f"{nom} ({symbole_formate})"
            unite, created = UniteMesure.objects.get_or_create(
                symbole=symbole_formate,
                defaults={'nom': nom_modifie}
            )
            if created and self.debug:
                self.stdout.write(f"  ✓ Unité créée: {nom_modifie} ({symbole_formate})")
        
        return unite
    
    def obtenir_ou_creer_ingredient(self, nom, symbole_unite):
        """Obtient ou crée un ingrédient avec normalisation"""
        if pd.isna(nom) or nom == "":
            return None
        
        nom_original = self.nettoyer_texte(nom)
        
        # Chercher un ingrédient similaire existant
        match = self.trouver_ingredient_similaire(nom_original)
        
        if match:
            # Utiliser l'ingrédient existant
            try:
                ingredient = Ingredient.objects.get(nom=match['nom'])
                return ingredient
            except Ingredient.DoesNotExist:
                # Créer avec le nom normalisé
                nom_a_utiliser = match['nom']
                symbole_unite = match['unite']
        else:
            # Utiliser le nom tel quel
            nom_a_utiliser = nom_original
        
        # Obtenir ou créer l'unité de mesure
        unite = self.obtenir_ou_creer_unite_mesure(symbole_unite)
        
        # Créer ou récupérer l'ingrédient
        ingredient, created = Ingredient.objects.get_or_create(
            nom=nom_a_utiliser,
            defaults={
                'unite_mesure': unite,
                'stock_reel': 0,
                'stock_alerte': 10,
                'description': f"Ingrédient importé automatiquement"
            }
        )
        
        if created and self.debug:
            self.stdout.write(self.style.SUCCESS(f"  ✓ Ingrédient créé: {nom_a_utiliser} ({unite.symbole})"))
        
        return ingredient
    
    def charger_et_normaliser_ingredients(self):
        """Charge et normalise les ingrédients existants"""
        self.stdout.write(self.style.WARNING("\n📦 Phase 1: Chargement et normalisation des ingrédients..."))
        
        try:
            df_ingredients = pd.read_excel(self.FICHIER_INGREDIENTS_EXISTANTS, sheet_name='Associations')
            
            for _, row in df_ingredients.iterrows():
                nom = self.nettoyer_texte(row['nom'])
                symbole = row['symbole unite de mesure']
                
                if nom:
                    # Créer l'ingrédient en base
                    ingredient = self.obtenir_ou_creer_ingredient(nom, symbole)
                    
                    # Stocker dans le dictionnaire de normalisation
                    nom_normalise = self.normaliser_nom_ingredient(nom)
                    self.ingredients_normalises[nom_normalise] = {
                        'nom': nom,
                        'unite': symbole,
                        'objet': ingredient
                    }
            
            self.stdout.write(self.style.SUCCESS(f"  → {len(self.ingredients_normalises)} ingrédients normalisés"))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"  ⚠ Fichier non trouvé: {self.FICHIER_INGREDIENTS_EXISTANTS}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ⚠ Erreur: {e}"))
    
    def obtenir_ou_creer_departement(self, nom):
        """Obtient ou crée un département"""
        if pd.isna(nom) or nom == "":
            nom = "Général"
        
        nom = self.nettoyer_texte(nom)
        departement, created = Departement.objects.get_or_create(
            nom=nom,
            defaults={'description': f"Département {nom}"}
        )
        
        if created and self.debug:
            self.stdout.write(self.style.SUCCESS(f"  ✓ Département créé: {nom}"))
        
        return departement
    
    def extraire_portions(self, texte_portions):
        """Extrait le nombre de portions depuis le texte"""
        if pd.isna(texte_portions):
            return 1
        
        texte = str(texte_portions)
        import re
        match = re.search(r'(\d+)', texte)
        if match:
            return int(match.group(1))
        return 1
    
    def est_sous_recette(self, nom):
        """Détermine si un nom correspond à une sous-recette"""
        if pd.isna(nom) or not isinstance(nom, str):
            return False
        nom_lower = nom.lower()
        return any(mot in nom_lower for mot in self.MOTS_CLES_SOUS_RECETTES)
    
    def importer_recettes_optimise(self):
        """Import optimisé basé sur ID_Recette et ID_Parent"""
        self.stdout.write(self.style.WARNING("\n📖 Phase 2: Lecture et analyse du fichier..."))
        
        try:
            df = pd.read_excel(self.FICHIER_RECETTES, sheet_name='Recettes_Consolidees')
            self.stdout.write(self.style.SUCCESS(f"  → {len(df)} lignes trouvées"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  ✗ Erreur: {e}"))
            return
        
        # Analyser la structure basée sur ID_Recette
        self.stdout.write(self.style.WARNING("\n🔍 Phase 3: Analyse de la structure par ID..."))
        
        # Obtenir tous les ID_Recette uniques (ce sont les vraies recettes)
        id_recettes_uniques = df['ID_Recette'].dropna().unique()
        self.stdout.write(f"  → {len(id_recettes_uniques)} recettes identifiées par ID unique")
        
        # Vérifier la présence de la colonne ID_Parent
        has_id_parent = 'ID_Parent' in df.columns
        if has_id_parent:
            # Compter les sous-recettes (lignes avec ID_Parent)
            nb_sous_recettes = df['ID_Parent'].notna().sum()
            self.stdout.write(f"  → {nb_sous_recettes} lignes de sous-recettes avec ID_Parent")
        
        # Structures de données pour organiser les données
        recettes_data = defaultdict(lambda: {
            'info': None,
            'ingredients': [],
            'sous_recettes': []  # Sous-recettes directement définies avec ID_Parent
        })
        
        # Parcourir toutes les lignes et les organiser par ID_Recette
        for _, row in df.iterrows():
            id_recette = row.get('ID_Recette')
            id_parent = row.get('ID_Parent') if has_id_parent else None
            est_sous_recette = row.get('Est_Sous_Recette') == 'OUI'
            nom_recette = self.nettoyer_texte(row.get('Nom_Recette', ''))
            
            # Si la ligne a un ID_Parent, c'est une sous-recette
            if has_id_parent and pd.notna(id_parent) and est_sous_recette:
                # C'est une sous-recette qui appartient à la recette ID_Parent
                if pd.notna(row.get('Ingredient_Normalise')):
                    # Créer ou compléter la sous-recette
                    sous_recette_key = f"{id_parent}_{nom_recette}"
                    
                    # Trouver ou créer l'entrée de la sous-recette dans la recette parente
                    recette_parent = recettes_data[str(int(id_parent))]
                    
                    # Chercher si cette sous-recette existe déjà
                    sr_existe = False
                    for sr in recette_parent['sous_recettes']:
                        if sr['nom'] == nom_recette:
                            sr['ingredients'].append({
                                'nom': row['Ingredient_Normalise'],
                                'unite': row.get('Unite_Mesure_Normalisee', 'g'),
                                'quantite': self.nettoyer_quantite(row.get('Quantite', 0))
                            })
                            sr_existe = True
                            break
                    
                    if not sr_existe:
                        recette_parent['sous_recettes'].append({
                            'nom': nom_recette,
                            'preparation': self.nettoyer_texte(row.get('Preparation', '')),
                            'quantite': self.nettoyer_quantite(row.get('Quantite', 1)),
                            'ingredients': [{
                                'nom': row['Ingredient_Normalise'],
                                'unite': row.get('Unite_Mesure_Normalisee', 'g'),
                                'quantite': self.nettoyer_quantite(row.get('Quantite', 0))
                            }]
                        })
                
            # Si la ligne a un ID_Recette, c'est une recette principale
            elif pd.notna(id_recette):
                id_str = str(int(id_recette))
                
                # Si c'est la première fois qu'on voit cette recette, initialiser ses infos
                if recettes_data[id_str]['info'] is None:
                    recettes_data[id_str]['info'] = {
                        'id': id_str,
                        'nom': nom_recette,
                        'departement': row.get('Departement'),
                        'portions': self.extraire_portions(row.get('Portions', 1)),
                        'preparation': self.nettoyer_texte(row.get('Preparation', ''))
                    }
                
                # Ajouter l'ingrédient ou la référence à une sous-recette
                if est_sous_recette:
                    # C'est une référence à une autre recette comme sous-recette
                    nom_ingredient = self.nettoyer_texte(row.get('Ingredient', ''))
                    if nom_ingredient and self.est_sous_recette(nom_ingredient):
                        # Vérifier si pas déjà ajouté
                        if not any(sr['nom'] == nom_ingredient for sr in recettes_data[id_str]['sous_recettes']):
                            recettes_data[id_str]['sous_recettes'].append({
                                'nom': nom_ingredient,
                                'preparation': '',
                                'quantite': self.nettoyer_quantite(row.get('Quantite', 1)),
                                'ingredients': [],  # Sera rempli plus tard si la sous-recette existe
                                'est_reference': True  # Marquer comme référence externe
                            })
                else:
                    # C'est un ingrédient direct
                    if pd.notna(row.get('Ingredient_Normalise')):
                        recettes_data[id_str]['ingredients'].append({
                            'nom': row['Ingredient_Normalise'],
                            'unite': row.get('Unite_Mesure_Normalisee', 'g'),
                            'quantite': self.nettoyer_quantite(row.get('Quantite', 0))
                        })
        
        self.stdout.write(f"  → {len(recettes_data)} recettes à importer")
        
        # Identifier les sous-recettes qui sont aussi des recettes principales
        # (pour les références externes)
        sous_recettes_globales = {}
        grouped_by_name = df.groupby('Nom_Recette')
        
        for nom, groupe in grouped_by_name:
            if self.est_sous_recette(nom):
                # Collecter les ingrédients de cette sous-recette
                ingredients = []
                for _, row in groupe.iterrows():
                    if pd.notna(row.get('Ingredient_Normalise')):
                        ingredients.append({
                            'nom': row['Ingredient_Normalise'],
                            'unite': row.get('Unite_Mesure_Normalisee', 'g'),
                            'quantite': self.nettoyer_quantite(row.get('Quantite', 0))
                        })
                
                if ingredients:
                    sous_recettes_globales[nom] = {
                        'preparation': self.nettoyer_texte(groupe.iloc[0].get('Preparation', '')),
                        'ingredients': ingredients
                    }
        
        self.stdout.write(f"  → {len(sous_recettes_globales)} sous-recettes globales identifiées")
        
        # Import en base de données
        self.stdout.write(self.style.WARNING("\n💾 Phase 4: Import en base de données..."))
        
        compteur_recettes = 0
        compteur_sous_recettes = 0
        compteur_ingredients = 0
        recettes_creees = {}
        
        with transaction.atomic():
            # Créer uniquement les recettes principales
            self.stdout.write(self.style.WARNING("\n  📝 Création des recettes principales..."))
            
            for nom_recette, data in recettes_data.items():
                info = data['info']
                
                if info is None:
                    continue
                
                try:
                    departement = self.obtenir_ou_creer_departement(info['departement'])
                    
                    recette, created = Recette.objects.get_or_create(
                        nom=info['nom'],
                        defaults={
                            'description': f"Recette ID {info['id']}",
                            'explication_fabrication': info['preparation'],
                            'departement': departement,
                            'temps_preparation': 30,
                            'temps_cuisson': 30,
                            'portions': info['portions']
                        }
                    )
                    
                    if created:
                        compteur_recettes += 1
                        if self.debug:
                            self.stdout.write(self.style.SUCCESS(f"    ✓ ID {info['id']}: {info['nom'][:40]}..."))
                    else:
                        RecetteIngredient.objects.filter(recette=recette).delete()
                        SousRecette.objects.filter(recette_parent=recette).delete()
                    
                    recettes_creees[nom_recette] = recette
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"    ✗ Erreur ID {nom_recette}: {e}"))
            
            # Ajouter les ingrédients directs
            self.stdout.write(self.style.WARNING("\n  🥗 Ajout des ingrédients..."))
            
            for nom_recette, data in recettes_data.items():
                if nom_recette not in recettes_creees:
                    continue
                
                recette = recettes_creees[nom_recette]
                
                for ing_data in data['ingredients']:
                    try:
                        ingredient = self.obtenir_ou_creer_ingredient(
                            ing_data['nom'],
                            ing_data['unite']
                        )
                        if ingredient:
                            RecetteIngredient.objects.get_or_create(
                                recette=recette,
                                ingredient=ingredient,
                                defaults={'quantite': ing_data['quantite']}
                            )
                            compteur_ingredients += 1
                    except Exception as e:
                        if self.debug:
                            self.stdout.write(self.style.ERROR(f"    ✗ Erreur ingrédient: {e}"))
            
            # Créer les sous-recettes
            self.stdout.write(self.style.WARNING("\n  🔗 Création des sous-recettes..."))
            
            for nom_recette, data in recettes_data.items():
                if nom_recette not in recettes_creees:
                    continue
                
                recette = recettes_creees[nom_recette]
                
                # Utiliser 'sous_recettes' au lieu de 'sous_recettes_refs'
                for sr_data in data.get('sous_recettes', []):
                    nom_sr = sr_data['nom']
                    
                    try:
                        # Créer l'objet SousRecette
                        sous_recette, created = SousRecette.objects.get_or_create(
                            nom=nom_sr,
                            recette_parent=recette,
                            defaults={
                                'explication_fabrication': sr_data.get('preparation', '') or f"Sous-recette {nom_sr}",
                                'quantite': sr_data.get('quantite', Decimal('1'))
                            }
                        )
                        
                        if created:
                            compteur_sous_recettes += 1
                            
                            # Si c'est une référence externe et qu'on a les données globales
                            if sr_data.get('est_reference') and nom_sr in sous_recettes_globales:
                                global_data = sous_recettes_globales[nom_sr]
                                ingredients_a_ajouter = global_data['ingredients']
                            else:
                                # Utiliser les ingrédients définis localement
                                ingredients_a_ajouter = sr_data.get('ingredients', [])
                            
                            # Ajouter les ingrédients de la sous-recette
                            for ing_data in ingredients_a_ajouter:
                                ingredient = self.obtenir_ou_creer_ingredient(
                                    ing_data['nom'],
                                    ing_data.get('unite', 'g')
                                )
                                if ingredient:
                                    SousRecetteIngredient.objects.get_or_create(
                                        sous_recette=sous_recette,
                                        ingredient=ingredient,
                                        defaults={'quantite': ing_data.get('quantite', Decimal('0.001'))}
                                    )
                            
                            if self.debug:
                                nb_ing = sous_recette.sousrecette_ingredients.count()
                                self.stdout.write(self.style.SUCCESS(f"    ✓ {recette.nom[:20]}... → {nom_sr[:20]}... ({nb_ing} ing.)"))
                                
                    except Exception as e:
                        if self.debug:
                            self.stdout.write(self.style.ERROR(f"    ✗ Erreur sous-recette {nom_sr}: {e}"))
            
            # Calculer les coûts
            for recette in recettes_creees.values():
                try:
                    recette.calculer_cout()
                except:
                    pass
        
        # Résumé final
        self.stdout.write(self.style.SUCCESS(f"\n{'='*60}"))
        self.stdout.write(self.style.SUCCESS("📊 RÉSUMÉ DE L'IMPORTATION"))
        self.stdout.write(self.style.SUCCESS(f"{'='*60}"))
        self.stdout.write(self.style.SUCCESS(f"✓ {compteur_recettes} recettes créées (IDs: {len(id_recettes_uniques)})"))
        self.stdout.write(self.style.SUCCESS(f"✓ {compteur_sous_recettes} sous-recettes créées"))
        self.stdout.write(self.style.SUCCESS(f"✓ {compteur_ingredients} ingrédients ajoutés"))
        self.stdout.write(self.style.SUCCESS(f"✓ {Ingredient.objects.count()} ingrédients totaux en base"))
        
        # Vérifications
        self.stdout.write(self.style.WARNING("\n🔍 Vérifications finales..."))
        recettes_avec_sr = Recette.objects.filter(sous_recettes__isnull=False).distinct().count()
        self.stdout.write(f"  → {recettes_avec_sr} recettes ont des sous-recettes")
        
        if self.debug:
            # Afficher quelques exemples
            self.stdout.write(self.style.WARNING("\n📋 Exemples de recettes avec sous-recettes:"))
            for recette in Recette.objects.filter(sous_recettes__isnull=False).distinct()[:3]:
                self.stdout.write(f"\n  {recette.nom}:")
                for sr in recette.sous_recettes.all():
                    nb_ing = sr.sousrecette_ingredients.count()
                    self.stdout.write(f"    → {sr.nom} (quantité: {sr.quantite}, {nb_ing} ingrédients)")