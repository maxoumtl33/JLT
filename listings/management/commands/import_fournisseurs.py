# recipes/management/commands/import_fournisseurs.py

from django.core.management.base import BaseCommand
from listings.models import Fournisseur

class Command(BaseCommand):
    help = 'Importe les fournisseurs depuis les données fournies'

    def handle(self, *args, **kwargs):
        fournisseurs_data = [
            {
                'nom': 'Can-Am',
                'telephone': '514-655-0355',
                'contact_principal': 'Daniel: 514-655-0355, Benoit: 514-710-1148, Biaggio: 514-264-5120',
                'type_produits': 'Fruits et légumes, viande, fruits de mer frais et congelés',
                'procedure_commande': 'Commander avant 9h pour réception début d\'après-midi. Limite 17h, idéal mettre sur Discord avant 14h',
                'notes': 'Meilleur pour les prix fruits/légumes et saumon. Excellent pour dépannage produits carnés et viande.',
            },
            {
                'nom': 'Hector Larivée',
                'telephone': '514-521-8331',
                'contact_principal': 'Benoit: 514-521-8331#4308, Myriam: 514-521-8331#4305',
                'type_produits': 'Fruits et légumes frais, produits épicerie, pain Bateau mouche, fondant au chocolat',
                'procedure_commande': 'Commander avant 9h pour réception début d\'après-midi. Limite 17h, idéal mettre sur Discord avant 14h',
                'notes': 'Méga liste de produits épicerie et viandes, fruits de mer congelés',
            },
            {
                'nom': 'J-G Fruit et Légumes',
                'telephone': '514-792-9987',
                'contact_principal': 'Line: 514-792-9987',
                'type_produits': 'Seulement fruits et légumes',
                'procedure_commande': 'Commander avant 16h pour livraison lendemain matin',
                'notes': 'Utilisé surtout comme back-up. Bons prix aussi.',
            },
            {
                'nom': 'Gordon GFS',
                'telephone': '438-332-0343',
                'contact_principal': 'Marc-Antoine: 438-332-0343',
                'type_produits': 'Produits épicerie, viande, fruits de mer, emballage, produits Coke',
                'procedure_commande': 'Commander avant 16h. Commande en ligne via plateforme (voir section guide)',
                'notes': 'Fournisseur principal d\'épicerie, viandes et fruits de mer congelés. En urgence, Marc-Antoine peut livrer avec sa voiture.',
            },
            {
                'nom': 'Sysco',
                'telephone': '514-531-6717',
                'contact_principal': 'Giuseppe: 514-531-6717',
                'type_produits': 'Produits épicerie, viande, fruits de mer, emballage, produits Pepsi (Dole)',
                'procedure_commande': 'Commander avant 16h via plateforme en ligne',
                'notes': 'Commande surtout produits Pepsi et craquelins Deluxe. Bon back-up si GFS n\'a pas en stock.',
            },
            {
                'nom': 'Maison du Rôti',
                'telephone': '514-521-2448',
                'contact_principal': '',
                'type_produits': 'Viande',
                'procedure_commande': 'Placer commandes de 6h30 à 16h. Si appel de bonne heure, livraison PM possible',
                'notes': 'Spécialiste viande',
            },
            {
                'nom': 'Vaskin',
                'telephone': '438-401-5938',
                'contact_principal': 'Dylan: 438-401-5938 (texter si pas de réponse)',
                'type_produits': 'Poisson, fruits de mer, spécialité huîtres',
                'procedure_commande': 'Minimum 16-24h à l\'avance',
                'notes': 'Spécialité huîtres et produits de mer exotiques. Tient aussi tous les produits standards.',
            },
            {
                'nom': 'Noreff',
                'telephone': '514-803-9390',
                'contact_principal': 'Renaldo: 514-803-9390',
                'type_produits': 'Poisson, fruits de mer',
                'procedure_commande': 'Commander avant 16h',
                'notes': 'Utilisé surtout comme back-up',
            },
            {
                'nom': 'Carrousel',
                'telephone': '450-655-2025',
                'contact_principal': 'Sylvie: 450-655-2025 #241',
                'type_produits': 'Emballage',
                'procedure_commande': 'Commander avant 17h lundi et jeudi pour livraison mardi et vendredi. Exceptions possibles si urgence.',
                'notes': 'Fournisseur emballage principal',
            },
            {
                'nom': 'ABC Embaluxe',
                'telephone': '514-808-5176',
                'contact_principal': 'Sandra: 514-808-5176',
                'type_produits': 'Pics et emballage pour sections canapés et pâtisserie',
                'procedure_commande': 'Commander avant 16h avec 24-48h de délai pour livraison',
                'notes': 'Spécialisé emballage canapés et pâtisserie',
            },
            {
                'nom': 'Marché PA',
                'telephone': '',
                'contact_principal': '',
                'adresse': '1420 rue Fort (à 2 coins de rue du traiteur)',
                'type_produits': 'Fruits et légumes, fromage végane et sans lactose, produits épicerie',
                'procedure_commande': 'Ouvre à 7h',
                'notes': 'La meilleure place pour se dépanner',
            },
            {
                'nom': 'H-Mart',
                'telephone': '',
                'contact_principal': '',
                'adresse': '2109 Saint-Catherine (moins de 5 min à pied du traiteur)',
                'type_produits': 'Produits asiatiques, Kim-chi en seau de 15L',
                'procedure_commande': 'Ouvre à 9h. Commander Kim-chi 1 semaine à l\'avance (normalement 5 seaux à la fois)',
                'notes': 'Meilleur choix pour tous les produits asiatiques',
            },
            {
                'nom': 'Aubut',
                'telephone': '',
                'contact_principal': '',
                'adresse': '3975 St-Ambroise',
                'type_produits': 'Fruits, légumes, épicerie, emballages',
                'procedure_commande': 'Ouvre à 8h',
                'notes': 'Fournisseur généraliste',
            },
        ]

        created_count = 0
        updated_count = 0
        
        for data in fournisseurs_data:
            fournisseur, created = Fournisseur.objects.update_or_create(
                nom=data['nom'],
                defaults={
                    'telephone': data.get('telephone', ''),
                    'contact_principal': data.get('contact_principal', ''),
                    'adresse': data.get('adresse', ''),
                    'email': data.get('email', ''),
                    'type_produits': data.get('type_produits', ''),
                    'procedure_commande': data.get('procedure_commande', ''),
                    'notes': data.get('notes', ''),
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Créé: {fournisseur.nom}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'↻ Mis à jour: {fournisseur.nom}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n--- Résumé ---\n'
                f'Fournisseurs créés: {created_count}\n'
                f'Fournisseurs mis à jour: {updated_count}\n'
                f'Total: {created_count + updated_count}'
            )
        )