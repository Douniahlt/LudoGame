# Jeu de Ludo

## Description
Ce projet est une implémentation du jeu de Ludo (aussi connu sous le nom de "Petits Chevaux" en français ou "Parcheesi" dans certains pays) en utilisant Python et Tkinter. C'est un jeu de plateau classique où chaque joueur essaie d'amener ses quatre pions de sa base à sa maison en suivant un parcours sur le plateau.

## Fonctionnalités
- Interface graphique complète avec menu d'accueil
- Prise en charge de 1 à 4 joueurs humains
- Intelligence artificielle pour jouer contre l'ordinateur
- Animation des mouvements des pions
- Effets visuels (lancement de dé, surbrillance des pions jouables)
- Règles complètes incluant les captures, les cases étoiles (protégées), etc.

## Comment jouer
1. Exécutez le fichier `LudoGame.py` pour lancer le jeu
2. Sur l'écran d'accueil, cliquez sur le bouton "COMMENCER"
3. Sélectionnez le nombre de joueurs humains (1-4)
4. À votre tour, cliquez sur "LANCER LE DÉ", puis sélectionnez un pion à déplacer
5. Le premier joueur à amener ses 4 pions à sa maison gagne!

## Règles principales
- Lancez un dé pour déplacer vos pions
- Vous devez faire un 6 pour sortir un pion de votre base
- Si vous faites un 6, vous rejouez (jusqu'à 3 fois consécutives maximum)
- Lorsque vous atterrissez sur un pion adverse, vous le renvoyez à sa base
- Les cases étoiles protègent les pions des captures
- Vous devez amener tous vos pions dans votre maison pour gagner

## Problèmes connus
⚠️ **Attention** : Il existe quelques problèmes avec l'affichage et les déplacements sur le plateau :
- Certaines parties du chemin coloré (notamment le chemin vert) peuvent ne pas s'afficher correctement
- Certains déplacements peuvent ne pas être calculés correctement dans des situations spécifiques
- Les coordonnées de certains éléments visuels peuvent être décalées

## Prérequis
- Python 3.6 ou supérieur
- Bibliothèque Tkinter (généralement incluse avec Python)
- Bibliothèque PIL/Pillow pour la gestion des images (`pip install pillow`)

## Installation
1. Clonez ce dépôt ou téléchargez les fichiers
2. Assurez-vous d'avoir les prérequis installés
3. Placez votre image `ludo_board.png` dans le même dossier que les scripts
4. Exécutez `LudoGame.py`

```bash
python main.py
```

## Améliorations futures
- Correction des problèmes d'affichage des chemins colorés
- Ajustement correct de la position des flèches directionnelles
- Ajout d'une option pour sauvegarder/charger une partie
- Amélioration de l'intelligence artificielle
- Ajout d'effets sonores
- Support pour le jeu en réseau

## Crédits
Développé comme projet éducatif pour apprendre Python et Tkinter.
