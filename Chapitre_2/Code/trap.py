import pygame
import math
import calculs
from player import Player
# import player

class Trap:
    def __init__(self, posx: int, posy: int):
        self.range = 100
        self.posx = posx
        self.posy = posy
        self.cote = 50

    def update(self, screen, player: Player):
        # Si un joueur est à portée de tir, on le ralentit
        if calculs.distance(self.posx, self.posy, player.posx, player.posy) <= self.range:
            player.ralentissement = 0.7
            # On ajoute la tour sur l'écran
            pygame.draw.rect(screen, 'RED', (-self.posx - self.cote / 2, -self.posy - self.cote / 2, self.cote, self.cote))
        else:
            # print(calculs.distance(self.posx, self.posy, player.posx, player.posy))
            # On ajoute la tour sur l'écran
            pygame.draw.rect(screen, 'GREEN', (-self.posx - self.cote / 2, -self.posy - self.cote / 2, self.cote, self.cote))
        
        self.draw_circle_alpha(screen, (50, 50, 50, 100), (-self.posx, -self.posy), self.range)

    def draw_circle_alpha(self, surface, color, center, radius):
        """Source : https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame"""
        target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surf, color, (radius, radius), radius)
        surface.blit(shape_surf, target_rect)