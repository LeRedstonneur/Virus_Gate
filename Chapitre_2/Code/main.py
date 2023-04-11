import pygame

def start():
    from Chapitre_2.Code.player import Player
    from Chapitre_2.Code.tower import Tower
    from Chapitre_2.Code.trap import Trap
    from Chapitre_2.Code.quit import leave
    from Chapitre_2.Code.obstacles import obstacles, spikes, checkpoints, towers, traps
    from Chapitre_2.Code.pieces import piecestemp

    """Cette fonction est appelée par l'écran d'accueil pour démarrer le niveau"""
    pygame.init()

    # Gestion de l'écran
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    bg = pygame.image.load("../Chapitre_2/Assets/a.jpg")
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

    pieces = [i for i in piecestemp]  # Copie élément par élément 
    piecesatrouver = [i for i in piecestemp]

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

        if running:
            screen.fill((255, 255, 255))
            rect = rect.move(0, 0)
            screen.blit(bg, rect)

            # On affiche la croix pour quitter à l'écran
            screen.blit(transparent_surface, rectangle_bouton)

            # On affiche les obstacles
            for element in obstacles:
                temp = element.move(padding, 0)
                pygame.draw.rect(screen, (0, 0, 0), temp)

            # On affiche les pièces
            for element in pieces:
                pygame.draw.circle(screen, (255, 255, 0), (element[0] + padding, element[1]), 25)

            # On affiche les checkpoints validés
            for element in range(joueur.checkpoint):
                pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(checkpoints[element][0] + padding, checkpoints[element][1], 50, 50))

            # On affiche les checkpoints à compléter
            for element in range(joueur.checkpoint, len(checkpoints)):
                pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(checkpoints[element][0] + padding, checkpoints[element][1], 50, 50))

            # On affiche d'une couleur différente le dernier checkpoint (fin de la partie)
            pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(checkpoints[-1][0] + padding, checkpoints[-1][1], 50, 50))

            # On actualise les tours si le joueur n'a pas été touché
            for tour in towers:
                tour.update(screen, joueur, obstacles, padding, pause=(joueur.pause!=0))
            if joueur.pause > 0:
                joueur.pause -= 1

            joueur.ralentissement = 0
            # On ralentit éventuellement le joueur en le prenant dans un trap
            for trap in traps:
                trap.update(screen, joueur, padding)
            
            for spike in spikes:
                spike.update(screen, joueur, padding)
            

            joueur.update(pygame.key.get_pressed(), screen, obstacles, padding, pieces, checkpoints, piecesatrouver)

            pygame.display.update()

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
                joueur.checkpoint = 0

        else:
            # Si on arrive ici, c'est que la partie est finie
            font = pygame.font.SysFont("Arial", 72)
            font2 = pygame.font.SysFont("Arial", 36)
            couleur = (200, 200, 200)  # La couleur des textes en petit
            if win:
                text = font.render("Vous avez gagné !", True, (100, 100, 255))
                text2 = font2.render("Recommencer : Entrée", True, couleur)
                text3 = font2.render("Quitter : Echap", True, couleur)

                def color_from_float(f):
                    if f == 0:
                        return (255, 0, 0)  # rouge
                    elif f == 1:
                        return (0, 255, 0)  # vert
                    else:
                        r = int((1-f)*255)  # rouge (max à 255 si f = 0)
                        g = int(f*255)      # vert (max à 255 si f = 1)
                        return (r, g, 0)    # jaune si f = 0.5

                text4 = font2.render(f"Pièces : {joueur.pieces}/{len(piecestemp)}", True, color_from_float(joueur.pieces/len(piecestemp)))
            else:  
                text = font.render("Vous êtes mort", True, (200, 0, 0))
                text2 = font2.render("Checkpoint : Entrée", True, couleur)
                text3 = font2.render("Quitter : Echap", True, couleur)
                text4 = font2.render(f"Progression : {joueur.checkpoint}/{len(checkpoints)}", True, (100, 100, 100))
                
            screen.blit(text, (250, 250))
            screen.blit(text2, (250, 450))
            screen.blit(text3, (250, 500))
            screen.blit(text4, (250, 400))

            pygame.display.flip()