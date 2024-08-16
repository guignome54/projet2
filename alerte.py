import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class GestionAlertes:
    def __init__(self, conn):
        """Initialise la gestion des alertes."""
        self.conn = conn
        self.alertes = []
        self.alertes_affichees = set()  # Utiliser un ensemble pour stocker les alertes déjà affichées

    def recuperer_alertes_vaccins(self):
        """Récupère les alertes de rappel de vaccins depuis la base de données."""
        sql = "SELECT id_animal, nom_vaccin, date_prochain_rappel FROM vaccins WHERE date_prochain_rappel IS NOT NULL"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            rows = cursor.fetchall()
            self.alertes = [(row[0], row[1], row[2]) for row in rows]
        except sqlite3.Error as e:
            print(f"Erreur lors de la récupération des alertes : {e}")

    def verifier_alertes(self):
        """Vérifie les alertes et déclenche celles qui sont à venir."""
        now = datetime.now()
        alertes_a_afficher = []
        for alerte in self.alertes:
            id_animal, nom_vaccin, date_str = alerte
            try:
                date_alerte = datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                print(f"Format de date invalide : {date_str}")
                continue

            if now >= date_alerte and alerte not in self.alertes_affichees:
                alertes_a_afficher.append(alerte)
                self.alertes_affichees.add(alerte)  # Marquer l'alerte comme affichée

        # Afficher les alertes qui doivent l'être
        for alerte in alertes_a_afficher:
            self.afficher_popup(*alerte)

    def afficher_popup(self, id_animal, nom_vaccin, date):
        """Affiche un pop-up d'alerte."""
        root = tk.Tk()
        root.withdraw()  # Masquer la fenêtre principale
        messagebox.showinfo("Alerte", f"Alerte pour l'animal {id_animal} : Vaccin '{nom_vaccin}' prévu pour le {date}.")
        root.destroy()

    def verifier_et_afficher_alertes(self):
        """Méthode appelée depuis l'interface graphique pour vérifier les alertes."""
        self.recuperer_alertes_vaccins()
        self.verifier_alertes()
