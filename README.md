# Be Strong Gym 

Un simulateur de salle de gym interactif développé en Python avec Pygame. Progressez à travers différents exercices, améliorez votre niveau physique et accumulez des pièces.

## Description

Be Strong Gym est un jeu de simulation où vous incarnez un personnage s'entraînant dans une salle de gym. Vous devez parcourir les équipements disponibles (banc, traction, sac de frappe) pour accumuler de l'expérience, progresser de niveau et gagner des pièces.

### Fonctionnalités

- Trois exercices différents avec des mécaniques uniques
- Système de progression de niveau avec déblocage d'équipements
- Gestion de l'énergie et de la monnaie
- Interface utilisateur interactive
- Système de son et musique
- Animations fluides
- State management centralisé

## Architecture

Le projet suit une architecture simple avec séparation des responsabilités :

- **main.py** : Point d'entrée principal et boucle de jeu
- **logic.py** : Logique métier et gestion d'état du jeu
- **view.py** : Affichage et rendu graphique
- **resources.py** : Chargement des assets et ressources
- **settings.py** : Configuration et constantes
- **assets/** : Ressources graphiques
- **sounds/** : Ressources audio

## Prérequis

- Python 3.8+
- Pygame
- Les dépendances listées dans l'environnement virtuel

## Installation

1. Clonez ou téléchargez le projet
2. Créez un environnement virtuel :
   ```bash
   python3 -m venv venvir
   ```

3. Activez l'environnement virtuel :
   ```bash
   source venvir/bin/activate
   ```

4. Installez les dépendances :
   ```bash
   pip3 install pygame
   ```

## Utilisation

Lancez le jeu avec :
```bash
python3 main.py
```

## Contrôles

- Utilisez les touches directionnelles ou WASD pour vous déplacer
- Approchez-vous des équipements pour interagir
- Validez vos actions avec la barre d'espace
- Utiliser la touche E pour changer d'exercices

## Structure des Données

Le jeu utilise un objet Context pour partager les données entre les différents modules :

```python
context.data = {
    'player_level': int,           # Niveau actuel
    'current_exercise': str,       # Exercice en cours
    'energy': int,                 # Énergie disponible
    'coins': int,                  # Pièces accumulées
    'exercises': dict,             # Données de progression par exercice
    ...
}
```

## Configuration

Les paramètres du jeu se trouvent dans `settings.py` :

- `SCREEN_WIDTH`, `SCREEN_HEIGHT` : Dimension de la fenêtre
- `FPS` : Images par seconde
- `LOADING_DURATION` : Durée d'écran de chargement
- Positions et couleurs des éléments

## Système de Progression

Le jeu propose une progression naturelle :

1. **Banc (Bench)** : Premier exercice, déverrouillé au démarrage
2. **Traction** : Débloqué au niveau 2
3. **Sac de frappe (Bag)** : Débloqué au niveau 3

Chaque exercice a son propre système de progression avec des objectifs croissants.

## Gestion de l'Énergie

- Le joueur commence chaque session avec une quantité d'énergie limitée
- Chaque action consomme de l'énergie
- L'énergie se régénère ou peut être restaurée via le distributeur
- Quand l'énergie atteint zéro, la session se termine

## Distribution de Pièces

Les pièces peuvent être gagnées :
- En accomplissant les objectifs des exercices
- En progressant de niveau
- Via le distributeur (échange d'énergie)


## Fichiers Importants

- [main.py](main.py) : Initialisation et boucle principale
- [logic.py](logic.py) : Cœur de la logique du jeu
- [view.py](view.py) : Système de rendu
- [settings.py](settings.py) : Configuration centralisée

## Améliorations Potentielles

- Sauvegarde/Chargement de progression
- Système de quêtes
- Multiples personnages
- Classements et statistiques
- Mode multijoueur local

## License

Non spécifiée

## Support

Pour toute question ou problème, veuillez consulter la structure du code ou modifier les settings selon vos besoins.
