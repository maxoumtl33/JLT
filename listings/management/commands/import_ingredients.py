from django.core.management.base import BaseCommand
from django.db import transaction
from decimal import Decimal
from listings.models import UniteMesure, Ingredient  # Remplacez 'votre_app' par le nom de votre app
from django.db import models

class Command(BaseCommand):
    help = 'Importe les ingrédients et unités de mesure depuis les données Excel'

    def handle(self, *args, **options):
        # Données des unités de mesure
        unites_data = [
            {'nom': 'Gramme', 'symbole': 'g'},
            {'nom': 'Unité', 'symbole': 'un'},
            {'nom': 'Millilitre', 'symbole': 'ml'},
            {'nom': 'Tranche', 'symbole': 'tr'},
            {'nom': 'Au goût', 'symbole': 'AG'},
        ]
        
        # Données des ingrédients (153 ingrédients)
        ingredients_data = [
            {'nom': 'Ail', 'unite': 'Gramme'},
            {'nom': 'Aneth', 'unite': 'Gramme'},
            {'nom': 'Aubergine', 'unite': 'Gramme'},
            {'nom': 'Avocat', 'unite': 'Unité'},
            {'nom': 'Basilic', 'unite': 'Gramme'},
            {'nom': 'Betterave', 'unite': 'Gramme'},
            {'nom': 'Brocoli', 'unite': 'Gramme'},
            {'nom': 'Carotte', 'unite': 'Gramme'},
            {'nom': 'Céleri', 'unite': 'Gramme'},
            {'nom': 'Champignon', 'unite': 'Gramme'},
            {'nom': 'Chou', 'unite': 'Gramme'},
            {'nom': 'Chou kale', 'unite': 'Gramme'},
            {'nom': 'Chou rouge', 'unite': 'Gramme'},
            {'nom': 'Chou vert', 'unite': 'Gramme'},
            {'nom': 'Chou-fleur', 'unite': 'Gramme'},
            {'nom': 'Ciboulette', 'unite': 'Gramme'},
            {'nom': 'Concombre', 'unite': 'Gramme'},
            {'nom': 'Coriandre', 'unite': 'Gramme'},
            {'nom': 'Courgette', 'unite': 'Gramme'},
            {'nom': 'Échalote', 'unite': 'Gramme'},
            {'nom': 'Épinard', 'unite': 'Gramme'},
            {'nom': 'Fenouil', 'unite': 'Gramme'},
            {'nom': 'Haricot vert', 'unite': 'Gramme'},
            {'nom': 'Laitue', 'unite': 'Gramme'},
            {'nom': 'Menthe', 'unite': 'Gramme'},
            {'nom': 'Navet', 'unite': 'Gramme'},
            {'nom': 'Oignon', 'unite': 'Gramme'},
            {'nom': 'Oignon rouge', 'unite': 'Gramme'},
            {'nom': 'Oignon vert', 'unite': 'Gramme'},
            {'nom': 'Persil', 'unite': 'Gramme'},
            {'nom': 'Poireau', 'unite': 'Gramme'},
            {'nom': 'Poivron', 'unite': 'Gramme'},
            {'nom': 'Poivron jaune', 'unite': 'Gramme'},
            {'nom': 'Poivron rouge', 'unite': 'Gramme'},
            {'nom': 'Poivron vert', 'unite': 'Gramme'},
            {'nom': 'Pomme de terre', 'unite': 'Gramme'},
            {'nom': 'Radis', 'unite': 'Gramme'},
            {'nom': 'Romarin', 'unite': 'Gramme'},
            {'nom': 'Roquette', 'unite': 'Gramme'},
            {'nom': 'Thym', 'unite': 'Gramme'},
            {'nom': 'Tomate', 'unite': 'Gramme'},
            {'nom': 'Tomate cerise', 'unite': 'Gramme'},
            {'nom': 'Tomate séchée', 'unite': 'Gramme'},
            {'nom': 'Citron', 'unite': 'Unité'},
            {'nom': 'Fraise', 'unite': 'Gramme'},
            {'nom': 'Framboise', 'unite': 'Gramme'},
            {'nom': 'Lime', 'unite': 'Unité'},
            {'nom': 'Mangue', 'unite': 'Gramme'},
            {'nom': 'Orange', 'unite': 'Unité'},
            {'nom': 'Pamplemousse', 'unite': 'Unité'},
            {'nom': 'Pêche', 'unite': 'Gramme'},
            {'nom': 'Poire', 'unite': 'Gramme'},
            {'nom': 'Pomme', 'unite': 'Gramme'},
            {'nom': 'Raisin', 'unite': 'Gramme'},
            {'nom': 'Beurre', 'unite': 'Gramme'},
            {'nom': 'Crème', 'unite': 'Millilitre'},
            {'nom': 'Crème 35%', 'unite': 'Millilitre'},
            {'nom': 'Feta', 'unite': 'Gramme'},
            {'nom': 'Fromage à la crème', 'unite': 'Gramme'},
            {'nom': 'Fromage de chèvre', 'unite': 'Gramme'},
            {'nom': 'Lait', 'unite': 'Millilitre'},
            {'nom': 'Mascarpone', 'unite': 'Gramme'},
            {'nom': 'Mozzarella', 'unite': 'Gramme'},
            {'nom': 'Parmesan', 'unite': 'Gramme'},
            {'nom': 'Ricotta', 'unite': 'Gramme'},
            {'nom': 'Yogourt', 'unite': 'Millilitre'},
            {'nom': 'Yogourt grec', 'unite': 'Millilitre'},
            {'nom': 'Bacon', 'unite': 'Gramme'},
            {'nom': 'Bœuf', 'unite': 'Gramme'},
            {'nom': 'Crevette', 'unite': 'Gramme'},
            {'nom': 'Jambon', 'unite': 'Gramme'},
            {'nom': 'Œuf', 'unite': 'Unité'},
            {'nom': 'Poitrine de poulet', 'unite': 'Gramme'},
            {'nom': 'Porc', 'unite': 'Gramme'},
            {'nom': 'Poulet', 'unite': 'Gramme'},
            {'nom': 'Prosciutto', 'unite': 'Tranche'},
            {'nom': 'Saumon', 'unite': 'Gramme'},
            {'nom': 'Saumon fumé', 'unite': 'Gramme'},
            {'nom': 'Thon', 'unite': 'Gramme'},
            {'nom': 'Tofu', 'unite': 'Gramme'},
            {'nom': 'Avoine', 'unite': 'Gramme'},
            {'nom': 'Couscous', 'unite': 'Gramme'},
            {'nom': 'Farine', 'unite': 'Gramme'},
            {'nom': 'Pain', 'unite': 'Gramme'},
            {'nom': 'Pâtes', 'unite': 'Gramme'},
            {'nom': 'Quinoa', 'unite': 'Gramme'},
            {'nom': 'Riz', 'unite': 'Gramme'},
            {'nom': 'Haricot blanc', 'unite': 'Gramme'},
            {'nom': 'Haricot noir', 'unite': 'Gramme'},
            {'nom': 'Haricot rouge', 'unite': 'Gramme'},
            {'nom': 'Lentille', 'unite': 'Gramme'},
            {'nom': 'Pois chiche', 'unite': 'Gramme'},
            {'nom': 'Amande', 'unite': 'Gramme'},
            {'nom': 'Graine de sésame', 'unite': 'Gramme'},
            {'nom': 'Noisette', 'unite': 'Gramme'},
            {'nom': 'Noix', 'unite': 'Gramme'},
            {'nom': 'Noix de cajou', 'unite': 'Gramme'},
            {'nom': 'Pacane', 'unite': 'Gramme'},
            {'nom': 'Pistache', 'unite': 'Gramme'},
            {'nom': "Huile d'olive", 'unite': 'Millilitre'},
            {'nom': 'Huile de canola', 'unite': 'Millilitre'},
            {'nom': 'Huile de sésame', 'unite': 'Millilitre'},
            {'nom': 'Huile végétale', 'unite': 'Millilitre'},
            {'nom': 'Vinaigre balsamique', 'unite': 'Millilitre'},
            {'nom': 'Vinaigre de cidre', 'unite': 'Millilitre'},
            {'nom': 'Vinaigre de riz', 'unite': 'Millilitre'},
            {'nom': 'Cornichon', 'unite': 'Gramme'},
            {'nom': 'Harissa', 'unite': 'Millilitre'},
            {'nom': 'Ketchup', 'unite': 'Millilitre'},
            {'nom': 'Mayonnaise', 'unite': 'Millilitre'},
            {'nom': 'Miel', 'unite': 'Millilitre'},
            {'nom': 'Moutarde', 'unite': 'Millilitre'},
            {'nom': 'Moutarde de Dijon', 'unite': 'Millilitre'},
            {'nom': 'Pâte de tomate', 'unite': 'Millilitre'},
            {'nom': 'Pesto', 'unite': 'Millilitre'},
            {'nom': 'Sauce soja', 'unite': 'Millilitre'},
            {'nom': 'Sauce sriracha', 'unite': 'Millilitre'},
            {'nom': 'Sauce worcestershire', 'unite': 'Millilitre'},
            {'nom': "Sirop d'érable", 'unite': 'Millilitre'},
            {'nom': 'Tabasco', 'unite': 'Millilitre'},
            {'nom': 'Tahini', 'unite': 'Millilitre'},
            {'nom': 'Cannelle', 'unite': 'Gramme'},
            {'nom': 'Cumin', 'unite': 'Gramme'},
            {'nom': 'Curcuma', 'unite': 'Gramme'},
            {'nom': 'Gingembre', 'unite': 'Gramme'},
            {'nom': 'Origan', 'unite': 'Gramme'},
            {'nom': 'Paprika', 'unite': 'Gramme'},
            {'nom': 'Poivre', 'unite': 'Gramme'},
            {'nom': 'Sel', 'unite': 'Gramme'},
            {'nom': 'Sel et poivre', 'unite': 'Au goût'},
            {'nom': 'Bicarbonate de soude', 'unite': 'Gramme'},
            {'nom': 'Cacao', 'unite': 'Gramme'},
            {'nom': 'Cassonade', 'unite': 'Gramme'},
            {'nom': 'Chocolat blanc', 'unite': 'Gramme'},
            {'nom': 'Chocolat noir', 'unite': 'Gramme'},
            {'nom': 'Croûton', 'unite': 'Gramme'},
            {'nom': 'Eau', 'unite': 'Millilitre'},
            {'nom': 'Extrait de vanille', 'unite': 'Millilitre'},
            {'nom': 'Fécule de maïs', 'unite': 'Gramme'},
            {'nom': 'Gélatine', 'unite': 'Gramme'},
            {'nom': 'Glucose', 'unite': 'Millilitre'},
            {'nom': 'Levure chimique', 'unite': 'Gramme'},
            {'nom': 'Poudre à pâte', 'unite': 'Gramme'},
            {'nom': 'Sucre', 'unite': 'Gramme'},
            {'nom': 'Sucre glace', 'unite': 'Gramme'},
            {'nom': 'Vanille', 'unite': 'Millilitre'},
            {'nom': 'Bouillon de légume', 'unite': 'Millilitre'},
            {'nom': 'Bouillon de poulet', 'unite': 'Millilitre'},
            {'nom': 'Jus de citron', 'unite': 'Millilitre'},
            {'nom': 'Jus de lime', 'unite': 'Millilitre'},
            {'nom': 'Lait de coco', 'unite': 'Millilitre'},
            {'nom': 'Vin blanc', 'unite': 'Millilitre'},
            {'nom': 'Vin rouge', 'unite': 'Millilitre'},
        ]

        try:
            with transaction.atomic():
                # Créer les unités de mesure
                self.stdout.write('Création des unités de mesure...')
                unites_created = 0
                unites_updated = 0
                
                for unite_data in unites_data:
                    unite, created = UniteMesure.objects.update_or_create(
                        nom=unite_data['nom'],
                        defaults={'symbole': unite_data['symbole']}
                    )
                    if created:
                        unites_created += 1
                        self.stdout.write(f"  ✓ Créé: {unite.nom} ({unite.symbole})")
                    else:
                        unites_updated += 1
                        self.stdout.write(f"  ↻ Mis à jour: {unite.nom} ({unite.symbole})")
                
                self.stdout.write(self.style.SUCCESS(
                    f'\n✅ Unités de mesure: {unites_created} créées, {unites_updated} mises à jour'
                ))
                
                # Créer les ingrédients
                self.stdout.write('\nCréation des ingrédients...')
                ingredients_created = 0
                ingredients_updated = 0
                errors = []
                
                for ing_data in ingredients_data:
                    try:
                        # Récupérer l'unité de mesure correspondante
                        unite = UniteMesure.objects.get(nom=ing_data['unite'])
                        
                        # Créer ou mettre à jour l'ingrédient
                        ingredient, created = Ingredient.objects.update_or_create(
                            nom=ing_data['nom'],
                            defaults={
                                'unite_mesure': unite,
                                'stock_reel': Decimal('0.00'),
                                'stock_alerte': Decimal('10.00'),
                                'description': f"Ingrédient importé automatiquement - Unité: {unite.symbole}"
                            }
                        )
                        
                        if created:
                            ingredients_created += 1
                            self.stdout.write(f"  ✓ Créé: {ingredient.nom} ({unite.symbole})")
                        else:
                            ingredients_updated += 1
                            self.stdout.write(f"  ↻ Mis à jour: {ingredient.nom} ({unite.symbole})")
                            
                    except UniteMesure.DoesNotExist:
                        error_msg = f"Unité '{ing_data['unite']}' non trouvée pour '{ing_data['nom']}'"
                        errors.append(error_msg)
                        self.stdout.write(self.style.ERROR(f"  ✗ Erreur: {error_msg}"))
                    except Exception as e:
                        error_msg = f"Erreur pour '{ing_data['nom']}': {str(e)}"
                        errors.append(error_msg)
                        self.stdout.write(self.style.ERROR(f"  ✗ {error_msg}"))
                
                # Afficher le résumé
                self.stdout.write('\n' + '='*50)
                self.stdout.write(self.style.SUCCESS(
                    f'✅ Import terminé avec succès!'
                ))
                self.stdout.write(f'  Unités de mesure: {unites_created} créées, {unites_updated} mises à jour')
                self.stdout.write(f'  Ingrédients: {ingredients_created} créés, {ingredients_updated} mis à jour')
                
                if errors:
                    self.stdout.write(self.style.WARNING(f'\n⚠️ {len(errors)} erreurs rencontrées:'))
                    for error in errors[:10]:  # Afficher max 10 erreurs
                        self.stdout.write(f'  - {error}')
                    if len(errors) > 10:
                        self.stdout.write(f'  ... et {len(errors) - 10} autres erreurs')
                
                # Statistiques finales
                self.stdout.write('\n📊 Statistiques finales:')
                self.stdout.write(f'  Total unités de mesure: {UniteMesure.objects.count()}')
                self.stdout.write(f'  Total ingrédients: {Ingredient.objects.count()}')
                
                # Vérifier les stocks d'alerte
                ingredients_alerte = Ingredient.objects.filter(stock_reel__lte=models.F('stock_alerte'))
                if ingredients_alerte.exists():
                    self.stdout.write(self.style.WARNING(
                        f'\n⚠️ {ingredients_alerte.count()} ingrédients nécessitent un réapprovisionnement'
                    ))
                    
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'\n❌ Erreur lors de l\'import: {str(e)}'
            ))
            raise