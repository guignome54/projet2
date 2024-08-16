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

    def exporter_pdf(self, nom_fichier):
        """Sauvegarde le PDF sous le nom spécifié."""
        self.pdf.output(nom_fichier)
        print(f"Rapport généré avec succès : {nom_fichier}")
