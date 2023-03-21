import pygame
from all import SquareTower, Enemy

pygame.init()
SCREEN_SIZE = (800, 800)
socle1 = pygame.transform.scale(pygame.image.load('socle.png'), (90, 90))
map1 = pygame.transform.scale(pygame.image.load('map1.png'), (800, 600))
screen = pygame.display.set_mode(SCREEN_SIZE)
etat = 0
startpos_x = 600
startpos_y = 50

enemy = []

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

draw_spawn_enemy.mouse_state = False


socle_rect = socle1.get_rect()
socle_rect.center = (170, 230)

# Créer une liste pour stocker toutes les tours carrées
square_towers = []


# Boucle principale
running = True
mouse_down = False

#Initialiser le temps 
clock = pygame.time.Clock()

while running:
    screen.fill((255, 255, 255))
    clock.tick(60)  # la méthode tick() renvoie le temps en millisecondes, nous le convertissons en secondes
    draw_spawn_enemy()
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            if socle_rect.collidepoint(mouse_pos):
                square_towers.append(SquareTower(socle_rect.x, socle_rect.y, 'square_tower.png', 1))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            for tower in square_towers:
                if tower.rect.collidepoint(pos):
                    tower.mouse_down = True
        else:
            for tower in square_towers:
                tower.mouse_down = False

    screen.blit(socle1, socle_rect)
    for tower in square_towers:
        if tower.mouse_down:
            tower.draw_range(screen)

        tower.draw(screen)

    # Dessiner chaque ennemi à l'écran
    for enemy_obj in enemy:
        print(enemy_obj.rect.x,enemy_obj.rect.y)
        enemy_obj.draw(screen)
        enemy_obj.update()

    pygame.display.flip()

pygame.quit()
