import re

class DatabaseError(Exception):
    """Exception levée pour les erreurs liées à la base de données."""

    def __init__(self, message, code=None):
        """
        Initialise l'exception avec un message et un code d'erreur optionnel.

        :param message: Message d'erreur à afficher.
        :param code: Code d'erreur associé (optionnel).
        """
        super().__init__(message)
        self.code = code

    def __str__(self):
        if self.code:
            return f"{self.args[0]} (Code: {self.code})"
        return self.args[0]

class AnimalNotFoundError(Exception):
    """Exception levée lorsque l'animal n'est pas trouvé."""

    def __init__(self, animal_id):
        """
        Initialise l'exception avec l'ID de l'animal non trouvé.

        :param animal_id: ID de l'animal qui n'a pas été trouvé.
        """
        super().__init__(f"Animal avec ID {animal_id} non trouvé.")
        self.animal_id = animal_id

    def __str__(self):
        return self.args[0]

class AnimalAlreadyExistsError(Exception):
    """Exception levée lorsque l'animal existe déjà."""

    def __init__(self, animal_name):
        """
        Initialise l'exception avec le nom de l'animal existant.

        :param animal_name: Nom de l'animal qui existe déjà.
        """
        super().__init__(f"Animal avec le nom '{animal_name}' existe déjà.")
        self.animal_name = animal_name

    def __str__(self):
        return self.args[0]

class NomError(Exception):
    """Exception levée pour les erreurs de validation du nom de l'animal."""
    pass

class NomAnimal:
    """Classe pour gérer et valider les noms des animaux."""

    def __init__(self, nom):
        """
        Initialise la classe avec un nom d'animal et valide ce nom.

        :param nom: Nom de l'animal à valider.
        :raises NomError: Si le nom n'est pas valide.
        """
        self.nom = nom
        self.valider_nom()

    def valider_nom(self):
        """Valide le nom de l'animal."""
        if not self.nom:
            raise NomError("Le nom de l'animal ne peut pas être vide.")
        if not isinstance(self.nom, str):
            raise NomError("Le nom de l'animal doit être une chaîne de caractères.")
        if not re.match(r'^[a-zA-Z\s]+$', self.nom):
            raise NomError("Le nom de l'animal ne peut contenir que des lettres et des espaces.")
        if len(self.nom) > 50:
            raise NomError("Le nom de l'animal ne peut pas dépasser 50 caractères.")

class SoinNotFoundError(Exception):
    """Exception levée lorsque le soin n'est pas trouvé dans la base de données."""
    def __init__(self, message="Soin non trouvé."):
        self.message = message
        super().__init__(self.message)

class VaccinNotFoundError(Exception):
    """Exception levée lorsque le vaccin n'est pas trouvé dans la base de données."""
    def __init__(self, message="Vaccin non trouvé."):
        self.message = message
        super().__init__(self.message)