from bibliotheque import Bibliotheque
from livre import Livre

biblio = Bibliotheque()

# 📚 livres
biblio.ajouter_livre(Livre(1, "Python", "A1", 5))
biblio.ajouter_livre(Livre(2, "Algorithmique", "A2", 5))
biblio.ajouter_livre(Livre(3, "Base de données", "A3", 5))
biblio.ajouter_livre(Livre(4, "Réseaux", "A4", 5))
biblio.ajouter_livre(Livre(5, "IA", "A5", 5))

while True:
    print("\n===== MENU =====")
    print("1. Voir livres")
    print("2. S'inscrire")
    print("3. Connexion")
    print("4. Déconnexion")
    print("5. Emprunter")
    print("6. Quitter")

    choix = input("Choix : ")

    # ❌ validation chiffre
    if not choix.isdigit():
        print("❌ Veuillez entrer un chiffre")
        continue

    choix = int(choix)

    if choix == 1:
        biblio.afficher_livres()

    elif choix == 2:
        nom = input("Nom : ")
        prenom = input("Prénom : ")
        email = input("Email : ")
        biblio.inscrire_utilisateur(nom, prenom, email)

    elif choix == 3:
        id_user = input("ID : ")
        if not id_user.isdigit():
            print("❌ ID doit être un chiffre")
            continue
        biblio.connexion(int(id_user))

    elif choix == 4:
        biblio.deconnexion()

    elif choix == 5:
        id_livre = input("ID livre : ")
        if not id_livre.isdigit():
            print("❌ ID livre doit être un chiffre")
            continue
        biblio.emprunter_livre(int(id_livre))

    elif choix == 6:
        print("Au revoir 👋")
        break

    else:
        print("❌ Choix invalide")