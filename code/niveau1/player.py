import pygame


class Player:
    def __init__(self):
        self.posx = 0
        self.posy = -1000
        self.speed = 10  # La vitesse du déplacement horizontal
        self.vitesseVerticale = 0
        self.jump_height = 50

        # Par défaut, le joueur est immobile
        self.mouvements = {"jump": False, "left": False, "right": False}
    
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

        # Par défaut, il est possible de bouger
        self.canMove = {"left": True, "right": True, "down": True, "up": True}

        # Les touches du clavier
        if self.mouvements["left"]:
            # On vérifie s'il y a un obstacle
            for element in obstacles:
                if pygame.Rect.colliderect(pygame.Rect(-self.posx - self.speed,-self.posy,30,30), element):
                    self.canMove["left"] = False
            if self.canMove["left"]:
                self.posx += self.speed

        if self.mouvements["right"]:
            # On vérifie s'il y a un obstacle
            for element in obstacles:
                if pygame.Rect.colliderect(pygame.Rect(-self.posx + self.speed,-self.posy,30,30), element):
                    self.canMove["right"] = False
            if self.canMove["right"]:
                self.posx -= self.speed

        if self.mouvements["jump"]:
            if self.posy == -1000:  # Si le joueur n'est pas en train de sauter
                self.vitesseVerticale = self.jump_height

        # La physique
        if self.posy > -1000 or self.vitesseVerticale > 0:
            # On vérifie s'il y a un obstacle
            for element in obstacles:
                if pygame.Rect.colliderect(pygame.Rect(-self.posx,-self.posy - self.vitesseVerticale,30,30), element):
                    self.canMove["down"] = False
            if self.canMove["down"]:
                self.vitesseVerticale -= 10
        elif self.canMove["down"]:
            self.vitesseVerticale = 0
            self.posy = -1000
        if (self.vitesseVerticale > 0 and self.canMove["up"]) or (self.vitesseVerticale < 0 and self.canMove["down"]):
            self.posy += self.vitesseVerticale

        self.rectangle = pygame.Rect(-self.posx,-self.posy,30,30)

        # Gestion des obstacles
        for element in obstacles:
            while pygame.Rect.colliderect(self.rectangle, element):
                self.posy -= 10
                self.canMove["right"] = False
                self.rectangle = pygame.Rect(-self.posx,-self.posy,30,30)

        # On ajoute le joueur sur l'écran
        pygame.draw.rect(screen, 'BLUE',(-self.posx,-self.posy,30,30))
