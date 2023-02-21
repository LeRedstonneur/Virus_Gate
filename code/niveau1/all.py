import pygame
from all import SquareTower

pygame.init()
SCREEN_SIZE = (800, 600)
socle1 = pygame.transform.scale(pygame.image.load('socle.png'), (100, 100))

screen = pygame.display.set_mode(SCREEN_SIZE)
etat = 0

# Placer l'image aux coordonnées (250, 250)
socle_rect = socle1.get_rect()
socle_rect.center = (250, 250)

# Créer une liste pour stocker toutes les tours carrées
square_towers = []

# Boucle principale
running = True
mouse_down = False
while running:
    screen.fill((0,0,0))
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()

            if socle_rect.collidepoint(mouse_pos):
                square_towers.append(SquareTower(socle_rect.x, socle_rect.y, 'square_tower.png', 1))

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
            pos = pygame.mouse.get_pos()
            for tower in square_towers:
                if tower.rect.collidepoint(pos):
                    tower.mouse_down = True
        else :
            for tower in square_towers:
                tower.mouse_down = False
  
    screen.blit(socle1, socle_rect)
    for tower in square_towers:
        if tower.mouse_down:
            tower.draw_range(screen) 
        
        tower.draw(screen)

    pygame.display.flip()
pygame.quit()


                
    
