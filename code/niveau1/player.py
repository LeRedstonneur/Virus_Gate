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
                if event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    self.mouvements["left"] = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.mouvements["right"] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.mouvements["jump"] = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_q:
                    self.mouvements["left"] = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.mouvements["right"] = False

        # Les touches du clavier
        if self.mouvements["left"]:
            self.posx += self.speed
        if self.mouvements["right"]:
            self.posx -= self.speed
        if self.mouvements["jump"]:
            if self.posy == -1000:  # Si le joueur n'est pas en train de sauter
                self.vitesseVerticale = self.jump_height

        # La physique
        if self.posy > -1000 or self.vitesseVerticale > 0:
            self.vitesseVerticale -= 10
        else:
            self.vitesseVerticale = 0
            self.posy = -1000
        self.posy += self.vitesseVerticale
        
        # On ajoute le joueur sur l'écran
        pygame.draw.rect(screen, 'BLUE',(-self.posx,-self.posy,30,30))

        self.rectangle = pygame.Rect(-self.posx,-self.posy,30,30)

        # Gestion des obstacles
        for element in obstacles:
            while self.rectangle.colliderect(element):
                # self.posx += 1
                # self.rectangle = pygame.Rect(-self.posx,-self.posy,30,30)
                # La variable collision_rect contient la zone de collision
                self.collision_rect = self.rectangle.clip(element)
                if self.collision_rect.width > self.collision_rect.height:
                    if self.collision_rect.x > element.x:
                        self.posx += 100
                        self.rectangle = pygame.Rect(-self.posx,-self.posy,30,30)
                    else:
                        self.posx -= 100
                        self.rectangle = pygame.Rect(-self.posx,-self.posy,30,30)
                else:
                    pass
                    #self.posy += 500
                    #self.rectangle = pygame.Rect(-self.posx,-self.posy,30,30)
