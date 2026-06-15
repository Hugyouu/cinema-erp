# Cinema ERP

## Sujet

Gestion d'un complexe cinématographique avec programmation, billetterie et exploitation.

### Priorités

- Salles & Séances : Capacité, équipements (3D, IMAX), horaires, conflits de planning
- Catalogue Films : Distributeurs, droits de diffusion, durée de licence3
- Contrats Distributeurs : Négociation des % recettes reversées, minimums garantis
- Billetterie : Vente de places, tarifs (étudiant, senior, CE…), réservations
- Clients & Abonnements : Carte fidélité, pass illimité type CinéPass, historique
- Recettes & Reversements : Calcul automatique des droits dus aux distributeurs par film
- Facturation : Factures distributeurs, justificatifs de reversement hebdomadaires

### Bonus

- Statistiques
- Dashboard séances du jour

## Stack

- FastAPI
- SQLAlchemy
- Alembic
- Pydantic (natif dans FastAPI)
- PostgreSQL

## Setup

```bash
# Créer l'environement virtuel
python -m venv .venv
# L'activer
.venv\Scripts\activate # Windows
source .venv/bin/activate # Linux
# Installer tous les librairies (dans le .venv)
pip install -r requirements.txt
# Lancer l'application
fastapi dev app/main.py
```
