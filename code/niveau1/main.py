import pygame
from player import Player
from quit import quit


def start():
    '''Cette fonction est appelée par l'écran d'accueil pour démarrer le niveau'''
    pygame.init()
    
    

    # Gestion de l'écran
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    bg = pygame.image.load("map.png")
    rect = bg.get_rect()

    # Le titre de la fenêtre
    pygame.display.set_caption("Virus Gate")

    # L'objet Joueur
    joueur = Player()

    # On récupère les informations de l'écran
    screen_info = pygame.display.Info()
    w, h = screen_info.current_w, screen_info.current_h


    # définition des dimensions du bouton
    largeur_bouton = 100
    hauteur_bouton = 50


    # création de la police puis du texte du bouton
    texte_bouton = pygame.font.Font(None, 24).render("X", True, (255, 255, 255))
    rectangle_bouton = pygame.Rect(100, 100, largeur_bouton, hauteur_bouton)
    transparent_surface = pygame.Surface((largeur_bouton, hauteur_bouton), pygame.SRCALPHA)

    # Remplir la surface transparente avec une transparence totale
    transparent_surface.fill((0, 0, 0, 0))
    transparent_surface.blit(texte_bouton, (0, 0))
    pygame.draw.rect(transparent_surface, (0, 0, 0, 0), transparent_surface.get_rect(), 1)

    obstacles = [pygame.Rect(1000, 1000, 50, 50)]

    running = True
    while running:
        maj = pygame.event.get()

        for event in maj:
            if event.type == pygame.QUIT:
                running = False
                quit()
                return  # On return pour quitter la fonction start
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rectangle_bouton.collidepoint(event.pos):
                    running = False
                    quit()
                    return  # On return pour quitter la fonction start

        screen.fill((255, 255, 255))
        rect = rect.move(0, 0)
        screen.blit(bg, rect)

        # On affiche la croix à l'écran
        screen.blit(transparent_surface, rectangle_bouton)

        # On affiche les obstacles
        for element in obstacles:
            pygame.draw.rect(screen, (0, 0, 0), element)

        joueur.update(maj, screen, obstacles)
        
        pygame.display.update()

start()
