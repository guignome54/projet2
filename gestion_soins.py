import sqlite3
from sqlite3 import Error
from error_handling import *

class GestionSoins:
    def __init__(self, conn):
        """Initialise le module de gestion des soins."""
        self.conn = conn
        self.create_table()

    def create_table(self):
        """Crée la table des soins si elle n'existe pas déjà."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS soins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_animal INTEGER NOT NULL,
            type_soin TEXT NOT NULL,
            maladie TEXT,
            symptomes TEXT,
            date_soin DATE,
            description TEXT,
            date_alerte TEXT,
            FOREIGN KEY (id_animal) REFERENCES animaux (id)
        );
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'soins' créée ou déjà existante.")
        except Error as e:
            raise DatabaseError("Erreur de création de la table des soins", e)

    def ajouter_soin(self, id_animal, type_soin, date_soin, description, maladie=None, symptomes=None):
        """Ajoute un soin pour un animal spécifique."""
        sql = '''INSERT INTO soins(id_animal, type_soin, date_soin, description, maladie, symptomes)
                 VALUES(?, ?, ?, ?, ?, ?)'''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (id_animal, type_soin, date_soin, description, maladie, symptomes))
            self.conn.commit()
            print(f"Soin {type_soin} ajouté pour l'animal {id_animal}.")
        except Error as e:
            raise DatabaseError("Erreur lors de l'ajout du soin à la base de données", e)

    def consulter_soins(self, id_animal=None):
        """Consulte tous les soins d'un animal donné par son ID ou tous les soins si ID est None."""
        sql = "SELECT * FROM soins"
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
            raise DatabaseError("Erreur lors de la consultation des soins", e)

    def supprimer_soin(self, id_soin):
        """Supprime un soin de la base de données."""
        with self.conn:
            result = self.conn.execute("""
                DELETE FROM soin WHERE id = ?
            """, (id_soin,))
            if result.rowcount == 0:
                raise SoinNotFoundError(f"Le soin avec l'ID {id_soin} n'existe pas.")
            
    def get_alerts(self, date):
        """Récupère les alertes programmées pour une date donnée."""
        sql = "SELECT id, type_soin FROM soins WHERE date_alerte=?"
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (date,))
            rows = cursor.fetchall()
            return rows
        except Error as e:
            raise DatabaseError("Erreur lors de la récupération des alertes", e)
