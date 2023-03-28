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
    bg = pygame.image.load("./assets/a.jpg")
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

    obstacles = [pygame.Rect(1100, 950, 50, 50), pygame.Rect(0, 1010, 10000, 500), pygame.Rect(1000, 700, 50, 250), pygame.Rect(500, 950, 150, 50), 
    pygame.Rect(660, 870, 60, 20), pygame.Rect(760, 790, 60, 20), pygame.Rect(860, 710, 60, 20), pygame.Rect(1400, 700, 250, 350), pygame.Rect(1300, 845, 60, 20),
    pygame.Rect(1350, 935, 60, 20), pygame.Rect(1350, 760, 60, 20), pygame.Rect(1750, 650, 80, 20), pygame.Rect(2000, 850, 80, 20), pygame.Rect(2200, 780, 100, 20),
    pygame.Rect(2300, 910, 250, 100), pygame.Rect(2300, 680, 250, 120), pygame.Rect(2200, 960, 50, 50), pygame.Rect(2250, 910, 50, 100), pygame.Rect(2400, 640, 150, 50),
    pygame.Rect(2400, 590, 150, 50), pygame.Rect(2625, 830, 50, 200), pygame.Rect(2800, 830, 50, 180), pygame.Rect(2975, 830, 50, 180)]

    towers = [Tower("classique", -600, -600), Tower("degats_de_zone", -1000, -450), Tower("classique", -1900, -1000), Tower("degats_de_zone",-2250, -425), 
    Tower("classique", -2740, -1000), Tower("classique", -2915, -1000)]

    traps = [Trap(-800, -1000), Trap(-2225, -935), Trap(-2175, -985)]
    #spikes = [Spike(-750, -1100)]

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
