import pygame


class Player:
    def __init__(self):
        self.posx = 0
        self.posy = -580
        self.speed = 10  # La vitesse du déplacement horizontal
        self.vitesseVerticale = 0
        self.jump_height = 25
        self.gravite = 5
        self.largeur = 30
        self.hauteur = 30

        # Par défaut, le joueur est immobile
        self.mouvements = {"jump": False, "left": False, "right": False}
        self.canMove = {"left": True, "right": True, "down": True, "up": True}
        self.rectangle = pygame.Rect(-self.posx, -self.posy, self.largeur, self.hauteur)

    def update(self, maj, screen, obstacles):
        for event in maj:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.mouvements["jump"] = True
                    self.canMove["left"] = True
                    self.canMove["right"] = True
                if event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    self.mouvements["left"] = True
                    self.canMove["right"] = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.mouvements["right"] = True
                    self.canMove["left"] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.mouvements["jump"] = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    self.mouvements["left"] = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.mouvements["right"] = False

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

        # Gestion des obstacles
        for element in obstacles:
            while pygame.Rect.colliderect(self.rectangle, element):
                # self.posy += 10
                self.canMove["right"] = False
                self.rectangle = pygame.Rect(-self.posx, -self.posy, self.largeur, self.hauteur)

        # On ajoute le joueur sur l'écran
        pygame.draw.rect(screen, 'BLUE', (-self.posx, -self.posy, self.largeur, self.hauteur))

    def surObstacle(self, obstacles) -> bool:
        joueur_rect = pygame.Rect(-self.posx, -self.posy + 1, self.largeur, self.hauteur)
        for obstacle in obstacles:
            if joueur_rect.colliderect(pygame.Rect(obstacle[0], obstacle[1], obstacle[2], obstacle[3])):
                # print("sur obstacle")
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
