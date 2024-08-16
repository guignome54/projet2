import sqlite3
from sqlite3 import Error
from error_handling import *


class GestionVaccins:
    def __init__(self, conn):
        """Initialise le module de gestion des vaccins."""
        self.conn = conn
        self.create_table()

    def create_table(self):
        """Crée la table des vaccins si elle n'existe pas déjà."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS vaccins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_animal INTEGER NOT NULL,
            nom_vaccin TEXT NOT NULL,
            date_vaccin TEXT NOT NULL,
            date_prochain_rappel TEXT NOT NULL,
            FOREIGN KEY (id_animal) REFERENCES animaux (id)
        );
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'vaccins' créée ou déjà existante.")
        except Error as e:
            raise DatabaseError("Erreur de création de la table des vaccins", e)

    def ajouter_vaccin(self, id_animal, nom_vaccin, date_vaccin, date_prochain_rappel):
        """Ajoute un vaccin pour un animal spécifique."""
        try:
            NomAnimal(nom_vaccin)
        except NomAnimal as e:
            raise NomError(str(e))        
        sql = '''INSERT INTO vaccins(id_animal, nom_vaccin, date_vaccin, date_prochain_rappel)
                 VALUES(?, ?, ?, ?)'''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (id_animal, nom_vaccin, date_vaccin, date_prochain_rappel))
            self.conn.commit()
            print(f"Vaccin {nom_vaccin} ajouté pour l'animal {id_animal}.")
        except Error as e:
            raise DatabaseError("Erreur lors de l'ajout du vaccin à la base de données", e)

    def consulter_vaccins(self, id_animal=None):
        """Consulte tous les vaccins d'un animal donné par son ID ou tous les vaccins si ID est None."""
        sql = "SELECT * FROM vaccins"
        params = ()
        if id_animal:
            sql += " WHERE id_animal=?"
            params = (id_animal,)

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            return rows
        except Error as e:
            raise DatabaseError("Erreur lors de la consultation des vaccins", e)

    def supprimer_vaccin(self, nom_vaccin):
        """Supprime un animal de la base de données."""
        with self.conn:
            result = self.conn.execute("""
                DELETE FROM vaccins WHERE nom_vaccin = ?
            """, (nom_vaccin,))
            if result.rowcount == 0:
                raise AnimalNotFoundError(f"Le vaccin avec le nom {nom_vaccin} n'existe pas.")
