import pygame
from player import Player
from tower import Tower
from trap import Trap
from quit import leave


def start():
    """Cette fonction est appelée par l'écran d'accueil pour démarrer le niveau"""
    pygame.init()

    # Gestion de l'écran
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    bg = pygame.image.load("map.jpg")
    rect = bg.get_rect()

    # Le titre de la fenêtre
    pygame.display.set_caption("Virus Gate")

    # L'objet Joueur
    joueur = Player()

    # On récupère les informations de l'écran
    # screen_info = pygame.display.Info()
    # w, h = screen_info.current_w, screen_info.current_h

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

    clock = pygame.time.Clock()

    obstacles = [pygame.Rect(1000, 950, 50, 50), pygame.Rect(0, 1010, 1920, 500), pygame.Rect(900, 700, 50, 250)]
    towers = [Tower("classique", -500, -500), Tower("degats_de_zone", -1000, -500)]
    traps = [Trap(-750, -1000)]

    while True:
        clock.tick(60)

        maj = pygame.event.get()

        for event in maj:
            if event.type == pygame.QUIT:
                leave()
                return  # On return pour quitter la fonction start
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rectangle_bouton.collidepoint(event.pos):
                    leave()
                    return  # On return pour quitter la fonction start

        screen.fill((255, 255, 255))
        rect = rect.move(0, 0)
        screen.blit(bg, rect)

        # On affiche la croix à l'écran
        screen.blit(transparent_surface, rectangle_bouton)

        # On affiche les obstacles
        for element in obstacles:
            pygame.draw.rect(screen, (0, 0, 0), element)

        # On s'occupe des tours si le joueur n'a pas été touché
        if joueur.pause == 0:
            for tour in towers:
                tour.update(screen, joueur, obstacles)
        else:
            for tour in towers:
                tour.update(screen, joueur, obstacles, pause=True)
            joueur.pause -= 1

        joueur.ralentissement = 0
        # On ralentit éventuellement le joueur
        for trap in traps:
            trap.update(screen, joueur)

        joueur.update(maj, screen, obstacles)

        pygame.display.update()

        if joueur.vies <= 0:
            # A faire : fin de partie
            leave()
            return


start()

