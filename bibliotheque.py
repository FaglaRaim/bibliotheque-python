from utilisateur import Utilisateur
from livre import Livre

class Bibliotheque:
    def __init__(self):
        self.livres = []
        self.utilisateurs = []
        self.next_id_user = 1
        self.utilisateur_connecte = None

    # 📚 ajouter livre
    def ajouter_livre(self, livre):
        self.livres.append(livre)

    # 👤 inscription avec email unique
    def inscrire_utilisateur(self, nom, prenom, email):

        for u in self.utilisateurs:
            if u.email == email:
                print("❌ Email déjà utilisé")
                return

        user = Utilisateur(self.next_id_user, nom, prenom, email)
        self.utilisateurs.append(user)

        print(f"✅ Inscription réussie ! ID : {user.id}")
        self.next_id_user += 1

    # 🔐 connexion
    def connexion(self, id_user):
        user = next((u for u in self.utilisateurs if u.id == id_user), None)

        if user:
            self.utilisateur_connecte = user
            print(f"🔓 Connecté : {user.nom} {user.prenom}")
        else:
            print("❌ Utilisateur introuvable")

    # 🚪 déconnexion
    def deconnexion(self):
        if self.utilisateur_connecte:
            print(f"🔒 Déconnecté : {self.utilisateur_connecte.nom}")
            self.utilisateur_connecte = None
        else:
            print("Aucun utilisateur connecté")

    # 📖 afficher livres
    def afficher_livres(self):
        for livre in self.livres:
            print(livre)

    # 📚 emprunter livre (avec session)
    def emprunter_livre(self, id_livre):

        if not self.utilisateur_connecte:
            print("⚠️ Vous devez vous connecter d'abord")
            return

        livre = next((l for l in self.livres if l.id == id_livre), None)

        if not livre:
            print("❌ Livre introuvable")
            return

        if livre.quantite <= 0:
            print("❌ Livre indisponible")
            return

        livre.quantite -= 1
        self.utilisateur_connecte.livres_empruntes.append(livre)

        print("📚 Emprunt réussi")