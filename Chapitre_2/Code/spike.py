import pygame
import math
from Chapitre_2.Code.player import Player

class Spike:
    def __init__(self, posx: int, posy: int):
        self.posx = posx
        self.posy = posy
        self.cote = 50
        self.triangle_height = int(math.sqrt(3) * self.cote / 2)  # Hauteur du triangle isocèle

    def update(self, screen, player: Player, padding):
        triangle_points_padded = [(-self.posx - self.cote / 2 + padding, -self.posy + self.triangle_height / 2),
                                  (-self.posx + self.cote / 2 + padding, -self.posy + self.triangle_height / 2),
                                  (-self.posx + padding, -self.posy - self.triangle_height / 2)]

        joueur = pygame.Rect(-player.posx, -player.posy, player.largeur, player.hauteur)

        # Si le joueur rentre en collision avec le spike, on lui enlève toutes ses vies
        if pygame.draw.polygon(screen, 'RED', triangle_points_padded).move(-padding, 0).colliderect(joueur):
            player.vies = 0
        
        # La condition a déjà affiché le spike, on s'arrête là