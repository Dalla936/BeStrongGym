import pygame
import os
from settings import *

def load_assets(context):
    """Charge toutes les images du jeu et les stocke dans le dictionnaire de données."""
    scale = 8
    assets_dir = "assets"
    
    def load_scaled_image(filename, scale_factor=scale):
        """Helper pour charger et redimensionner une image."""
        path = os.path.join(assets_dir, filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            new_width = image.get_width() * scale_factor
            new_height = image.get_height() * scale_factor
            return pygame.transform.scale(image, (new_width, new_height))
        except Exception as e:
            # Fallback en cas d'erreur: carré rose
            print(f"Erreur chargement {filename}: {e}")
            surface = pygame.Surface((50, 50))
            surface.fill((255, 0, 255))
            return surface

    # Dictionnaire des fichiers images
    image_files = {
        'bench_up': "bench_up_v2.png",
        'bench_down': "perso_bench_down.png",
        'bench_up_muscle': "perso_bench_up_muscle.png",
        'bench_down_muscle': "perso_bench_down_muscle.png",
        'img_bench_solo': "solo_bench.png",
        'traction_up': "traction_haut.png",
        'traction_down': "traction_bas.png",
        'img_traction_vide': "traction_vide.png",
        'traction_up_muscle': "traction_haut-muscle.png",
        'traction_down_muscle': "traction_bas-muscle.png",
        'bag_up': "sac_droite.png",
        'bag_down': "sac_gauche.png",
        'img_perso_up': "perso_up.png",
        'img_perso_up_left': "perso_up_left.png",
        'img_perso_punch': "perso_frappe.png",
        'img_perso_normal': "perso_normal.png",
        'img_perso_up_muscle': "perso_up_right-muscle.png",
        'img_perso_up_left_muscle': "perso_up_left-muscle.png",
        'img_perso_punch_muscle': "perso_up_frappe_muscle.png",
        'img_perso_normal_muscle': "perso_normal_muscle.png"
    }
    
    # Chargement en boucle
    for key, filename in image_files.items():
        context.data[key] = load_scaled_image(filename)

    # Chargement spécifique du Background
    try:
        bg_path = os.path.join(assets_dir, "new_home.png")
        bg_image = pygame.image.load(bg_path).convert()
        context.data['background'] = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except Exception as e:
        print(f"Erreur background: {e}")
        bg_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_surface.fill((45, 45, 60))
        context.data['background'] = bg_surface

    # Chargement des images UI et objets
    optional_images = {
        'interdit': ("interdit.png", None), # pas de scale auto
        'boisson_verte': ("boisson_verte.png", (180, 240)),
        'boisson_rouge': ("boisson_rouge.png", (180, 240)),
        'coin': ("coin.png", (100, 100))
    }
    
    for key, (filename, size) in optional_images.items():
        try:
            path = os.path.join(assets_dir, filename)
            img = pygame.image.load(path).convert_alpha()
            if size:
                img = pygame.transform.scale(img, size)
            context.data[key] = img
        except:
            context.data[key] = None

def load_sounds(context):
    """Charge tous les sons et musiques du jeu."""
    def safe_load_sound(filename):
        try:
            return pygame.mixer.Sound(f"sounds/{filename}")
        except:
            return None
    
    sound_files = {
        'sound_rep_success': "repetition_reussi.wav",
        'sound_coin_earned': "coin_gagne.wav",
        'sound_coin_buy': "coin.mp3",
        'sound_energy_full': "energy_full.wav",
        'music_ambient': "sport_ambiance.mp3",
        'sound_minecraft_hit': "minecraft_hit.mp3",
        'sound_retro_hit': "retro_hit.wav"
    }
    
    for key, filename in sound_files.items():
        context.data[key] = safe_load_sound(filename)
        
    context.data['coin_sound_timer'] = 0
    context.data['coin_sound_played'] = False
