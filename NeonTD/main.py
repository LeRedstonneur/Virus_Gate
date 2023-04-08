# Importation des bibliothèques nécessaires
import pygame
from random import choice
from class_Base import*
from class_Enemy import*
from class_Tower import*
from groups import*

pygame.init()
# Création de la fenêtre de jeu de taille 800x800
SCREEN_SIZE = (800, 800)
screen = pygame.display.set_mode(SCREEN_SIZE)

# Position initiale de l'ennemi
startpos_x = 600
startpos_y = 50
bases = [Base(250, 250, 'Assets/Environnement/base.png'), Base(100, 100, 'Assets/Environnement/base.png'), Base(450, 450, 'Assets/Environnement/base.png')]

def draw_spawn_enemy():
    # Création du rectangle pour le bouton
    button_rect = pygame.Rect(0, 0, 200, 50)
    pygame.draw.rect(screen, (255, 0, 255), button_rect)
    # Ajout du texte au bouton
    text = 'Spawn Enemy'
    text_color = pygame.Color('black')
    font = pygame.font.Font(None, 30)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    # Détection du clic de souris sur le bouton
    mouse_pressed = pygame.mouse.get_pressed()[0]
    if button_rect.collidepoint(pygame.mouse.get_pos()) and mouse_pressed and not draw_spawn_enemy.mouse_state:   
        # Choix d'un ennemi aléatoire parmi ceux déjà créés
        enemy_classes = [GrandeCroix,Croix]
        random_enemy_class = choice(enemy_classes)   
        # Ajout de l'ennemi aléatoire au groupe
        enemy_group.add(random_enemy_class(startpos_x, startpos_y))  
        draw_spawn_enemy.mouse_state = True
    elif not mouse_pressed and draw_spawn_enemy.mouse_state:
        draw_spawn_enemy.mouse_state = False
    # Blitter le texte et le rectangle du bouton sur l'écran
    screen.blit(text_surface, text_rect)


# Initialisation des variables de la boucle principale
running = True
mouse_down = False
draw_spawn_enemy.mouse_state = False

# Initialisation de la clock pour la gestion du temps
clock = pygame.time.Clock()

# Boucle principale du jeu
while running:
    # Effacement de l'écran
    screen.fill((255, 255, 255)) 
    
    # Limitation de la boucle à 60 FPS
    clock.tick(60)
    draw_spawn_enemy()

    for event in pygame.event.get():
        # Arrêt du jeu si l'utilisateur ferme la fenêtre
        if event.type == pygame.QUIT:
            running = False

        # Gestion de l'ajout de tours sur les bases
        if event.type == pygame.MOUSEBUTTONUP and bool(bases):
            mouse_pos = pygame.mouse.get_pos()
            for base in bases:
                if base.rect.collidepoint(mouse_pos):
                    tower_group.add(SquareTower(base.rect.x+5, base.rect.y+5, 'Assets/Towers/square_tower.png'))
                    base.kill()  
                    bases.remove(base)


                
        # Gestion du clic de souris sur une tour
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for tower in tower_group:
                # Vérifier si le clic de souris se trouve dans la zone de détection de la tour
                detection_zone = tower.rect.inflate(50, 50)
                if detection_zone.collidepoint(pos):
                    # Si oui, marquer la tour comme "cliquée"
                    tower.mouse_down = True
        else:
            # Si le clic de souris n'est pas enfoncé, marquer toutes les tours comme "non cliquées"
            for tower in tower_group:
                tower.mouse_down = False

            # Gestion de la vente de la tour avec la touche S
            if event.type == pygame.KEYDOWN and bool(tower_group):
                if event.key == pygame.K_s:
                    pos = pygame.mouse.get_pos()
                    for tower in tower_group:
                        if tower.rect.collidepoint(pos):
                            # Ajouter une nouvelle base à l'emplacement de la tour vendue
                            bases.append(Base(tower.rect.x - 5, tower.rect.y - 5, 'Assets/Environnement/base.png'))
                            # Supprimer la tour de la liste des tours
                            tower.sell()
                            tower_group.remove(tower)


    # GESTION TOWERS
    for tower in tower_group:
        # Partie Attaque
        targets = []
        for enemy_in_range in enemy_group.sprites():
            if tower.in_range(enemy_in_range):
                targets.append(enemy_in_range)
        if targets:
            if isinstance(tower, RoundTower):
                tower.attack(targets, screen)
            elif isinstance(tower, SquareTower):
                tower.update(enemy_group)



        #Partie Range
        if tower.mouse_down:
            tower.draw_range(screen)
        tower.draw(screen)



    # GESTION BASE
    for base in bases:
        base.draw(screen)

    # GESTION ENEMY
    enemy_group.update()
    enemy_group.draw(screen)

    # Rafraîchir l'écran
    pygame.display.flip()

pygame.quit()
