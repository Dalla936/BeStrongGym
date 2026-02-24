import pygame
import sys
from settings import *
from resources import load_assets, load_sounds
from logic import init_game_state, handle_input, update_game
from view import draw_entities, draw_hud, draw_overlay_ui, draw_loading_screen

class Context:
    "Conteneur de données pour le jeu, partagé entre les fonctions."
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen
        self.data = {}

def main():
    """Point d'entrée principal du jeu."""
    
    # 1. Initialisation Pygame
    pygame.init()
    pygame.mixer.init()
    
    # 2. Création de la fenêtre
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Be Strong Gym - Simulator")
    clock = pygame.time.Clock()
    
    # 3. Initialisation du Contexte
    context = Context(SCREEN_WIDTH, SCREEN_HEIGHT, screen)
    
    # 4. Chargement des ressources
    print("Chargement des assets...")
    load_assets(context)
    load_sounds(context)
    
    # 5. Initialisation de l'état du jeu
    init_game_state(context)
    
    # 6. Boucle principale
    running = True
    while running:
        # Calcul du delta time en secondes
        etime = clock.tick(FPS) / 1000.0
        
        # --- Gestion des entrées ---
        if not handle_input(context, etime):
            running = False
            break
            
        # --- Mise à jour logique ---
        update_game(context, etime)
        
        # --- Rendu graphique ---
        # Fond d'écran
        if 'background' in context.data and context.data['background']:
            screen.blit(context.data['background'], (0, 0))
        else:
            screen.fill((45, 45, 60)) # Couleur de fond par défaut
        
        # Affichage conditionnel (Loading vs Jeu)
        if context.data.get('loading', False):
            # Écran de chargement
            draw_loading_screen(screen, context.data.get('loading_timer', 0))
        else:
            # Jeu principal
            draw_entities(context)
            draw_hud(context)
            draw_overlay_ui(context)
            
        # Mise à jour de l'affichage
        pygame.display.flip()
        
    # Nettoyage
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
