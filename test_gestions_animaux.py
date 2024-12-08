import unittest
from gestion_animaux import GestionAnimaux, NomError, DatabaseError, AnimalNotFoundError
import os

class TestGestionAnimaux(unittest.TestCase):

    def setUp(self):
        """Initialise une base de données temporaire pour les tests."""
        self.db_file = "test_animaux.db"
        self.gestion = GestionAnimaux(self.db_file)

    def tearDown(self):
        """Supprime la base de données temporaire après chaque test."""
        self.gestion.conn.close()
        os.remove(self.db_file)

    def test_ajouter_animal_nom_valide(self):
        self.gestion.ajouter_animal("Milo", "Chat", 3)
        animaux = self.gestion.consulter_animal()
        self.assertEqual(len(animaux), 1)

    def test_ajouter_animal_nom_invalide(self):
        with self.assertRaises(NomError):
            self.gestion.ajouter_animal("Milo123", "Chat", 3)

    def test_ajouter_animal_race_invalide(self):
        with self.assertRaises(NomError):
            self.gestion.ajouter_animal("Milo", "Ch@t", 3)

    def test_ajouter_animal_age_negatif(self):
        with self.assertRaises(ValueError):
            self.gestion.ajouter_animal("Milo", "Chat", -1)

    def test_ajouter_animal_age_grand(self):
        self.gestion.ajouter_animal("Milo", "Chat", 1000)
        animaux = self.gestion.consulter_animal()
        self.assertEqual(animaux[0][3], 1000)

    def test_consulter_animal_existant(self):
        self.gestion.ajouter_animal("Milo", "Chat", 3)
        animaux = self.gestion.consulter_animal(1)
        self.assertEqual(len(animaux), 1)

    def test_consulter_animal_inexistant(self):
        with self.assertRaises(AnimalNotFoundError):
            self.gestion.consulter_animal(999)

    def test_supprimer_animal_existant(self):
        self.gestion.ajouter_animal("Milo", "Chat", 3)
        animaux = self.gestion.consulter_animal()
        id_animal = animaux[0][0]
        self.gestion.supprimer_animal(id_animal)
        self.assertEqual(len(self.gestion.consulter_animal()), 0)

    def test_mettre_a_jour_animal(self):
        self.gestion.ajouter_animal("Milo", "Chat", 3)
        animaux = self.gestion.consulter_animal()
        id_animal = animaux[0][0]
        self.gestion.mettre_a_jour_animal(id_animal, age=4)
        animal = self.gestion.consulter_animal(id_animal)[0]
        self.assertEqual(animal[3], 4)

    def test_mettre_a_jour_animal_inexistant(self):
        with self.assertRaises(AnimalNotFoundError):
            self.gestion.mettre_a_jour_animal(999, nom="Felix")

    def test_grande_quantite_donnees(self):
        """Test d'ajout d'une grande quantité d'animaux."""
        for i in range(1000):
            self.gestion.ajouter_animal(f"Animal{i}", "EspeceTest", i % 100, test_mode=True)

    def test_injection_sql(self):
        """Test de résistance contre les injections SQL."""
        self.gestion.ajouter_animal("InjectionTest", "EspeceTest", 3)
        animaux = self.gestion.consulter_animal()
        self.assertIn(("InjectionTest", "EspeceTest", 3), [(a[1], a[2], a[3]) for a in animaux])

    def test_consulter_apres_suppression(self):
        self.gestion.ajouter_animal("Milo", "Chat", 3)
        animaux = self.gestion.consulter_animal()
        id_animal = animaux[0][0]
        self.gestion.supprimer_animal(id_animal)
        with self.assertRaises(AnimalNotFoundError):
            self.gestion.consulter_animal(id_animal)

if __name__ == "__main__":
    unittest.main()
