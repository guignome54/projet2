from fpdf import FPDF

class RapportPDF:
    def __init__(self, titre, gestion_animaux, gestion_soins, gestion_vaccins):
        self.pdf = FPDF()
        self.gestion_animaux = gestion_animaux
        self.gestion_soins = gestion_soins
        self.gestion_vaccins = gestion_vaccins
        self.pdf.add_page()
        self.pdf.set_font("Arial", "B", 16)
        self.pdf.cell(0, 10, titre, ln=True, align="C")

    def ajouter_texte(self, texte):
        """Ajoute du texte au PDF avec un formatage de base."""
        self.pdf.set_font("Arial", size=12)
        self.pdf.multi_cell(0, 10, texte)

    def generer_rapport_animaux_et_soins(self):
        """Génère un rapport combiné des animaux et de leurs soins."""
        animaux = self.gestion_animaux.consulter_animal()
        for animal in animaux:
            self.ajouter_texte(f"ID: {animal[0]}, Nom: {animal[1]}, Race: {animal[2]}, Âge: {animal[3]}")
            soins = self.gestion_soins.consulter_soins(animal[0])
            vaccins = self.gestion_vaccins.consulter_vaccins(animal[0])
            for soin in soins:
                self.ajouter_texte(f"    - Soin: {soin[2]}, Date: {soin[3]}, Description: {soin[4]}")
            for vaccin in vaccins: 
                self.ajouter_texte(f"    - Vaccin: {vaccin[2]}, Date administration {vaccin[3]}, date Alerte: {vaccin[4]} ")

        self.exporter_pdf("rapport_cheptel.pdf")

    def generate_vaccination_report(self):
        """Génère un rapport des vaccinations en format PDF."""
        try:
            vaccins = self.gestion_vaccins.consulter_vaccins()
            self.ajouter_texte("Rapport des Vaccinations")
            
            for vaccin in vaccins:
                self.ajouter_texte(f"ID: {vaccin[0]}, ID Animal: {vaccin[1]}, Nom du Vaccin: {vaccin[2]}")
                self.ajouter_texte(f"    - Date du Vaccin: {vaccin[3]}, Date du Prochain Rappel: {vaccin[4]}")

            self.exporter_pdf("rapport_vaccinations.pdf")
            print("Rapport des vaccinations généré avec succès : rapport_vaccinations.pdf")
        except Exception as e:
            print(f"Erreur lors de la génération du rapport des vaccinations : {e}")
    
    def generate_animal_report(self):
        """Génère un rapport des animaux en format PDF."""
        try:
            animaux = self.gestion_animaux.consulter_animal()
            self.ajouter_texte("Rapport des Animaux")
            
            for animal in animaux:
                self.ajouter_texte(f"ID: {animal[0]}, Nom: {animal[1]}, Race: {animal[2]}, Âge: {animal[3]}")

            self.exporter_pdf("rapport_animaux.pdf")
            print("Rapport des animaux généré avec succès : rapport_animaux.pdf")
        except Exception as e:
            print(f"Erreur lors de la génération du rapport des animaux : {e}")


    def exporter_pdf(self, nom_fichier):
        """Sauvegarde le PDF sous le nom spécifié."""
        self.pdf.output(nom_fichier)
        print(f"Rapport généré avec succès : {nom_fichier}")
