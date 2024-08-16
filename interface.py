import tkinter as tk
from tkinter import messagebox, simpledialog
from error_handling import *
from datetime import datetime

class InterfaceGUI:
    def __init__(self, gestion_animaux, gestion_soins, gestion_vaccins, gestion_alertes):
        """
        Initialise l'interface graphique avec les modules de gestion.

        :param gestion_animaux: Instance de la classe GestionAnimaux.
        :param gestion_soins: Instance de la classe GestionSoins.
        :param gestion_vaccins: Instance de la classe GestionVaccins.
        """
        self.gestion_animaux = gestion_animaux
        self.gestion_soins = gestion_soins
        self.gestion_vaccins = gestion_vaccins
        self.gestion_alertes = gestion_alertes
        self.root = tk.Tk()
        self.root.title("Gestion de Cheptel")
        self.label = tk.Label(self.root, text="Bienvenue dans l'interface de gestion")
        self.label.pack(padx=20, pady=20)

        # Lancer la vérification des alertes au démarrage
        self.verifier_alertes()

        # Ajouter des boutons pour les fonctionnalités principales
        tk.Button(self.root, text="Ajouter Animal", command=self.ajouter_animal_gui).pack(pady=5)
        tk.Button(self.root, text="Consulter Animaux", command=self.consulter_animaux_gui).pack(pady=5)
        tk.Button(self.root, text="Ajouter Soin", command=self.ajouter_soin_gui).pack(pady=5)
        tk.Button(self.root, text="Voir Soins", command=self.voir_soins_gui).pack(pady=5)
        tk.Button(self.root, text="Ajouter Vaccin", command=self.ajouter_vaccin_gui).pack(pady=5)
        tk.Button(self.root, text="Voir Vaccins", command=self.voir_vaccins_gui).pack(pady=5)

    def verifier_alertes(self):
        """Vérifie les alertes et affiche les pop-ups si nécessaire."""
        self.gestion_alertes.verifier_et_afficher_alertes()
        # Optionnel : Vérifier à des intervalles réguliers (ex. toutes les minutes)
        self.root.after(60000, self.verifier_alertes) 

    def ajouter_animal_gui(self):
        """Ouvre une fenêtre pour ajouter un animal."""
        new_window = tk.Toplevel(self.root)
        new_window.title("Ajouter Animal")

        frame = tk.Frame(new_window)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Nom:").grid(row=0)
        tk.Label(frame, text="Race:").grid(row=1)
        tk.Label(frame, text="Âge:").grid(row=2)

        nom = tk.Entry(frame)
        race = tk.Entry(frame)
        age = tk.Entry(frame)

        nom.grid(row=0, column=1)
        race.grid(row=1, column=1)
        age.grid(row=2, column=1)

        def submit():
            try:
                self.gestion_animaux.ajouter_animal(nom.get(), race.get(), int(age.get()))
                messagebox.showinfo("Succès", "Animal ajouté avec succès!")
                new_window.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "L'âge doit être un nombre entier.")
            except DatabaseError as e:
                messagebox.showerror("Erreur de base de données", str(e))

        tk.Button(frame, text="Ajouter", command=submit).grid(row=4, column=1, pady=10)

        # Ajout du bouton de suppression
        def supprimer_animal():
            try:
                id_animal = tk.simpledialog.askinteger("Supprimer Animal", "Entrez l'ID de l'animal à supprimer:")
                if id_animal:
                    self.gestion_animaux.supprimer_animal(id_animal)
                    messagebox.showinfo("Succès", "Animal supprimé avec succès!")
            except ValueError:
                messagebox.showerror("Erreur", "L'ID doit être un nombre entier.")
            except AnimalNotFoundError as e:
                messagebox.showerror("Erreur", str(e))
            except DatabaseError as e:
                messagebox.showerror("Erreur de base de données", str(e))

        tk.Button(frame, text="Supprimer Animal", command=supprimer_animal).grid(row=5, column=1, pady=10)

    def consulter_animaux_gui(self):
        """Ouvre une fenêtre pour consulter les animaux."""
        new_window = tk.Toplevel(self.root)
        new_window.title("Consulter Animaux")

        frame = tk.Frame(new_window)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="ID Animal (laisser vide pour tout voir):").grid(row=0, column=0)
        id_animal = tk.Entry(frame)
        id_animal.grid(row=0, column=1)

        def submit():
            try:
                id_value = id_animal.get()
                animaux = self.gestion_animaux.consulter_animal(id_value if id_value else None)
                for widget in frame.winfo_children():
                    widget.destroy()
                tk.Label(frame, text="ID | Nom | Race | Âge | État de Santé").grid(row=0, column=0, columnspan=2)
                for i, animal in enumerate(animaux, start=1):
                    tk.Label(frame, text=" | ".join(map(str, animal))).grid(row=i, column=0, columnspan=2)
            except AnimalNotFoundError as e:
                messagebox.showerror("Erreur", str(e))
            except ValueError:
                messagebox.showerror("Erreur", "L'ID doit être un nombre entier.")
            except DatabaseError as e:
                messagebox.showerror("Erreur de base de données", str(e))

        tk.Button(frame, text="Consulter", command=submit).grid(row=1, column=1, pady=10)

    def ajouter_soin_gui(self):
        """Ouvre une fenêtre pour ajouter un soin."""
        new_window = tk.Toplevel(self.root)
        new_window.title("Ajouter Soin")

        frame = tk.Frame(new_window)
        frame.pack(padx=10, pady=10)

        today = datetime.today().strftime('%Y-%m-%d')
        tk.Label(frame, text="ID Animal:").grid(row=0, column=0)
        tk.Label(frame, text="Type de Soin:").grid(row=1, column=0)
        tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0)
        tk.Label(frame, text="Maladie:").grid(row=3, column=0)
        tk.Label(frame, text="Symptômes:").grid(row=4, column=0)
        tk.Label(frame, text="Description:").grid(row=5, column=0)

        id_animal = tk.Entry(frame)
        type_soin = tk.Entry(frame)
        date = tk.Entry(frame)
        maladie = tk.Entry(frame)
        symptomes = tk.Entry(frame)
        description = tk.Entry(frame)

        date.insert(0, today)

        id_animal.grid(row=0, column=1)
        type_soin.grid(row=1, column=1)
        date.grid(row=2, column=1)
        maladie.grid(row=3, column=1)
        symptomes.grid(row=4, column=1)
        description.grid(row=5, column=1)

        def submit():
            try:
                self.gestion_soins.ajouter_soin(
                    int(id_animal.get()), 
                    type_soin.get(), 
                    date.get(), 
                    description.get(), 
                    maladie.get(), 
                    symptomes.get()
                )
                messagebox.showinfo("Succès", "Soin ajouté avec succès!")
                new_window.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "L'ID doit être un nombre entier.")
            except DatabaseError as e:
                messagebox.showerror("Erreur de base de données", str(e))

        tk.Button(frame, text="Ajouter", command=submit).grid(row=6, column=1, pady=10)

        # Ajout du bouton de suppression
        def supprimer_soin():
            try:
                id_soin = tk.simpledialog.askstring("Supprimer Soin", "Entrez le nom du soin à supprimer:")
                if id_soin:
                    self.gestion_soins.supprimer_soin(id_soin)
                    messagebox.showinfo("Succès", "Soin supprimé avec succès!")
            except ValueError:
                messagebox.showerror("Erreur", "L'ID doit être un nombre entier.")
            except SoinNotFoundError as e:
                messagebox.showerror("Erreur", str(e))
            except DatabaseError as e:
                messagebox.showerror("Erreur de base de données", str(e))

        tk.Button(frame, text="Supprimer Soin", command=supprimer_soin).grid(row=7, column=1, pady=10)

    def voir_soins_gui(self):
        """Ouvre une fenêtre pour voir les soins d'un animal."""
        new_window = tk.Toplevel(self.root)
        new_window.title("Voir Soins")

        frame = tk.Frame(new_window)
        frame.pack(padx=10, pady=10)

  
        tk.Label(frame, text="ID Animal (laisser vide pour tout voir):").grid(row=0, column=0)
        id_animal = tk.Entry(frame)
        id_animal.grid(row=0, column=1)

        def submit():
            try:
                id_value = id_animal.get()
                soins = self.gestion_soins.consulter_soins(id_value if id_value else None)
                for widget in frame.winfo_children():
                    widget.destroy()
                tk.Label(frame, text="ID | Type de Soin | Date | Description").grid(row=0, column=0, columnspan=2)
                for i, soin in enumerate(soins, start=1):
                    tk.Label(frame, text=" | ".join(map(str, soin))).grid(row=i, column=0, columnspan=2)
            except ValueError:
                messagebox.showerror("Erreur", "L'ID doit être un nombre entier.")
            except DatabaseError as e:
                messagebox.showerror("Erreur de base de données", str(e))

        tk.Button(frame, text="Voir Soins", command=submit).grid(row=1, column=1, pady=10)

    def ajouter_vaccin_gui(self):
        """Ouvre une fenêtre pour ajouter un vaccin."""
        new_window = tk.Toplevel(self.root)
        new_window.title("Ajouter Vaccin")

        frame = tk.Frame(new_window)
        frame.pack(padx=10, pady=10)

        today = datetime.today().strftime('%Y-%m-%d')

        tk.Label(frame, text="ID Animal:").grid(row=0, column=0)
        tk.Label(frame, text="Nom du Vaccin:").grid(row=1, column=0)
        tk.Label(frame, text="Date du Vaccin (YYYY-MM-DD):").grid(row=2, column=0)
        tk.Label(frame, text="Date du Prochain Rappel (YYYY-MM-DD):").grid(row=3, column=0)

        id_animal = tk.Entry(frame)
        nom_vaccin = tk.Entry(frame)
        date_vaccin = tk.Entry(frame)
        date_prochain_rappel = tk.Entry(frame)

        date_vaccin.insert(0, today)
        id_animal.grid(row=0, column=1)
        nom_vaccin.grid(row=1, column=1)
        date_vaccin.grid(row=2, column=1)
        date_prochain_rappel.grid(row=3, column=1)

        def submit():
            try:
                self.gestion_vaccins.ajouter_vaccin(int(id_animal.get()), nom_vaccin.get(), date_vaccin.get(), date_prochain_rappel.get())
                messagebox.showinfo("Succès", "Vaccin ajouté avec succès!")
                new_window.destroy()
            except ValueError:
                messagebox.showerror("Erreur", "L'ID doit être un nombre entier.")
            except DatabaseError as e:
                messagebox.showerror("Erreur de base de données", str(e))

        tk.Button(frame, text="Ajouter", command=submit).grid(row=4, column=1, pady=10)

        # Ajout du bouton de suppression
        def supprimer_vaccin():
            id_vaccin = tk.simpledialog.askstring("Supprimer Vaccin", "Entrez le nom du vaccin à supprimer:")
            if id_vaccin is not None : 
                try :
                        self.gestion_vaccins.supprimer_vaccin(id_vaccin)
                        messagebox.showinfo("Succès", "Vaccin supprimé avec succès!")
                except VaccinNotFoundError as e:
                    messagebox.showerror("Erreur", str(e))
                except DatabaseError as e:
                    messagebox.showerror("Erreur de base de données", str(e))

        tk.Button(frame, text="Supprimer Vaccin", command=supprimer_vaccin).grid(row=5, column=1, pady=10)

    def voir_vaccins_gui(self):
        """Ouvre une fenêtre pour voir les vaccins d'un animal."""
        new_window = tk.Toplevel(self.root)
        new_window.title("Voir Vaccins")

        frame = tk.Frame(new_window)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="ID Animal (laisser vide pour tout voir):").grid(row=0, column=0)
        id_animal = tk.Entry(frame)
        id_animal.grid(row=0, column=1)

        def submit():
            try:
                id_value = id_animal.get()
                vaccins = self.gestion_vaccins.consulter_vaccins(id_value if id_value else None)
                for widget in frame.winfo_children():
                    widget.destroy()
                tk.Label(frame, text="ID | Nom du Vaccin | Date du Vaccin | Date du Prochain Rappel").grid(row=0, column=0, columnspan=2)
                for i, vaccin in enumerate(vaccins, start=1):
                    tk.Label(frame, text=" | ".join(map(str, vaccin))).grid(row=i, column=0, columnspan=2)
            except ValueError:
                messagebox.showerror("Erreur", "L'ID doit être un nombre entier.")
            except DatabaseError as e:
                messagebox.showerror("Erreur de base de données", str(e))

        tk.Button(frame, text="Voir Vaccins", command=submit).grid(row=1, column=1, pady=10)

    def run(self):
        """Démarre l'interface graphique."""
        self.root.mainloop()
