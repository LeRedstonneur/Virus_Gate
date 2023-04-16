# Importation des bibliothèques nécessaires
import pygame
from random import choice
from class_Base import *
from class_Enemy import *
from class_Tower import *
from groups import *
from class_Button import *
from waves import*
from generate_map import *

def start_TD():
    #-------------------------------------------------------------------------------------------------------------------------------------------#
    pygame.init()
    # Création de la fenêtre de jeu de taille 800x800
    
    SCREEN_SIZE = (800,800)
    screen = pygame.display.set_mode(SCREEN_SIZE)

    
    #-------------------------------------------------------------------------------------------------------------------------------------------#
    # Position initiale de l'ennemi
    

    try :
        content=read(path_assets+"/map.txt")
        running = True
        max = max_line(content)
        size=(SCREEN_SIZE[0]//max[0],SCREEN_SIZE[1]//max[1]) #taille d'un rectangle de la grille
        matrice=generate_map(content)
        del content
        bases = generate_bases(matrice,size)
        waves = generate_waves()
        wave,index,cpt = waves[0],0,[]
        len_wave = len(wave)
        start_time = pygame.time.get_ticks()
        quitting = False
    except EmptyFile :
        print("File was found to be empty")
        running = False

    except FileNotFoundError :
        print("File not found")
        running = False

    #-------------------------------------------------------------------------------------------------------------------------------------------#
    def draw_player_lives(screen, player_lives):
        text = f'Lives: {player_lives}'
        text_color = pygame.Color('white')
        font = pygame.font.Font(None, 30)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(topright=(750, 20))
        screen.blit(text_surface, text_rect)
    #-------------------------------------------------------------------------------------------------------------------------------------------#
    def draw_game_over(screen):
        text = 'YOU LOST'
        text_color = pygame.Color('red')
        font = pygame.font.Font(None, 60)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
        screen.blit(text_surface, text_rect)
    #-------------------------------------------------------------------------------------------------------------------------------------------#
    def draw_game_win(screen):
        text = 'YOU WIN !'
        text_color = pygame.Color('Green')
        font = pygame.font.Font(None, 60)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
        screen.blit(text_surface, text_rect)
    #-------------------------------------------------------------------------------------------------------------------------------------------#
    def draw_spawn_enemy():
        # Création du rectangle pour le bouton
        button_rect = pygame.Rect(225, 25, 200, 50)
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
            enemy_classes = [Rectangle,Croix,GrandeCroix,Fleche,Coeur,Losange,Hexagone]
            random_enemy_class = choice(enemy_classes)   
            # Ajout de l'ennemi aléatoire au groupe
            enemy_group.add(random_enemy_class(startpos_x, startpos_y))
            draw_spawn_enemy.mouse_state = True
        elif not mouse_pressed and draw_spawn_enemy.mouse_state:
            draw_spawn_enemy.mouse_state = False
        # Blitter le texte et le rectangle du bouton sur l'écran
        screen.blit(text_surface, text_rect)
    #-------------------------------------------------------------------------------------------------------------------------------------------#
    def draw_player_money(screen, player_money):
        text = f'Money: {player_money}'
        text_color = pygame.Color('white')
        font = pygame.font.Font(None, 30)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(topright=(775, 50))
        screen.blit(text_surface, text_rect)
    #-------------------------------------------------------------------------------------------------------------------------------------------#
    def draw_price(screen,cost,coord):  
        text = f'Cost: {cost}'
        text_color = pygame.Color('white')
        font = pygame.font.Font(None, 30)
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(topright=coord)
        screen.blit(text_surface, text_rect)
    def draw_prices(screen,TOWER_COSTS,tower_dico):
        for i, tower_type in enumerate(["Square", "Round", "Triangle", "Trapeze"]):
            draw_price(screen,TOWER_COSTS[tower_dico[tower_type]],(775,150+i*150))
    #-------------------------------------------------------------------------------------------------------------------------------------------#
    # Initialisation des variables de la boucle principale
    mouse_down = False
    draw_spawn_enemy.mouse_state = False
    #-------------------------------------------------------------------------------------------------------------------------------------------#
    # Boutons
    start_button = Button(600, 750, 200, 50,text='Start Game')
    next_wave_button = Button(375, 750, 200,50 ,text='Next Wave') 
    button =(start_button,next_wave_button)
    #-------------------------------------------------------------------------------------------------------------------------------------------#
    clock = pygame.time.Clock()
    #-------------------------------------------------------------------------------------------------------------------------------------------#
    # Créer des boutons pour chaque type de tour disponible
    BUTTON_INACTIVE_COLOR = (192, 192, 192)
    BUTTON_ACTIVE_COLOR = (255, 0, 0)
    TOWER_COSTS = {
    "SquareTower": 20,
    "RoundTower": 30,
    "TriangleTower": 40,
    "TrapezeTower": 50,
    }
    tower_buttons = []
    tower_dico={"Square" : "SquareTower", "Round" : "RoundTower", "Triangle" : "TriangleTower", "Trapeze" : "TrapezeTower"}
    for i, tower_type in enumerate(["Square", "Round", "Triangle", "Trapeze"]):
        tower_button = Button( 680, 100+i*150, 100, 50, text=tower_type)     
        tower_buttons.append(tower_button)
    selected_tower = None
    player_money = 120
    player_lives = 10
    game_over = False
    #-------------------------------------------------------------------------------------------------------------------------------------------#
    while running:
        screen.fill((0, 0, 0)) 
        print_map(screen,matrice,size)
        clock.tick(60)
#-------------------------------------------------------------------------------------------------------------------------------------------#  
   

#-------------------------------------------------------------------------------------------------------------------------------------------#
        if game_over:
            running = False

        #draw_spawn_enemy() 
        draw_player_money(screen, player_money)

        # Afficher les boutons de tour
        for tower_button in tower_buttons:
            # Si le texte du bouton correspond à la tour sélectionnée, afficher le bouton en rouge
            if tower_dico[tower_button.text] == selected_tower:
                tower_button.draw(screen, BUTTON_ACTIVE_COLOR)
            else :
                tower_button.draw(screen, BUTTON_INACTIVE_COLOR)

    #-------------------------------------------------------------------------------------------------------------------------------------------#   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                quitting = True
    #-------------------------------------------------------------------------------------------------------------------------------------------#

    #-------------------------------------------------------------------------------------------------------------------------------------------#        
            # Gestion de l'ajout de tours sur les bases
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for base in bases:
                    if base.rect.collidepoint(mouse_x, mouse_y):
                        if selected_tower is not None and player_money >= TOWER_COSTS[selected_tower]:
                            # Placer la tour sélectionnée sur la base
                            tower_class = globals()[selected_tower]
                            base.add_tower(tower_class(base.rect.x, base.rect.y,size))
                            base.kill()
                            bases.remove(base)
                            player_money -= TOWER_COSTS[selected_tower]  # Déduire le coût de la tour
                        selected_tower = None
                
                if event.button == 1:  # Bouton gauche de la souris
                    for tower_button in tower_buttons:
                        if tower_button.rect.collidepoint(event.pos):
                            selected_tower = tower_dico[tower_button.text]
                            
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    for tower in tower_group:
                        if tower.rect.collidepoint(mouse_x, mouse_y):
                            tower.toggle_range()
                        else :
                            if tower.show_range == True :
                                tower.toggle_range()
                    start_button.verify_clik((mouse_x, mouse_y))    
                    next_wave_button.verify_clik_alt((mouse_x, mouse_y))           

                    
    #-------------------------------------------------------------------------------------------------------------------------------------------#
            #gestion vente des tours
            if event.type == pygame.KEYDOWN and bool(tower_group):
                if event.key == pygame.K_s:
                    pos = pygame.mouse.get_pos()
                    for tower in tower_group:
                        if tower.rect.collidepoint(pos):
                            refund_amount, original_pos = tower.sell()
                            bases.append(Base(original_pos[0], original_pos[1],size[0],size[1],(tower.rect.x//size[0],tower.rect.y//size[1])))
                            player_money += refund_amount
                            tower_group.remove(tower)

                                
    #-------------------------------------------------------------------------------------------------------------------------------------------#
        for tower in tower_group:
            tower.draw(screen)
            if isinstance(tower, SquareTower):
                tower.update(enemy_group,screen)
                tower.draw_range(screen)
            elif isinstance(tower, RoundTower):
                tower.attack(enemy_group, screen)
                tower.draw_range(screen)
            elif isinstance(tower, TriangleTower):
                tower.update(enemy_group, screen)
                tower.draw_projectiles(screen)
                tower.draw_range(screen)
    #-------------------------------------------------------------------------------------------------------------------------------------------#
        for enemy in enemy_group:
            enemy.update()
            enemy.draw(screen)
            if enemy.is_dead():
                player_money += enemy.value
            if enemy.has_traversed:
                enemy_group.remove(enemy)
                player_lives -= 1
                if player_lives <= 0:
                    game_over = True
                    player_lives = 0

        if start_button.activated == True :
            past_time = (pygame.time.get_ticks() - start_time)/1000.0
            if past_time > 0.75  :
                if not wave :
                    if not enemy_group :              
                        if next_wave_button.activated == True :
                            del waves[0]
                            if waves  :
                                wave = waves[0]
                                index,cpt,len_wave = 0,[],len(wave)
                            else :
                                running = False
                else :
                    index,len_wave = spawn_next_ennemy(wave,index,cpt,len_wave)
                    start_time = pygame.time.get_ticks()


                      
    #-------------------------------------------------------------------------------------------------------------------------------------------#
        # Affichage des boutons
        for b in button :
            if b.activated :
                b.draw(screen,(0, 86, 27))
            else :
                b.draw(screen,(200, 200, 200))
        draw_player_lives(screen, player_lives)
        draw_player_money(screen, player_money)
        draw_prices(screen,TOWER_COSTS,tower_dico)
        pygame.display.flip()
    
    replay = None
    if not quitting :

        Replay = Button(300, 500, 200,50 ,text='Replay ?') 
        Quit = Button(300, 600, 200,50 ,text='Quit ?') 
        del button
        button = (Replay,Quit)
        screen.fill((0, 0, 0)) 
        if game_over :
            draw_game_over(screen)
        else :
            draw_game_win(screen)
        while replay is None :
                Replay.draw(screen,(200, 200, 200))
                Quit.draw(screen,(200, 200, 200))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT :
                        replay = False
                    if event.type == pygame.MOUSEBUTTONDOWN :
                        if event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            for b in button :
                                b.verify_clik(mouse_pos)
                pygame.display.flip()
                if Replay.activated :
                    enemy_group.empty()
                    tower_group.empty()
                    pygame.quit()
                    start_TD()
                if Quit.activated :
                    replay = False
    
    pygame.quit()
    return replay

print(start_TD())