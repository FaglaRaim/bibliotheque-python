# 👨‍💻 Auteur : FAGLA CHADARE

# 📚 Système de Gestion de Bibliothèque en Python

---

## 👨‍💻 Présentation du projet

Ce projet est une application console développée en **Python** permettant de gérer une bibliothèque numérique.

Il a été réalisé dans un but pédagogique afin de pratiquer :
- la programmation orientée objet (POO)
- la gestion des utilisateurs
- la manipulation de données
- la logique de développement d’un système réel

---

## 🎯 Objectif

Créer une application capable de :
- gérer des utilisateurs
- gérer un catalogue de livres
- permettre l’emprunt et le retour de livres
- sécuriser les actions via une connexion utilisateur

---

## 🚀 Fonctionnalités

### 👤 Gestion des utilisateurs
- Inscription avec :
  - Nom
  - Prénom
  - Email unique
- Connexion / Déconnexion
- Système de session utilisateur

---

### 📚 Gestion des livres
- Affichage des livres disponibles
- 10 livres préchargés dans le système
- Gestion du stock de chaque livre

---

### 📖 Emprunt et retour
- Emprunt possible uniquement si l’utilisateur est connecté
- Vérification du stock disponible
- Retour de livres avec mise à jour du stock

---

### ⚠️ Sécurité et validation
- Email unique (pas de doublon)
- Connexion obligatoire pour emprunter
- Validation des entrées utilisateur (chiffres uniquement dans le menu)

---

## 🧠 Concepts utilisés

- Programmation Orientée Objet (POO)
- Classes et objets
- Listes
- Conditions et boucles
- Gestion de session utilisateur
- Validation des entrées utilisateur

---

## 🛠️ Technologies utilisées

- Python 3

---

## 📁 Structure du projet

- main.py → Menu principal
- bibliotheque.py → Gestion logique
- livre.py → Classe Livre
- utilisateur.py → Classe Utilisateur
