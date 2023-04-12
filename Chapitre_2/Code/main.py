def color_from_float(f: float) -> tuple:
    if f == 0:
        return 255, 0, 0  # rouge
    elif f == 1:
        return 0, 255, 0  # vert
    else:
        r = int((1 - f) * 255)  # rouge (max à 255 si f = 0)
        g = int(f * 255)  # vert (max à 255 si f = 1)
        return r, g, 0  # jaune si f = 0.5


def start():
    """Cette fonction est appelée par l'écran d'accueil pour démarrer le niveau"""
    import pygame
    # Puisque le code s'exécute depuis l'accueil, on doit parcourir l'arborescence pour
    # accéder aux fichiers situés au même endroit que le présent fichier
    from Chapitre_2.Code.player import Player
    from Chapitre_2.Code.tower import Tower
    from Chapitre_2.Code.trap import Trap
    from Chapitre_2.Code.quit import leave
    from Chapitre_2.Code.obstacles import obstacles, spikes, checkpoints, towers, traps
    from Chapitre_2.Code.pieces import piecestemp

    pygame.init()

    # Gestion de l'écran
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    bg = pygame.image.load("../Chapitre_2/Assets/a.jpg")
    rect = bg.get_rect()
    pygame.display.set_caption("Virus Gate - Chapitre 2")

    # L'objet Joueur
    joueur = Player()

    # La croix pour retourner à l'accueil
    largeur_bouton = 100
    hauteur_bouton = 50
    texte_bouton = pygame.font.Font(None, 24).render("X", True, (255, 255, 255))
    rectangle_bouton = pygame.Rect(100, 100, largeur_bouton, hauteur_bouton)
    transparent_surface = pygame.Surface((largeur_bouton, hauteur_bouton), pygame.SRCALPHA)
    transparent_surface.fill((0, 0, 0, 0))
    transparent_surface.blit(texte_bouton, (0, 0))
    pygame.draw.rect(transparent_surface, (0, 0, 0, 0), transparent_surface.get_rect(), 1)

    # On charge les conditions pour la fin de partie
    font = pygame.font.SysFont("Arial", 72)
    font2 = pygame.font.SysFont("Arial", 36)
    couleur = (200, 200, 200)  # La couleur des textes en petit

    # On initialise une horloge pour limiter ensuite le framerate
    clock = pygame.time.Clock()

    # Les obstacles sont directement inclus depuis obstacles.py
    obstacles.append(pygame.Rect(-1, 0, 1, pygame.display.Info().current_h))  # On ajoute à gauche du spawn un obstacle

    pieces = [i for i in piecestemp]  # Copie élément par élément
    piecesatrouver = [i for i in piecestemp]

    # Le décalage visuel des obstacles pour créer un défilement
    padding = 0

    running = True
    win = False
    while True:
        # On limite les FPS, pour que le jeu ne soit pas trop fluide (donc trop rapide) sur les plus grosses machines
        clock.tick(60)

        # La gestion des évènements (inputs utilisateur)
        for event in pygame.event.get():
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
                    return  # On return pour quitter la fonction start
                if event.key == pygame.K_RETURN:  # Retour au checkpoint
                    if joueur.checkpoint == 0:
                        joueur = Player()
                        for tour in towers:
                            tour.projectiles = []
                        running = True
                        pieces = [i for i in piecestemp]  # On remet la liste des pièces comme au départ
                    else:
                        joueur.posx = -checkpoints[joueur.checkpoint - 1][0] - 10
                        joueur.posy = -checkpoints[joueur.checkpoint - 1][1] - 10
                        for tour in towers:
                            tour.projectiles = []
                        joueur.vies = joueur.vies_max
                        joueur.pieces = joueur.pieces_validees
                        pieces = [i for i in piecesatrouver]
                        running = True

        # Si le jeu est en cours
        if running:
            # On affiche le fond d'écran
            screen.blit(bg, rect)

            # On affiche la croix pour quitter à l'écran
            screen.blit(transparent_surface, rectangle_bouton)

            # On affiche les obstacles
            for element in obstacles:
                temp = element.move(padding, 0)
                pygame.draw.rect(screen, (0, 0, 0), temp)

            # On affiche les pièces
            for element in pieces:
                if element[0] + padding > 0:
                    pygame.draw.circle(screen, (255, 255, 0), (element[0] + padding, element[1]), 25)

            # On affiche les checkpoints validés
            for element in range(joueur.checkpoint):
                pygame.draw.rect(screen, (128, 128, 128),
                                 pygame.Rect(checkpoints[element][0] + padding, checkpoints[element][1], 50, 50))

            # On affiche les checkpoints à compléter
            for element in range(joueur.checkpoint, len(checkpoints)):
                pygame.draw.rect(screen, (255, 255, 255),
                                 pygame.Rect(checkpoints[element][0] + padding, checkpoints[element][1], 50, 50))

            # On affiche d'une couleur différente le dernier checkpoint (fin de la partie)
            pygame.draw.rect(screen, (0, 255, 255),
                             pygame.Rect(checkpoints[-1][0] + padding, checkpoints[-1][1], 50, 50))

            # On update les tours si le joueur n'a pas été touché (sinon, elles ne tirent pas)
            for tour in towers:
                tour.update(screen, joueur, obstacles, padding, pause=(joueur.pause != 0))

            # On ralentit éventuellement le joueur en le prenant dans un trap
            # Si ralentissement == 0, le joueur a une vitesse normale
            # Si ralentissement == 1, le joueur ne peut plus bouger ni sauter
            joueur.ralentissement = 0  # Par défaut, le joueur n'est pas ralenti
            for element in traps + spikes:
                element.update(screen, joueur, padding)

            # On met à jour le joueur dans son environnement
            joueur.update(pygame.key.get_pressed(), screen, obstacles, padding, pieces, checkpoints, piecesatrouver)

            # On s'occupe du défilement de la map (padding)
            if -joueur.posx < 750:
                padding = 0
            else:
                padding = joueur.posx + 750

            # Si le joueur n'a plus de vies, on arrête le jeu
            if joueur.vies <= 0:
                running = False
                win = False

            # Si le joueur a atteint le dernier checkpoint, il a gagné
            if joueur.checkpoint == len(checkpoints):
                running = False
                win = True
                joueur.checkpoint = 0  # Pour qu'il puisse recommencer s'il le souhaite

        # Si le jeu n'est pas en cours (le joueur est mort ou la partie est terminée)
        else:  # Si on arrive ici, c'est que la partie est finie
            if win:
                text = font.render("Vous avez gagné !", True, (100, 100, 255))
                text2 = font2.render("Recommencer : Entrée", True, couleur)
                text3 = font2.render("Quitter : Echap", True, couleur)

                text4 = font2.render(f"Pièces : {joueur.pieces}/{len(piecestemp)}", True,
                                     color_from_float(joueur.pieces / len(piecestemp)))
            else:
                text = font.render("Vous êtes mort", True, (200, 0, 0))
                text2 = font2.render("Checkpoint : Entrée", True, couleur)
                text3 = font2.render("Quitter : Echap", True, couleur)
                text4 = font2.render(f"Progression : {joueur.checkpoint}/{len(checkpoints)}", True, (100, 100, 100))

            # Quels que soient les textes, on les affiche
            screen.blit(text, (250, 250))
            screen.blit(text2, (250, 450))
            screen.blit(text3, (250, 500))
            screen.blit(text4, (250, 400))

        # Dans tous les cas, on met à jour l'affichage de tous les éléments
        pygame.display.update()
