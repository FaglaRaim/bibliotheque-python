class Livre:
    def __init__(self, id_livre, titre, auteur, quantite):
        self.id = id_livre
        self.titre = titre
        self.auteur = auteur
        self.quantite = quantite

    def __str__(self):
        return f"{self.id} - {self.titre} ({self.auteur}) [Stock: {self.quantite}]"