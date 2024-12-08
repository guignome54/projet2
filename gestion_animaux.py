import sqlite3
import re  # Pour les validations avec expressions régulières
from sqlite3 import Error
from error_handling import DatabaseError, AnimalNotFoundError, NomError  # Assurez-vous que ces exceptions sont définies


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

    def ajouter_animal(self, nom, race, age, test_mode=False):
        """Ajoute un nouvel animal à la base de données après validation."""
        if not test_mode:
            if not re.match("^[a-zA-ZÀ-ÿ\\s]+$", nom):
                raise NomError("Le nom doit contenir uniquement des lettres et des espaces.")
        else:
            if not re.match("^[a-zA-ZÀ-ÿ0-9\\s]+$", nom):
                raise NomError("Le nom doit contenir uniquement des lettres, chiffres, et des espaces.")

        if not re.match("^[a-zA-ZÀ-ÿ\\s]+$", race):
            raise NomError("La race doit contenir uniquement des lettres et des espaces.")
        if not isinstance(age, int) or age < 0:
            raise ValueError("L'âge doit être un entier non négatif.")

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
                raise AnimalNotFoundError(f"L'animal avec l'ID {id_animal} n'existe pas.")
            return rows
        except Error as e:
            raise DatabaseError("Erreur lors de la consultation des animaux", e)

    def supprimer_animal(self, id_animal):
        """Supprime un animal de la base de données."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM animaux WHERE id = ?", (id_animal,))
            self.conn.commit()
            if cursor.rowcount == 0:
                raise AnimalNotFoundError(f"L'animal avec l'ID {id_animal} n'existe pas.")
            print(f"L'animal avec l'ID {id_animal} a été supprimé.")
        except Error as e:
            raise DatabaseError("Erreur lors de la suppression de l'animal.", e)

    def mettre_a_jour_animal(self, id_animal, nom=None, race=None, age=None):
        """Met à jour les informations d'un animal."""
        try:
            # Validation des entrées si elles sont fournies
            if nom and not re.match("^[a-zA-ZÀ-ÿ\\s]+$", nom):
                raise NomError("Le nom doit contenir uniquement des lettres et des espaces.")
            if race and not re.match("^[a-zA-ZÀ-ÿ\\s]+$", race):
                raise NomError("La race doit contenir uniquement des lettres et des espaces.")
            if age is not None and (not isinstance(age, int) or age < 0):
                raise ValueError("L'âge doit être un entier non négatif.")

            # Construction dynamique de la requête SQL
            updates = []
            params = []
            if nom:
                updates.append("nom = ?")
                params.append(nom)
            if race:
                updates.append("race = ?")
                params.append(race)
            if age is not None:
                updates.append("age = ?")
                params.append(age)

            params.append(id_animal)
            sql = f"UPDATE animaux SET {', '.join(updates)} WHERE id = ?"

            cursor = self.conn.cursor()
            cursor.execute(sql, params)
            self.conn.commit()

            if cursor.rowcount == 0:
                raise AnimalNotFoundError(f"L'animal avec l'ID {id_animal} n'existe pas.")
            print(f"L'animal avec l'ID {id_animal} a été mis à jour.")
        except Error as e:
            raise DatabaseError("Erreur lors de la mise à jour de l'animal.", e)
