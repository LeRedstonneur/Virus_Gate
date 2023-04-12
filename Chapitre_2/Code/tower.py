import pygame
import math
import Chapitre_2.Code.calculs as calculs
from Chapitre_2.Code.player import Player
# import player

class Tower:
    def __init__(self, type: str, posx: int, posy: int):
        if type == "classique":
            self.range = 500
            self.reloadTime = 6
            self.bulletSpeed = 10
        elif type == "degats_de_zone":
            self.range = 500
            self.reloadTime = 30
            self.bulletSpeed = 5
        elif type == "sniper":
            self.range = 500
            self.reloadTime = 120
            self.bulletSpeed = 18
        else:
            self.range = 500
            self.reloadTime = 60
            self.bulletSpeed = 50
        self.type = type
        self.canShoot = True
        self.currentReload = 0
        self.posx = posx
        self.posy = posy
        self.cote = 50
        self.projectiles = []

    def update(self, screen, player: Player, obstacles: list, padding, pause=False):
        if not pause:
            # Rechargement
            if not self.canShoot and self.currentReload < self.reloadTime:
                self.currentReload += 1
            if self.currentReload == self.reloadTime:
                self.canShoot = True
        
        # Si un joueur est à portée de tir, on tire dans sa direction
        if calculs.distance(self.posx, self.posy, player.posx, player.posy) <= self.range:
            if self.canShoot and not pause:
                self.tirer(self.posx, self.posy, player.posx - (player.largeur / 2), player.posy - (player.hauteur / 2), self.type == "degats_de_zone", padding)
            # On ajoute la tour sur l'écran
            pygame.draw.rect(screen, 'RED', (-self.posx - self.cote / 2 + padding, -self.posy - self.cote / 2, self.cote, self.cote))

        else:
            # On ajoute la tour sur l'écran
            pygame.draw.rect(screen, 'GREEN', (-self.posx - self.cote / 2 + padding, -self.posy - self.cote / 2, self.cote, self.cote))

        # On actualise chaque projectile
        for projectile in self.projectiles:
            projectile.update(screen, player, obstacles, padding)
            if projectile.to_delete:
                self.projectiles.remove(projectile)
        if pause:  # Si le jeu est en pause
            self.projectiles = []  # On supprime les projectiles
            pygame.draw.rect(screen, (25, 25, 25), (-self.posx - self.cote / 2 + 5 + padding, -self.posy - self.cote / 2 + 5, 40, 40))  # On affiche les tours en gris
    
    def tirer(self, x1: float, y1: float, x2: float, y2: float, explosif: bool, padding) -> None:
        """En fonction de la position d'une tour située en x1 et y1, tire un projectile vers le joueur situé en x2 et y2"""
        angle = math.atan2(y2 - y1, (x2) - (x1))
        v_horizontale = self.bulletSpeed * math.cos(angle)
        v_verticale = self.bulletSpeed * math.sin(angle)
        self.projectiles.append(Projectile(x1, y1, v_horizontale, v_verticale, explosif))
        self.canShoot = False
        self.currentReload = 0


class Projectile:
    def __init__(self, posx: int, posy: int, vitesseHorizontale: int, vitesseVerticale: int, explosif: bool):
        self.posx = posx
        self.posy = posy
        self.vitesseHorizontale = vitesseHorizontale
        self.vitesseVerticale = vitesseVerticale
        self.to_delete = False
        self.cote = 20
        self.explosif = explosif
    
    def update(self, screen, joueur: Player, obstacles: list, padding):
        self.posx += self.vitesseHorizontale
        self.posy += self.vitesseVerticale
        pygame.draw.rect(screen, 'WHITE', (-self.posx - self.cote / 2 + padding, -self.posy - self.cote / 2, self.cote, self.cote))
        rayon = 25
        if self.explosif:
            self.draw_circle_alpha(screen, (255, 0, 0, 100), (-self.posx + padding, -self.posy), rayon)
            
        for obstacle in obstacles:
            if obstacle.colliderect(-self.posx - self.cote / 2, -self.posy - self.cote / 2, self.cote, self.cote):
                self.to_delete = True
                if self.explosif:
                    # self.draw_circle_alpha(screen, (255, 0, 0, 100), (-self.posx, -self.posy), 50)
                    if calculs.distance(self.posx, self.posy, joueur.posx, joueur.posy) <= rayon:
                        joueur.vies -= 2
                        self.to_delete = True
                        joueur.pause = 180
                
        if pygame.Rect(-self.posx - self.cote / 2, -self.posy - self.cote / 2, self.cote, self.cote).colliderect(-joueur.posx, -joueur.posy, joueur.largeur, joueur.hauteur):
            joueur.vies -= 1 + int(self.explosif)
            if joueur.vies < 0:
                joueur.vies = 0
            # On évite de se retrouver face à un nombre de vies négatif
            self.to_delete = True
            joueur.pause = 180

    def draw_circle_alpha(self, surface, color, center, radius):
        """Source : https://stackoverflow.com/questions/6339057/draw-a-transparent-rectangles-and-polygons-in-pygame"""
        target_rect = pygame.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
        shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
        pygame.draw.circle(shape_surf, color, (radius, radius), radius)
        surface.blit(shape_surf, target_rect)
