import pygame
from classtd import*

pygame.init()
SCREEN_SIZE = (800, 800)
screen = pygame.display.set_mode(SCREEN_SIZE) 

startpos_x = 600
startpos_y = 50

enemy = []
square_towers = []
bases = [Base(250, 250, 'base.png'),Base(100, 100, 'base.png'),Base(400, 400, 'base.png')]


def draw_spawn_enemy():
    
    button_rect = pygame.Rect(0, 0, 200, 50)
    pygame.draw.rect(screen, (255, 0, 255), button_rect)
    text = 'Spawn ennemi'
    text_color = pygame.Color('white')
    font = pygame.font.Font(None, 30)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)
    

    mouse_pressed = pygame.mouse.get_pressed()[0]

    if button_rect.collidepoint(pygame.mouse.get_pos()) and mouse_pressed and not draw_spawn_enemy.mouse_state:
        enemy.append(Enemy(startpos_x, startpos_y, "star.png"))

        draw_spawn_enemy.mouse_state = True

    elif not mouse_pressed and draw_spawn_enemy.mouse_state:
        draw_spawn_enemy.mouse_state = False
        
    screen.blit(text_surface, text_rect)



# Boucle principale
running = True
mouse_down = False
draw_spawn_enemy.mouse_state = False

#Initialiser le temps 
clock = pygame.time.Clock()

while running:
    screen.fill((255, 255, 255)) 
    clock.tick(60)  # la méthode tick() renvoie le temps en millisecondes, nous le convertissons en secondes
    draw_spawn_enemy() #temporaire

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # //

        if event.type == pygame.MOUSEBUTTONUP and bool(bases): #et la liste pour les bases non vide
            mouse_pos = pygame.mouse.get_pos()
            for base in bases :
                if base.rect.collidepoint(mouse_pos):
                        square_towers.append(SquareTower(base.rect.x+5, base.rect.y+5, 'square_tower.png', 1))
                        base.remove
                        bases.remove(base)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and bool(square_towers):  # Left mouse button clicked
            pos = pygame.mouse.get_pos()
            for tower in square_towers:
                if tower.rect.collidepoint(pos):
                    tower.mouse_down = True
        else :
            for tower in square_towers:
                tower.mouse_down = False

            if event.type == pygame.KEYDOWN and bool(square_towers):
                if event.key == pygame.K_s:
                    pos = pygame.mouse.get_pos()
                    for tower in square_towers:
                        if tower.rect.collidepoint(pos):
                            bases.append(Base(tower.rect.x-5, tower.rect.y-5, 'base.png'))
                            tower.sell()
                            square_towers.remove(tower)

        # ////

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for tower in square_towers:
                if tower.rect.collidepoint(pos):
                    tower.mouse_down = True
        else:
            for tower in square_towers:
                tower.mouse_down = False

  

    #GESTION SQUARETOWER
    for tower in square_towers:
        if tower.mouse_down:
            tower.draw_range(screen)
        tower.draw(screen)

    #GESTION BASE
    for base in bases :
        base.draw(screen)
        
    #GESTION ENEMY
    for enemy_obj in enemy:
        enemy_obj.draw(screen)
        enemy_obj.update()
        if enemy_obj.has_traversed:
            enemy.remove(enemy_obj)

    pygame.display.flip()

pygame.quit()
