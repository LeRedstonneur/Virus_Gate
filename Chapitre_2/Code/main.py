import pygame
from player import Player
from tower import Tower
from trap import Trap
from quit import leave
from obstacles import obstacles
from obstacles import towers
from obstacles import traps
# from obstacles import spikes


def start():
    """Cette fonction est appelée par l'écran d'accueil pour démarrer le niveau"""
    pygame.init()

    # Gestion de l'écran
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    bg = pygame.image.load("../Assets/a.jpg")
    rect = bg.get_rect()

    # Le titre de la fenêtre
    pygame.display.set_caption("Virus Gate")

    # L'objet Joueur
    joueur = Player()

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

    # Les obstacles sont directement includes depuis obstacles.py



    # On récupère les informations de l'écran
    screen_info = pygame.display.Info()
    h, w = screen_info.current_h, screen_info.current_w
    # On ajoute des obstacles correspondant aux bords de l'écran
    obstacles.append(pygame.Rect(-1, 0, 1, h))  # Gauche
    #obstacles.append(pygame.Rect(w, 0, 1, h))  # Droite

    running = True

    padding = 0

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    leave()
                    return
                if event.key == pygame.K_RETURN:
                    joueur = Player()
                    for tour in towers:
                        tour.projectiles = []
                    running = True

        if running:
            screen.fill((255, 255, 255))
            rect = rect.move(0, 0)
            screen.blit(bg, rect)

            # On affiche la croix à l'écran
            screen.blit(transparent_surface, rectangle_bouton)

            # On affiche les obstacles
            for element in obstacles:
                temp = element.move(padding, 0)
                pygame.draw.rect(screen, (0, 0, 0), temp)

            # On s'occupe des tours si le joueur n'a pas été touché
            if joueur.pause == 0:
                for tour in towers:
                    tour.update(screen, joueur, obstacles, padding)
            else:
                for tour in towers:
                    tour.update(screen, joueur, obstacles, padding, pause=True)
                joueur.pause -= 1

            joueur.ralentissement = 0
            # On ralentit éventuellement le joueur
            for trap in traps:
                trap.update(screen, joueur, padding)

            joueur.update(pygame.key.get_pressed(), screen, obstacles, padding)

            pygame.display.update()

            if -joueur.posx < 750:
                padding = 0
            else:
                padding = joueur.posx + 750

            if joueur.vies <= 0:
                running = False
        else:
            # Si on arrive ici, c'est que la partie est finie

            # on devrait afficher au milieu de l'écran que la partie est finie
            font = pygame.font.SysFont("Arial", 72)
            text = font.render("Partie terminée", True, (128, 0, 0))
            screen.blit(text, (320 - text.get_width() // 2, 240 - text.get_height() // 2))

            pygame.display.flip()


start()
