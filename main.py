import argparse
from gestion_animaux import GestionAnimaux
from gestion_soins import GestionSoins
from interface import InterfaceGUI
from gestion_vaccins import GestionVaccins
from rapportPDF import RapportPDF
from alerte import GestionAlertes

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
            rapport_pdf = RapportPDF("Rapport complet des animaux du cheptel", gestion_animaux, gestion_soins, gestion_vaccins)
            rapport_pdf.generate_animal_report()
        elif args.rapport == 'vaccinations':
            rapport_pdf = RapportPDF("Rapport complet des vaccin du cheptel", gestion_animaux, gestion_soins, gestion_vaccins)
            rapport_pdf.generate_vaccination_report()
        elif args.rapport == 'cheptel':
            rapport_pdf = RapportPDF("Rapport Complet du Cheptel", gestion_animaux, gestion_soins, gestion_vaccins)
            rapport_pdf.generer_rapport_animaux_et_soins()

    if args.verifier_alertes:
        check_alerts(gestion_alertes)

def check_alerts(gestion_alertes):
    """Vérifie les alertes programmées pour les vaccins."""
    try:
        gestion_alertes.verifier_et_afficher_alertes()
    except Exception as e:
        print(f"Erreur lors de la vérification des alertes : {e}")

if __name__ == '__main__':
    main()
