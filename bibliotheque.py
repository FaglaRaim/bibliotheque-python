from datetime import datetime


class Bibliotheque:
    def __init__(self):
        self.livres = []
        self.utilisateurs = []
        self.next_id = 1
        self.next_livre_id = 1
        self.user_connecte = None

    def ajouter_livre(self, titre, auteur="", genre="", quantite=5):
        livre = {
            "id": self.next_livre_id,
            "titre": titre,
            "auteur": auteur,
            "genre": genre,
            "quantite": quantite,
            "quantite_initiale": quantite,
        }
        self.livres.append(livre)
        self.next_livre_id += 1
        return livre

    def inscrire(self, nom, prenom, email):
        if not nom.strip() or not prenom.strip() or not email.strip():
            return False, "Tous les champs sont obligatoires."
        if "@" not in email or "." not in email:
            return False, "Adresse email invalide."
        for u in self.utilisateurs:
            if u["email"].lower() == email.lower():
                return False, "Cet email est déjà utilisé."
        user = {
            "id": self.next_id,
            "nom": nom.strip(),
            "prenom": prenom.strip(),
            "email": email.strip().lower(),
            "emprunts": [],
            "date_inscription": datetime.now().strftime("%d/%m/%Y"),
        }
        self.utilisateurs.append(user)
        self.next_id += 1
        return True, f"Bienvenue, {prenom} !"

    def login(self, email):
        if not email.strip():
            return False, "Veuillez saisir votre email."
        for u in self.utilisateurs:
            if u["email"] == email.strip().lower():
                self.user_connecte = u
                return True, f"Bonjour, {u['prenom']} !"
        return False, "Aucun compte associé à cet email."

    def logout(self):
        self.user_connecte = None

    def emprunter(self, livre_id):
        if not self.user_connecte:
            return "no_user", "Vous devez être connecté pour emprunter."
        for l in self.livres:
            if l["id"] == livre_id:
                if l["quantite"] <= 0:
                    return "unavailable", f"« {l['titre']} » est indisponible."
                l["quantite"] -= 1
                emprunt = {**l, "date_emprunt": datetime.now().strftime("%d/%m/%Y")}
                self.user_connecte["emprunts"].append(emprunt)
                return "ok", f"« {l['titre']} » emprunté avec succès !"
        return "not_found", "Livre introuvable."

    def retourner(self, livre_id):
        if not self.user_connecte:
            return False, "Non connecté."
        for emprunt in self.user_connecte["emprunts"]:
            if emprunt["id"] == livre_id:
                self.user_connecte["emprunts"].remove(emprunt)
                for l in self.livres:
                    if l["id"] == livre_id:
                        l["quantite"] += 1
                return True, f"« {emprunt['titre']} » retourné. Merci !"
        return False, "Ce livre ne figure pas dans vos emprunts."

    def stats(self):
        total_livres = sum(l["quantite_initiale"] for l in self.livres)
        empruntes = sum(l["quantite_initiale"] - l["quantite"] for l in self.livres)
        return {
            "total_titres": len(self.livres),
            "total_exemplaires": total_livres,
            "empruntes": empruntes,
            "membres": len(self.utilisateurs),
        }
