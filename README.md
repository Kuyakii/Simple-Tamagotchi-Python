# Projet Tamagotchi - Simulation d’animaux virtuels

Projet personnel réalisé à titre académique (année 2023-2024).  
Développé seul avec **Python** et **pygame**, en s’appuyant sur un sujet officiel de SAE.

---

## Présentation

Ce jeu Tamagotchi propose une interface graphique interactive permettant de gérer jusqu’à **6 animaux virtuels**.

Chaque animal possède 3 jauges principales :
- Enthousiasme
- Faim
- Fatigue
- Point de Vie

### Fonctionnalités implémentées :
- Actions : **Manger**, **Jouer**, **Sieste**
- Boutique interactive avec des **objets achetables**
- Plusieurs **salles** (salon, salle à manger, salle de jeux)
- **Système de pièces (coins)** à gagner via mini-jeux
- **Pause / Reprise** du jeu à tout moment
- **Bagarre** entre les tamagotchis une fois enthousiasme nul, ce qui fait perdre des points de vie"
- 3 mini-jeux intégrés :
  - Balle rebondissante
  - Air Hockey
  - Pierre-Feuille-Ciseaux

> Aucun système de sauvegarde n’est intégré.

---

## 🛠️ Technologies utilisées

- Python 3.x
- Pygame
- time / random

---

## 🗂️ Structure du projet

```plaintext
TAMAGOTCHI/
├── images/                # Assets (sprites, icônes, background)
│   ├── tamagotchis/       # Images des personnages
│   ├── shop/              # Icônes du magasin
│   ├── minigames/         # Graphismes mini-jeux
│   └── ...
│
├── mini_games/
│   ├── airhockey.py
│   ├── bounceball.py
│   ├── rpc.py             # Pierre Feuille Ciseaux
│   └── ...
│
├── constants.py
├── event.py
├── game.py
├── interface.py
├── tamagotchi.py
├── minigames.py
└── main.py                # Point d’entrée principal
```

---

## 🚀 Lancement

1. S’assurer que `pygame` est installé :
```bash
pip install pygame
```

2. Lancer le jeu :
```bash
python main.py
```

> L’interface graphique s’ouvre automatiquement avec tous les personnages.

---

## Auteurs

Projet réalisé seul par **Willien HU**.  
Initialement pensé pour accompagner un camarade sur le sujet de projet officiel.

---

## 📄 Licence

Usage académique uniquement – Ne pas utiliser en production.
