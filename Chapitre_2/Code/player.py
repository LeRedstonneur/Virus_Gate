import pygame
import time


class Player:
    def __init__(self):
        self.posx = 0
        self.posy = -580
        self.vitesse = 10  # La vitesse du déplacement horizontal
        self.vitesseVerticale = 0
        self.hauteur_de_saut = 22
        self.gravite = 3
        self.largeur = 30
        self.hauteur = 30
        self.vies_max = 5
        self.vies = self.vies_max  # Au début, le joueur commence avec toutes ses vies
        self.pause = 0  # Quand le joueur est touché, plus aucune tour ne tire pendant une certaine durée
        self.ralentissement = 4
        self.speed = int(self.vitesse * (1 - self.ralentissement))
        self.jump_height = int(self.hauteur_de_saut * (1 - self.ralentissement / 2))
        self.pieces = 0  # Les pièces ramassées par le joueur
        self.pieces_validees = 0  # Les pièces ramassées par le joueur au dernier moment où il a été sur un checkpoint
        self.checkpoint = 0  # Le numéro du checkpoint sur lequel le joueur est

        # Par défaut, le joueur est immobile
        self.mouvements = {"jump": False, "left": False, "right": False}
        self.canMove = {"left": True, "right": True, "down": True, "up": True}
        self.rectangle = pygame.Rect(-self.posx, -self.posy, self.largeur, self.hauteur)

        self.last_jump_time = time.time()

    def update(self, keys, screen, obstacles, padding, pieces, checkpoints, piecesatrouver):
        self.speed = int(self.vitesse * (1 - self.ralentissement))
        self.jump_height = int(self.hauteur_de_saut * (1 - self.ralentissement / 2))
        self.rectangle = pygame.Rect(-self.posx, -self.posy, self.largeur, self.hauteur)

        # Lecture des touches (opti)
        # On ajoute un délai entre les sauts
        if keys[pygame.K_SPACE] and (time.time() - self.last_jump_time) > 0.3:
            self.mouvements["jump"] = True
            self.canMove["left"] = True
            self.canMove["right"] = True
            self.last_jump_time = time.time()
        else:
            self.mouvements["jump"] = False

        self.mouvements["left"] = keys[pygame.K_LEFT] or keys[pygame.K_q]
        self.mouvements["right"] = keys[pygame.K_RIGHT] or keys[pygame.K_d]

        self.canMove["left"] = not self.mouvements["right"]
        self.canMove["right"] = not self.mouvements["left"]

        # Par défaut, il est possible de bouger dans toutes les directions
        self.canMove = {"left": True, "right": True, "down": True, "up": True}

        # Les touches du clavier
        if self.mouvements["left"]:
            # On vérifie s'il y a un obstacle
            for element in obstacles:
                if pygame.Rect.colliderect(pygame.Rect(-self.posx - self.speed, -self.posy, 30, 30), element):
                    self.canMove["left"] = False
            if self.canMove["left"]:
                self.posx += self.speed

        if self.mouvements["right"]:
            # On vérifie s'il y a un obstacle
            for element in obstacles:
                if pygame.Rect.colliderect(pygame.Rect(-self.posx + self.speed, -self.posy, 30, 30), element):
                    self.canMove["right"] = False
            if self.canMove["right"]:
                self.posx -= self.speed

        if self.mouvements["jump"]:
            if self.surObstacle(obstacles):  # Si le joueur touche le sol
                self.vitesseVerticale = self.jump_height

        # La physique des chutes
        if self.vitesseVerticale < 0 and self.canMove["down"]:
            self.chute(obstacles)
        elif self.vitesseVerticale > 0 and self.canMove["up"]:
            self.saut(obstacles)

        if self.canMove["down"] and not self.surObstacle(obstacles):
            self.vitesseVerticale = max(self.vitesseVerticale - self.gravite, -1000)
            # Borne supérieure à la vitesse de chute (peut être assimilé aux frottements de l'air)

        # On empêche de passer sous la map
        if self.posy < -2000:
            self.posy = 500
            self.vitesseVerticale = 0
        elif self.posy > 2000:
            self.posy = -1000
            self.vitesseVerticale = 0

        # Gestion des pièces
        for piece in pieces:
            distance = ((-self.posx - piece[0])**2 + (-self.posy - piece[1])**2)**0.5
            if distance <= 50:
                pieces.remove(piece)
                self.pieces += 1

        # On valide un nouveau checkpoint
        if self.checkpoint < len(checkpoints) and pygame.Rect(checkpoints[self.checkpoint][0], checkpoints[self.checkpoint][1], 50, 50).colliderect(self.rectangle):
            self.checkpoint += 1
            self.pieces_validees = self.pieces
            piecesatrouver.clear()
            piecesatrouver.extend([i for i in pieces])

        # En cas de retour sur le dernier checkpoint déjà validé, on sauvegarde quand même les pièces
        if self.checkpoint > 0 and pygame.Rect(checkpoints[self.checkpoint - 1][0], checkpoints[self.checkpoint - 1][1], 50, 50).colliderect(self.rectangle):
            self.pieces_validees = self.pieces
            piecesatrouver.clear()
            piecesatrouver.extend([i for i in pieces])

        # On ajoute le joueur sur l'écran
        if self.pause == 0:
            pygame.draw.rect(screen, 'BLUE', (-self.posx + padding, -self.posy, self.largeur, self.hauteur))
        else:
            pygame.draw.rect(screen, 'GRAY', (-self.posx + padding, -self.posy, self.largeur, self.hauteur))

        # On dessine la barre de vie sur l'écran
        pygame.draw.rect(screen, 'GREEN', (1000, 1800, 80, 100))
        font = pygame.font.SysFont("Arial", 36)
        text = font.render(f"{self.vies}/{self.vies_max}", True, (255, 255, 255))
        screen.blit(text, (1650, 1038))
        self.afficherVies()

        self.afficherPieces(screen)

    def surObstacle(self, obstacles) -> bool:
        joueur_rect = pygame.Rect(-self.posx, -self.posy + 1, self.largeur, self.hauteur)
        for obstacle in obstacles:
            if joueur_rect.colliderect(pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3])):
                self.canMove["down"] = False
                return True
        return False

    def sousObstacle(self, obstacles) -> bool:
        joueur_rect = pygame.Rect(-self.posx, -self.posy - 1, self.largeur, self.hauteur)
        for obstacle in obstacles:
            if joueur_rect.colliderect(pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3])):
                self.canMove["up"] = False
                return True
        return False

    def ajusterPosition(self, obstacles: list) -> int:
        """Retourne un entier contenant la position corrigée du joueur
        S'il était dans un obstacle, c'est sa position au-dessus de l'obstacle
        Sinon, c'est sa position inchangée"""
        for obs in obstacles:
            if pygame.Rect.colliderect(pygame.Rect(-self.posx, -self.posy, 30, 30), obs):
                return -obs.top + 30
        return self.posy

    def chute(self, obstacles: list) -> None:
        for _ in range(abs(self.vitesseVerticale)):
            self.posy -= 1
            if self.surObstacle(obstacles):
                self.vitesseVerticale = 0
                return

    def saut(self, obstacles: list) -> None:
        for _ in range(self.vitesseVerticale):
            self.posy += 1
            if self.sousObstacle(obstacles):
                self.vitesseVerticale = 0
                return

    def afficherVies(self) -> None:
        # Définition des dimensions et de la position du rectangle vert
        x, y = pygame.display.get_surface().get_size()
        largeur_rect_vert = 200
        hauteur_rect_vert = 30
        position_rect_vert = (x - largeur_rect_vert - 10, y - hauteur_rect_vert - 10)

        # Définition des dimensions et de la position du rectangle rouge
        largeur_rect_rouge = largeur_rect_vert * ((self.vies_max - self.vies) / self.vies_max)
        hauteur_rect_rouge = hauteur_rect_vert
        position_rect_rouge = position_rect_vert

        # Dessin des rectangles
        rect_vert = pygame.Rect(position_rect_vert, (largeur_rect_vert, hauteur_rect_vert))
        rect_rouge = pygame.Rect(position_rect_rouge, (largeur_rect_rouge, hauteur_rect_rouge))
        pygame.draw.rect(pygame.display.get_surface(), (0, 255, 0), rect_vert)
        pygame.draw.rect(pygame.display.get_surface(), (255, 0, 0), rect_rouge)

    def afficherPieces(self, screen):
        """Affiche le nombre de pièces collectées sur l'écran"""
        x, y = pygame.display.get_surface().get_size()

        texte = pygame.font.SysFont("Arial", 72).render(str(self.pieces), True, (255, 255, 255))
        screen.blit(texte, (x - 150, 35))

        pygame.draw.circle(screen, (255, 255, 0), (x - 40, 70), 25)