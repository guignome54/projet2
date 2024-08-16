import unittest
from gestion_animaux import GestionAnimaux, DatabaseError, AnimalNotFoundError
import os

class TestGestionAnimaux(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_file = "test_cheptel.db"
        cls.gestion_animaux = GestionAnimaux(cls.db_file)

    def test_ajouter_animal(self):
        self.gestion_animaux.ajouter_animal("Rex", "Berger Allemand", 5, "Bon")
        animaux = self.gestion_animaux.consulter_animal(1)  # Supposons que l'ID est 1
        self.assertEqual(animaux[0][1], "Rex")

    def test_consulter_animal_not_found(self):
        with self.assertRaises(AnimalNotFoundError):
            self.gestion_animaux.consulter_animal(999)  # ID fictif

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.db_file)  # Nettoyage après les tests

if __name__ == '__main__':
    unittest.main()
