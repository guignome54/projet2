import argparse
from datetime import datetime
from gestion_animaux import GestionAnimaux
from gestion_soins import GestionSoins
from interface import InterfaceGUI
from gestion_vaccins import GestionVaccins
from rapportPDF import RapportPDF
from alerte import GestionAlertes
import pandas as pd

def main():
    parser = argparse.ArgumentParser(description="Gestion de Cheptel - Application pour éleveurs")
    parser.add_argument('--gui', action='store_true', help="Lancer l'interface graphique.")
    parser.add_argument('--rapport', type=str, choices=['animaux', 'vaccinations', 'cheptel'], help="Générer un rapport spécifique.")
    parser.add_argument('--verifier-alertes', action='store_true', help="Vérifier les alertes programmées.")
    args = parser.parse_args()

    db_file = "cheptel.db"
    gestion_animaux = GestionAnimaux(db_file)
    gestion_soins = GestionSoins(gestion_animaux.conn)
    gestion_vaccins = GestionVaccins(gestion_animaux.conn)
    gestion_alertes = GestionAlertes(gestion_animaux.conn)
    if args.gui:
        app = InterfaceGUI(gestion_animaux, gestion_soins, gestion_vaccins, gestion_alertes)
        app.run()

    if args.rapport:
        if args.rapport == 'animaux':
            generate_animal_report(gestion_animaux)
        elif args.rapport == 'vaccinations':
            generate_vaccination_report(gestion_soins)
        elif args.rapport == 'cheptel':
            rapport_pdf = RapportPDF("Rapport Complet du Cheptel", gestion_animaux, gestion_soins, gestion_vaccins)
            rapport_pdf.generer_rapport_animaux_et_soins()

    if args.verifier_alertes:
        check_alerts(gestion_alertes)


def generate_animal_report(gestion_animaux):
    """Génère un rapport des animaux."""
    try:
        animaux = gestion_animaux.consulter_animal()
        df = pd.DataFrame(animaux, columns=['ID', 'Nom', 'Race', 'Âge', 'État de Santé'])
        df.to_csv('rapport_animaux.csv', index=False)
        print("Rapport des animaux généré avec succès : rapport_animaux.csv")
    except Exception as e:
        print(f"Erreur lors de la génération du rapport des animaux : {e}")

def generate_vaccination_report(gestion_soins, gestion_vaccins):
    """Génère un rapport des vaccinations."""
    try:
        vaccins = gestion_vaccins.consulter_vaccins()
        df = pd.DataFrame(vaccins, columns=['ID', 'ID Animal', 'Nom du Vaccin', 'Date du Vaccin', 'Date du Prochain Rappel'])
        df.to_csv('rapport_vaccinations.csv', index=False)
        print("Rapport des vaccinations généré avec succès : rapport_vaccinations.csv")
    except Exception as e:
        print(f"Erreur lors de la génération du rapport des vaccinations : {e}")

def check_alerts(gestion_alertes):
    """Vérifie les alertes programmées pour les vaccins."""
    try:
        gestion_alertes.verifier_et_afficher_alertes()
    except Exception as e:
        print(f"Erreur lors de la vérification des alertes : {e}")

if __name__ == '__main__':
    main()
