import random
import pygame
from settings import *

def init_game_state(context):
    """Initialise toutes les variables et l'état de départ."""
    context.data.update({
        # Joueur
        'player_level': 1,
        'current_exercise': 'bench',
        'energy': 5,
        'energy_at_start': 5,
        'coins': 0,
        
        # État Physique
        'state': "DOWN",
        'timer_up': 0,
        'perso_x': 1100,
        'perso_y': 500,
        'perso_speed': 400,
        'perso_direction': 'left',
        
        # État Logique
        'finished': False,
        'finished_timer': 0,
        'waiting_to_start': True,
        'first_game': True,
        'loading': True,
        'loading_timer': LOADING_DURATION,
        
        # Interactions
        'near_bench': False,
        'near_distributor': False,
        'show_menu': False,
        
        # UI / Modals
        'modal': {'active': None, 'timer': 0, 'shown_half': False, 'shown_last': False},
        'distributor_modal': None,
        'distributor_modal_timer': 0,
        
        # Audio
        'volume': 0.3,
        'music_playing': False,
        
        # Données des exercices configuration
        'exercises': {
            'bench': {
                'level': 1, 'score': 0, 'next_level_reps': 5, 
                'cursor': 0, 'speed': 100, 'dir': 1, 
                'target_center': 70, 'target_size': 25, 
                'pos': POS_BENCH
            },
            'traction': {
                'level': 1, 'score': 0, 'next_level_reps': 5, 
                'cursor': 0, 'speed': 100, 'dir': 1, 
                'target_center': 30, 'target_size': 25, 
                'pos': POS_TRACTION
            },
            'bag': {
                'level': 1, 'score': 0, 'next_level_reps': 4, 
                'cursor': 0, 'speed': 0, 'dir': 1, 
                'target_center': 50, 'target_size': 20, 
                'pos': POS_BAG, 
                'qte_active': False, 'qte_key': None, 'qte_label': None, 
                'qte_timer': 0, 'qte_spawn_timer': 0, 
                'swing_timer': 0.0, 'swing_dir': 1
            }
        }
    })

def reset_round(context):
    """Réinitialise les paramètres pour lancer une nouvelle interaction/série."""
    # Garder l'énergie actuelle au lieu de la réinitialiser
    current_energy = context.data['energy']
    
    context.data.update({
        'energy': current_energy,
        'energy_at_start': current_energy,
        'state': "DOWN",
        'finished': False,
        'waiting_to_start': False
    })
    
    # Nettoyage des Modals
    context.data['modal']['active'] = None
    
    # Reset Exercice
    exo_name = context.data['current_exercise']
    current_exo = context.data['exercises'][exo_name]
    current_exo.update({'cursor': 0, 'dir': 1})
    
    # Spécifique au sac de frappe
    if exo_name == 'bag':
        current_exo.update({
            'qte_active': False,
            'qte_key': None,
            'qte_label': None,
            'qte_timer': 0,
            'qte_spawn_timer': random.uniform(1.5, 2.5),
            'swing_timer': 0.0,
            'swing_dir': 1
        })

def check_level_up(context, exo_name):
    """Vérifie si le joueur monte de niveau dans l'exercice."""
    exo = context.data['exercises'][exo_name]
    
    if exo['score'] >= exo['next_level_reps']:
        # Level Up Logic
        exo['level'] += 1
        exo['next_level_reps'] += 5 + (exo['level'] * 2)
        exo['speed'] += 20
        exo['target_size'] = max(10, exo['target_size'] - 2)
        
        # Mise à jour du niveau global du joueur
        max_level = max(v['level'] for v in context.data['exercises'].values())
        context.data['player_level'] = max_level
        
        # Notification
        context.data['modal'].update({'active': "LEVEL_UP", 'timer': 1.5})
    else:
        # Augmentation légère de la difficulté
        exo['speed'] += 3

def perform_rep(context):
    """Gère la tentative de répétition (Barre Espace)."""
    exo_name = context.data['current_exercise']
    exo = context.data['exercises'][exo_name]
    
    # Zone de succès
    hit_start = exo['target_center'] - (exo['target_size'] / 2)
    hit_end = exo['target_center'] + (exo['target_size'] / 2)
    
    if hit_start <= exo['cursor'] <= hit_end:
        # Succès
        context.data.update({
            'state': "UP",
            'timer_up': 0.3,
            'coins': context.data['coins'] + 10,
            'coin_sound_timer': 0.4,
            'coin_sound_played': False
        })
        exo['score'] += 1
        check_level_up(context, exo_name)
    else:
        # Échec
        context.data['energy'] -= 1
        if context.data['sound_minecraft_hit']:
            context.data['sound_minecraft_hit'].set_volume(context.data['volume'])
            context.data['sound_minecraft_hit'].play()
        check_danger_modals(context)

def start_bag_qte(context):
    """Lance un Quick Time Event pour le sac de frappe."""
    bag = context.data['exercises']['bag']
    if bag['qte_active']: 
        return
        
    # Choix aléatoire de la touche
    options = [("LEFT", pygame.K_LEFT), ("RIGHT", pygame.K_RIGHT), ("UP", pygame.K_UP)]
    bag['qte_label'], bag['qte_key'] = random.choice(options)
    
    bag.update({
        'qte_timer': 1.5,
        'qte_active': True,
        'qte_spawn_timer': random.uniform(1.5, 2.5)
    })

def bag_hit_success(context):
    """Appelé quand un QTE est réussi."""
    bag = context.data['exercises']['bag']
    
    # Feedback visuel et sonore
    context.data.update({
        'state': "UP",
        'timer_up': 0.3,
        'coins': context.data['coins'] + 8,
        'coin_sound_timer': 0.4,
        'coin_sound_played': False
    })
    
    # Mise à jour sac
    bag.update({
        'score': bag['score'] + 1,
        'qte_active': False,
        'qte_timer': 0,
        'swing_timer': 0.6,
        'swing_dir': bag['swing_dir'] * -1
    })
    
    # Son spécifique
    if context.data['sound_retro_hit']:
        context.data['sound_retro_hit'].set_volume(context.data['volume'])
        context.data['sound_retro_hit'].play()
        
    check_level_up(context, 'bag')

def check_danger_modals(context):
    """Affiche des alertes si l'énergie est critique."""
    modal = context.data['modal']
    energy = context.data['energy']
    
    if energy == 2 and not modal['shown_half']:
        modal.update({'active': "HALF", 'timer': 2.0, 'shown_half': True})
    elif energy == 1 and not modal['shown_last']:
        modal.update({'active': "LAST", 'timer': 2.0, 'shown_last': True})

def buy_drink(context, cost, energy_add=0, full=False):
    """Logique d'achat au distributeur."""
    if context.data['coins'] >= cost:
        # Transaction réussie
        context.data['coins'] -= cost
        if full:
            context.data['energy'] = 5
        else:
            context.data['energy'] = min(5, context.data['energy'] + energy_add)
            
        context.data['distributor_modal'] = 'BOUGHT'
        context.data['distributor_modal_timer'] = 2.0
        
        # Sons
        if context.data['sound_coin_buy']: 
            context.data['sound_coin_buy'].set_volume(context.data['volume'])
            context.data['sound_coin_buy'].play()
        if context.data['sound_energy_full']: 
            context.data['sound_energy_full'].set_volume(context.data['volume'])
            context.data['sound_energy_full'].play(1)
    else:
        # Pas assez d'argent
        context.data['distributor_modal'] = 'NOT_ENOUGH'
        context.data['distributor_modal_timer'] = 2.0

def handle_input(context, etime):
    """Traite les événements Pygame (Clavier/Souris)."""
    keys = pygame.key.get_pressed()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
            
        if event.type == pygame.KEYDOWN:
            # 1. Gestion QTE Sac
            if context.data['current_exercise'] == 'bag':
                bag_data = context.data['exercises']['bag']
                if bag_data['qte_active'] and event.key == bag_data['qte_key']:
                    bag_hit_success(context)
                    continue
            
            # 2. Menu Pause
            if event.key == pygame.K_ESCAPE:
                context.data['show_menu'] = not context.data['show_menu']
                
            if context.data['show_menu']:
                if event.key == pygame.K_SPACE:
                    context.data['show_menu'] = False
                    continue
                if event.key == pygame.K_q:
                    # Si en exercice: quitter l'exercice en cours
                    if not (context.data['finished'] or context.data['waiting_to_start']):
                        context.data.update({'show_menu': False, 'finished': True})
                        # Restauration energie perdue
                        context.data['energy'] = context.data['energy_at_start'] - (context.data['energy_at_start'] - context.data['energy'])
                    # Si en lobby: fermer le jeu
                    else:
                        return False
                    continue
                # Volume
                if event.key == pygame.K_UP:
                    context.data['volume'] = min(1.0, context.data['volume'] + 0.1)
                    continue
                if event.key == pygame.K_DOWN:
                    context.data['volume'] = max(0.0, context.data['volume'] - 0.1)
                    continue

            # 3. Distributeur
            in_lobby = context.data['finished'] or context.data['waiting_to_start']
            
            if event.key == pygame.K_v and in_lobby and context.data['near_distributor']:
                context.data['distributor_modal'] = 'CHOICE'
            
            if context.data['distributor_modal'] == 'CHOICE':
                if event.key == pygame.K_1:
                    buy_drink(context, 5, energy_add=3)
                elif event.key == pygame.K_2:
                    buy_drink(context, 10, full=True)
                elif event.key == pygame.K_ESCAPE:
                    context.data['distributor_modal'] = None
            
            # 4. Changement d'exercice (Touche E)
            elif event.key == pygame.K_e and in_lobby:
                order = ['bench', 'traction', 'bag']
                current_idx = order.index(context.data['current_exercise'])
                next_exo = order[(current_idx + 1) % len(order)]
                
                # Vérification lock
                locked = None
                if next_exo == 'traction' and context.data['player_level'] < 2:
                    locked = 'LOCKED_TRACTION'
                elif next_exo == 'bag' and context.data['player_level'] < 3:
                    locked = 'LOCKED_BAG'
                    
                if locked:
                    context.data['modal'].update({'active': locked, 'timer': 2.0})
                else:
                    context.data['current_exercise'] = next_exo
            
            # 5. Action Principale (Espace)
            if event.key == pygame.K_SPACE and not context.data['show_menu']:
                # Lancer l'exercice
                if in_lobby and context.data['near_bench']:
                    reset_round(context)
                    continue
                # Faire une rep
                if not in_lobby and context.data['state'] == "DOWN" and not context.data['modal']['active']:
                    perform_rep(context)

        # Souris (Distributeur)
        if event.type == pygame.MOUSEBUTTONDOWN and context.data['distributor_modal'] == 'CHOICE':
            mouse_pos = pygame.mouse.get_pos()
            # On utilise le get() pour éviter une erreur si la clé n'existe pas encore
            if context.data.get('rect_boisson_verte') and context.data['rect_boisson_verte'].collidepoint(mouse_pos):
                buy_drink(context, 5, energy_add=3)
            elif context.data.get('rect_boisson_rouge') and context.data['rect_boisson_rouge'].collidepoint(mouse_pos):
                buy_drink(context, 10, full=True)
            else:
                context.data['distributor_modal'] = None

    # Déplacement du personnage
    if context.data['finished'] or context.data['waiting_to_start']:
        speed = context.data['perso_speed'] * etime
        dx = 0
        dy = 0
        
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = speed
        elif keys[pygame.K_LEFT] or keys[pygame.K_q]: dx = -speed
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = speed
        elif keys[pygame.K_UP] or keys[pygame.K_z]: dy = -speed
        
        if dx != 0:
            context.data['perso_direction'] = 'right' if dx > 0 else 'left'
            
        # Mise à jour position avec clamp
        context.data['perso_x'] = max(50, min(1150, context.data['perso_x'] + dx))
        context.data['perso_y'] = max(100, min(720, context.data['perso_y'] + dy))
        
        # Détection zones interactives
        target_pos = context.data['exercises'][context.data['current_exercise']]['pos']
        dist_bench_x = abs(context.data['perso_x'] - target_pos[0])
        dist_bench_y = abs(context.data['perso_y'] - target_pos[1])
        context.data['near_bench'] = (dist_bench_x < 90 and dist_bench_y < 120)
        
        dist_distributor = abs(context.data['perso_x'] - POS_DISTRIBUTOR[0])
        context.data['near_distributor'] = (dist_distributor < 80 and context.data['perso_y'] > 300)
        
    return True

def update_game(context, etime):
    """Mise à jour logique du cycle de jeu."""
    
    # 1. Chargement
    if context.data['loading']:
        context.data['loading_timer'] -= etime
        if context.data['loading_timer'] <= 0:
            context.data.update({'loading': False, 'waiting_to_start': True})
            if context.data['music_ambient'] and not context.data['music_playing']:
                context.data['music_ambient'].set_volume(context.data['volume'] * 0.05)
                context.data['music_ambient'].play(-1)
                context.data['music_playing'] = True
        return

    # 2. Audio Différé
    if context.data['coin_sound_timer'] > 0:
        context.data['coin_sound_timer'] -= etime
        if context.data['coin_sound_timer'] <= 0 and context.data['sound_coin_earned'] and not context.data['coin_sound_played']:
            context.data['sound_coin_earned'].set_volume(context.data['volume'])
            context.data['sound_coin_earned'].play()
            context.data['coin_sound_played'] = True
    
    # Ajustement volume musique continue
    if context.data['music_playing'] and context.data['music_ambient']:
        context.data['music_ambient'].set_volume(context.data['volume'] * 0.05)
    
    # 3. Timers UI
    if context.data['finished']:
        context.data['finished_timer'] += etime
        if context.data['finished_timer'] >= 3.0:
            context.data['waiting_to_start'] = True
    
    if context.data['modal']['active']:
        context.data['modal']['timer'] -= etime
        if context.data['modal']['timer'] <= 0:
            context.data['modal']['active'] = None
    
    if context.data['distributor_modal_timer'] > 0:
        context.data['distributor_modal_timer'] -= etime
        if context.data['distributor_modal_timer'] <= 0:
            context.data['distributor_modal'] = None

    # 4. Mécaniques de jeu
    # Mouvement curseur (sauf pour bag)
    playing = not context.data['finished'] and not context.data['modal']['active'] and not context.data['waiting_to_start']
    if playing and context.data['current_exercise'] != 'bag':
        exo = context.data['exercises'][context.data['current_exercise']]
        exo['cursor'] += exo['speed'] * exo['dir'] * etime
        if exo['cursor'] > 100 or exo['cursor'] < 0:
            exo['dir'] *= -1

    # Logique Sac de frappe
    if context.data['current_exercise'] == 'bag' and playing:
        bag = context.data['exercises']['bag']
        
        if not bag['qte_active']:
            bag['qte_spawn_timer'] -= etime
            if bag['qte_spawn_timer'] <= 0:
                start_bag_qte(context)
        elif bag['qte_active']:
            bag['qte_timer'] -= etime
            if bag['qte_timer'] <= 0:
                # Echec QTE temps écoulé
                bag['qte_active'] = False
                context.data['energy'] -= 1
                if context.data['sound_minecraft_hit']:
                    context.data['sound_minecraft_hit'].set_volume(context.data['volume'])
                    context.data['sound_minecraft_hit'].play()
                check_danger_modals(context)
                
        if bag['swing_timer'] > 0:
            bag['swing_timer'] = max(0.0, bag['swing_timer'] - etime)

    # 5. Animation UP/DOWN
    if context.data['state'] == "UP":
        context.data['timer_up'] -= etime
        if context.data['timer_up'] <= 0:
            context.data['state'] = "DOWN"
    
    # 6. Game Over
    if context.data['energy'] <= 0 and not context.data['finished']:
        context.data['finished'] = True
