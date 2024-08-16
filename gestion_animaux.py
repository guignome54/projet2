import sqlite3
from sqlite3 import Error
from error_handling import *

class GestionAnimaux:
    def __init__(self, db_file):
        """Initialise la connexion à la base de données et crée la table."""
        self.conn = self.create_connection(db_file)
        self.create_table()

    def create_connection(self, db_file):
        """Crée une connexion à la base de données SQLite."""
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            print("Connexion établie à la base de données SQLite.")
        except Error as e:
            raise DatabaseError("Erreur de connexion à la base de données", e)
        return conn

    def create_table(self):
        """Crée la table des animaux si elle n'existe pas déjà."""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS animaux (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            race TEXT NOT NULL,
            age INTEGER
        );
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute(create_table_sql)
            self.conn.commit()
            print("Table 'animaux' créée ou déjà existante.")
        except Error as e:
            raise DatabaseError("Erreur de création de la table des animaux", e)

    def ajouter_animal(self, nom, race, age):
        """Ajoute un nouvel animal à la base de données après validation du nom."""
        try:
            # Validation du nom
            NomAnimal(nom)
        except NomAnimal as e:
            raise NomError(str(e))
        
        sql = '''INSERT INTO animaux(nom, race, age)
                 VALUES(?, ?, ?)'''
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, (nom, race, age))
            self.conn.commit()
            print(f"Animal {nom} ajouté à la base de données.")
        except Error as e:
            raise DatabaseError("Erreur lors de l'ajout de l'animal à la base de données", e)

    def consulter_animal(self, id_animal=None):
        """Consulte les détails d'un animal donné par son ID ou tous les animaux si ID est None."""
        sql = "SELECT * FROM animaux"
        params = ()
        if id_animal:
            sql += " WHERE id=?"
            params = (id_animal,)

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            if not rows and id_animal:
                raise AnimalNotFoundError(id_animal)
            return rows
        except Error as e:
            raise DatabaseError("Erreur lors de la consultation des animaux", e)
    
    def supprimer_animal(self, id_animal):
        """Supprime un animal de la base de données."""
        with self.conn:
            result = self.conn.execute("""
                DELETE FROM animaux WHERE id = ? """,(id_animal,))
            if result.rowcount == 0:
                raise AnimalNotFoundError(f"L'animal avecl'ID{id_animal}n'existe pas")
