class Utilisateur:
    def __init__(self, id_user, nom, prenom, email):
        self.id = id_user
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.livres_empruntes = []

    def __str__(self):
        return f"{self.id} - {self.nom} {self.prenom} ({self.email})"