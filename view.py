import math
import pygame
from settings import *

def draw_entities(context):
    """Affiche les entités du jeu (joueur, équipement)."""
    screen = context.screen
    exo_name = context.data['current_exercise']
    playing = not (context.data['finished'] or context.data['waiting_to_start'])
    bag = context.data['exercises']['bag']
    is_muscle = context.data['player_level'] >= 3

    # Calcul oscillation sac
    swing_offset = 0
    if bag['swing_timer'] > 0:
        swing_offset = math.sin(pygame.time.get_ticks() / 80) * 8 * bag['swing_dir']

    # --- Éléments de Décor ---
    # Banc
    screen.blit(context.data['img_bench_solo'], context.data['img_bench_solo'].get_rect(midbottom=POS_BENCH))
    
    # Traction
    traction_img = context.data['img_traction_vide']
    screen.blit(traction_img, traction_img.get_rect(midbottom=POS_TRACTION))
    # Verrou traction
    if context.data['player_level'] < 2 and context.data['interdit']:
        lock_icon = pygame.transform.scale(context.data['interdit'], (80, 80))
        screen.blit(lock_icon, lock_icon.get_rect(center=(POS_TRACTION[0], POS_TRACTION[1]-140)))
    
    # Sac
    bag_key = 'bag_up' if swing_offset > 0 else 'bag_down'
    bag_img = context.data[bag_key]
    
    # Position sac (bouge si actif)
    bag_x_offset = swing_offset if (exo_name == 'bag' and playing and is_muscle) else 0
    bag_pos = (POS_BAG[0] + bag_x_offset, POS_BAG[1])
    screen.blit(bag_img, bag_img.get_rect(midbottom=bag_pos))
    
    # Verrou sac
    if context.data['player_level'] < 3 and context.data['interdit']:
        lock_icon = pygame.transform.scale(context.data['interdit'], (70, 70))
        screen.blit(lock_icon, lock_icon.get_rect(center=(POS_BAG[0], POS_BAG[1]-150)))

    # --- Personnage ---
    if playing:
        # En exercice
        if exo_name == 'bag':
            # Animation frappe
            base_key = 'img_perso_punch' if context.data['state'] == "UP" else 'img_perso_normal'
            if is_muscle: base_key += '_muscle'
            
            p_img = context.data[base_key]
            screen.blit(p_img, p_img.get_rect(midbottom=(POS_BAG[0] - 90, POS_BAG[1] + 20)))
        else:
            # Animation Bench ou Traction
            state_suffix = "up" if context.data['state'] == "UP" else "down"
            # Clé d'image
            if (exo_name in ['traction', 'bench']) and is_muscle:
                img_key = f"{exo_name}_{state_suffix}_muscle"
            else:
                img_key = f"{exo_name}_{state_suffix}"
            
            # Fallback simple
            img = context.data.get(img_key, context.data.get(f"{exo_name}_{state_suffix}"))
            
            draw_pos = POS_BENCH if exo_name == 'bench' else POS_TRACTION
            screen.blit(img, img.get_rect(midbottom=draw_pos))
    else:
        # En déplacement (Lobby)
        direction_key = 'img_perso_up_left' if context.data['perso_direction'] == 'left' else 'img_perso_up'
        if is_muscle: direction_key += '_muscle'
        
        p_img = context.data[direction_key]
        screen.blit(p_img, p_img.get_rect(midbottom=(context.data['perso_x'], context.data['perso_y'])))

def draw_hud(context):
    """Affiche l'interface tête-haute (Jauges, scores)."""
    screen = context.screen
    exo_name = context.data['current_exercise']
    exo = context.data['exercises'][exo_name]
    playing = not (context.data['finished'] or context.data['waiting_to_start'])
    
    # 1. Jauge de Timing (Bench et Traction uniquement)
    if playing and exo_name != 'bag':
        anchor_pos = POS_BENCH if exo_name == 'bench' else POS_TRACTION
        gauge_x, gauge_y, gauge_w, gauge_h = anchor_pos[0] + 120, anchor_pos[1] - 220, 35, 180
        
        # Fond jauge
        pygame.draw.rect(screen, (40, 40, 45), (gauge_x-3, gauge_y-3, gauge_w+6, gauge_h+6), border_radius=8)
        pygame.draw.rect(screen, (60, 60, 65), (gauge_x, gauge_y, gauge_w, gauge_h), border_radius=6)
        
        # Zone cible (verte)
        target_y = gauge_y + gauge_h - (exo['target_center'] / 100 * gauge_h)
        target_h = (exo['target_size'] / 100) * gauge_h
        pygame.draw.rect(screen, COLOR_GREEN, (gauge_x+2, target_y - target_h/2, gauge_w-4, target_h), border_radius=3)
        
        # Curseur (rouge)
        cursor_y = gauge_y + gauge_h - (exo['cursor'] / 100 * gauge_h)
        pygame.draw.rect(screen, COLOR_RED, (gauge_x-10, cursor_y-6, gauge_w+20, 12), border_radius=3)
    
    # 2. Bandeau HUD Supérieur
    hud_bg = pygame.Surface((460, 50), pygame.SRCALPHA)
    pygame.draw.rect(hud_bg, (0, 0, 0, 170), hud_bg.get_rect(), border_radius=8)
    screen.blit(hud_bg, (15, 15))
    
    font_bold = pygame.font.SysFont('Arial', 14, bold=True)
    font_tiny = pygame.font.SysFont('Arial', 11)
    
    def draw_stat(label, value, x_offset, color, icon=None):
        screen.blit(font_tiny.render(label, True, color), (15 + x_offset, 23))
        screen.blit(font_bold.render(str(value), True, color), (15 + x_offset, 38))
        if icon:
            screen.blit(icon, (15 + x_offset - 7, 23))
        
    draw_stat("PLAYER", f"LVL {context.data['player_level']}", 10, COLOR_TEXT_GREY)
    draw_stat("BENCH", f"LVL {context.data['exercises']['bench']['level']}", 90, COLOR_GOLD if exo_name=='bench' else COLOR_TEXT_GREY)
    draw_stat("TRACT", f"LVL {context.data['exercises']['traction']['level']}", 180, COLOR_GOLD if exo_name=='traction' else COLOR_TEXT_GREY)
    draw_stat("BAG", f"LVL {context.data['exercises']['bag']['level']}", 260, COLOR_GOLD if exo_name=='bag' else COLOR_TEXT_GREY)
    draw_stat("REPS", f"{exo['score']}", 330, COLOR_CYAN)
    draw_stat("COINS", f"{context.data['coins']:03d}", 390, COLOR_GREEN, context.data['coin'])
    
    # 3. Énergie (Cœurs)
    screen.blit(font_tiny.render(f"ENERGY: {context.data['energy']}/5", True, COLOR_RED), (25, 75))
    for i in range(5):
        color = COLOR_RED if i < context.data['energy'] else (60, 60, 60)
        x_pos = 110 + i * 12
        # Dessin d'un coeur stylisé
        points = [(x_pos-4, 79), (x_pos-2, 77), (x_pos, 79), (x_pos+2, 77), (x_pos+4, 79), (x_pos, 87)]
        pygame.draw.polygon(screen, color, points)

    # 4. Instructions QTE (Bag)
    if playing and exo_name == 'bag':
        font_qte = pygame.font.SysFont('Arial', 18, bold=True)
        if exo['qte_active']:
            text_qte = f"TAPE {exo['qte_label']} !"
            color_qte = COLOR_RED
        else:
            text_qte = "Attends le signal..."
            color_qte = COLOR_CYAN
            
        render = font_qte.render(text_qte, True, color_qte)
        screen.blit(render, render.get_rect(center=(POS_BAG[0], POS_BAG[1]-200)))

def draw_overlay_ui(context):
    """Dessine les éléments superposés (Menus, Alertes)."""
    screen = context.screen
    font_large = pygame.font.SysFont('Arial', 48, bold=True)
    font_std = pygame.font.SysFont('Arial', 20)
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    
    # Messages de fin de série ou d'accueil
    if context.data['finished'] or context.data['waiting_to_start']:
        if context.data['finished'] and context.data['finished_timer'] < 2.0:
            msg = font_large.render("SÉRIE TERMINÉE !", True, COLOR_GOLD)
            screen.blit(msg, msg.get_rect(center=(center_x, 520)))
        elif context.data['waiting_to_start']:
            brand = pygame.font.SysFont('Arial', 40, bold=True).render("BE STRONG GYM", True, COLOR_GOLD)
            screen.blit(brand, (SCREEN_WIDTH - 350, 180))
        
        # Bouton d'interaction
        prompt_text = None
        is_locked = False
        
        if context.data['near_bench']:
            # Logique de verrous
            needed_level = 1
            if context.data['current_exercise'] == 'traction': needed_level = 2
            elif context.data['current_exercise'] == 'bag': needed_level = 3
            
            if context.data['player_level'] < needed_level:
                is_locked = True
                prompt_text = f"LOCKED (Need LVL {needed_level})"
            else:
                prompt_text = "GO ! (Espace)"
                
        elif context.data['near_distributor']:
            prompt_text = "[V] Acheter"
            
        if prompt_text:
            # Animation bouton
            pulse = abs(math.sin(pygame.time.get_ticks() / 200)) * 20
            
            if is_locked:
                btn_color = (50, 0, 0)
                btn_w = 200
            else:
                btn_color = (int(50+pulse), int(150+pulse), 255)
                btn_w = 180
                
            pygame.draw.rect(screen, btn_color, (center_x-90, 430, btn_w, 50), border_radius=10)
            btn_render = font_std.render(prompt_text, True, (255,255,255))
            screen.blit(btn_render, btn_render.get_rect(center=(center_x, 455)))

    # Gestion des Modals (Alertes)
    if context.data['modal']['active']:
        # Fond sombre
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        # Textes et couleurs selon le type d'alerte
        alerts = {
            "LAST": ((255, 50, 50), "LAST CHANCE BUDDY"),
            "HALF": ((255, 200, 0), "ATTENTION MON AMI"),
            "LEVEL_UP": ((0, 255, 100), "LEVEL UP !"),
            "LOCKED_TRACTION": ((255, 100, 0), "NIVEAU 2 REQUIS !"),
            "LOCKED_BAG": ((255, 120, 0), "NIVEAU 3 REQUIS !")
        }
        color, text = alerts.get(context.data['modal']['active'], ((255,255,255), "ALERT"))
        
        # Boîte de dialogue
        pygame.draw.rect(screen, color, (295, 275, 610, 250), border_radius=20)
        pygame.draw.rect(screen, (30, 30, 30), (300, 280, 600, 240), border_radius=15)
        
        text_render = font_large.render(text, True, color)
        screen.blit(text_render, text_render.get_rect(center=(center_x, 380)))

    # Modal Distributeur
    if context.data['distributor_modal']:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        screen.blit(overlay, (0, 0))
        
        if context.data['distributor_modal'] == 'CHOICE':
            # Affichage des choix
            if context.data['boisson_verte']:
                r_vert = context.data['boisson_verte'].get_rect(center=(center_x - 180, center_y))
                screen.blit(context.data['boisson_verte'], r_vert)
                context.data['rect_boisson_verte'] = r_vert
                
            if context.data['boisson_rouge']:
                r_rouge = context.data['boisson_rouge'].get_rect(center=(center_x + 180, center_y))
                screen.blit(context.data['boisson_rouge'], r_rouge)
                context.data['rect_boisson_rouge'] = r_rouge
                
            title = pygame.font.SysFont('Arial', 40, bold=True).render("DISTRIBUTEUR", True, COLOR_GOLD)
            screen.blit(title, title.get_rect(center=(center_x, center_y - 120)))
            
            help_txt = pygame.font.SysFont('Arial', 18).render("ESC pour fermer", True, COLOR_TEXT_GREY)
            screen.blit(help_txt, help_txt.get_rect(center=(center_x, center_y + 100)))
        else:
            # Feedback Achat
            is_error = context.data['distributor_modal'] == 'NOT_ENOUGH'
            msg = "PAS ASSEZ DE COINS" if is_error else "ACHAT EFFECTUÉ !"
            col = COLOR_RED if is_error else COLOR_GREEN
            
            render_fb = pygame.font.SysFont('Arial', 40, bold=True).render(msg, True, col)
            screen.blit(render_fb, render_fb.get_rect(center=(center_x, center_y)))

    # Menu Pause
    if context.data['show_menu']:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        title_pause = font_large.render("PAUSE", True, COLOR_GOLD)
        screen.blit(title_pause, title_pause.get_rect(center=(center_x, center_y - 100)))
        
        font_opt = pygame.font.SysFont('Arial', 24)
        opt1 = font_opt.render("Espace - Reprendre", True, COLOR_CYAN)
        screen.blit(opt1, opt1.get_rect(center=(center_x, center_y)))
        
        opt2 = font_opt.render("Q - Quitter", True, COLOR_RED)
        screen.blit(opt2, opt2.get_rect(center=(center_x, center_y + 60)))
        
        # Barre de Volume
        vol_pct = int(context.data['volume']*100)
        vol_txt = pygame.font.SysFont('Arial', 18).render(f"↑/↓ Volume: {vol_pct}%", True, COLOR_GOLD)
        screen.blit(vol_txt, vol_txt.get_rect(center=(center_x, center_y + 130)))
        
        bar_x, bar_y = center_x - 100, center_y + 170
        pygame.draw.rect(screen, (60, 60, 80), (bar_x, bar_y, 200, 20), border_radius=5)
        pygame.draw.rect(screen, COLOR_GREEN, (bar_x, bar_y, 200 * context.data['volume'], 20), border_radius=5)

def draw_loading_screen(screen, timer):
    """Affiche l'écran de chargement avec une barre de progression."""
    center_x, center_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
    
    # Fond semi-transparent
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))
    
    # Titre du jeu
    font_large = pygame.font.SysFont('Arial', 56, bold=True)
    title_text = font_large.render("BE STRONG GYM ", True, COLOR_GOLD)
    screen.blit(title_text, title_text.get_rect(center=(center_x, center_y - 170)))
    
    # Texte de chargement
    font_small = pygame.font.SysFont('Arial', 24)
    loading_text = font_small.render("Chargement...", True, COLOR_CYAN)
    screen.blit(loading_text, loading_text.get_rect(center=(center_x, center_y + 100)))
    
    # Barre de progression
    bar_width = 300
    bar_height = 20
    bar_x = center_x - bar_width // 2
    bar_y = center_y + 120
    
    # Calcul de la progression (de 0.0 à 1.0)
    # On utilise LOADING_DURATION comme référence de temps total
    progress = max(0, min(1, (LOADING_DURATION - timer) / LOADING_DURATION))
    
    # Dessin de la barre
    pygame.draw.rect(screen, (60, 60, 80), (bar_x, bar_y, bar_width, bar_height), border_radius=10) # Fond
    pygame.draw.rect(screen, COLOR_GOLD, (bar_x, bar_y, bar_width * progress, bar_height), border_radius=10) # Remplissage
    pygame.draw.rect(screen, COLOR_GOLD, (bar_x, bar_y, bar_width, bar_height), border_radius=10, width=2) # Bordure
