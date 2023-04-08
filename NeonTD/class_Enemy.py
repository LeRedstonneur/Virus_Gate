import pygame
import math
import time
import random
from groups import*

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tempx = float(x)
        self.tempy = float(y)
        self.path = [(600, 50), (50, 50), (50, 600), (400, 600), (400, 300), (700, 300), (700, 850)]
        self.current_checkpoint = 0
        self.destination = self.path[self.current_checkpoint]
        self.has_traversed = False 
        self.slowed_by = []
        self.slowing_towers = []
    
    def update(self):
        # calculer la distance et la direction vers la destination actuelle
        dx = self.destination[0] - self.rect.x
        dy = self.destination[1] - self.rect.y
        distance = math.hypot(dx, dy)
                
        if distance > 0 :
            direction = (dx / distance, dy / distance)
            self.tempx += float(direction[0] * self.speed)
            self.tempy += float(direction[1] * self.speed)
            self.rect.x = self.tempx
            self.rect.y = self.tempy
        
        if distance < self.speed or distance == 0:
            self.current_checkpoint += 1
            if self.current_checkpoint >= len(self.path):
                self.has_traversed = True # on est arrivé au dernier checkpoint, on peut supprimer l'ennemi
                self.groups()[0].remove(self)
                
            else:
                self.destination = self.path[self.current_checkpoint]

        if self.slowed_by: #Gestion du ralentissement
            for tower in self.slowed_by:
                if not tower.in_range(self):
                    self.reset_speed()
                    self.slowed_by.remove(tower)
        
    def take_damage(self, damage):
        self.health -= damage
    
    def slow(self, slowing_factor, tower):
        if tower not in self.slowing_towers:
            self.slowing_towers.append(tower)
            self.speed *= (1 - slowing_factor)

    def reset_speed(self):
        self.speed = self.original_speed
        for tower in self.slowing_towers:
            if not tower.in_range(self):
                self.slowing_towers.remove(tower)

    def is_dead(self):
        if self.health <= 0:
            self.groups()[0].remove(self)
            return True
        else:
            return False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def get_pos(self):
        return self.x, self.y

#-------------------------------------------------------------------------------------------------------------------------------------------#

class Croix(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Assets/Enemies/croix.png")
        self.speed = 3
        self.original_speed = self.speed
        self.health = 2

#-------------------------------------------------------------------------------------------------------------------------------------------#

class GrandeCroix(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Assets/Enemies/grande_croix.png")
        self.speed = 1
        self.original_speed = self.speed
        self.health = 20
        self.last_spawn_time = time.time()  # enregistrer l'heure actuelle
        self.spawn_interval = 10  # intervalle de spawn de 10 secondes

    def update(self):
        super().update()
        self.check_spawn_croix(enemy_group)  # vérifier si une nouvelle instance doit être créée

    def check_spawn_croix(self, enemy_group):
        # vérifier si le temps écoulé dépasse l'intervalle de spawn
        current_time = time.time()
        time_since_last_spawn = current_time - self.last_spawn_time
        if time_since_last_spawn >= self.spawn_interval:
            self.last_spawn_time = current_time
            self.spawn_croix(enemy_group)

    def spawn_croix(self, enemy_group):
        # créer 2 nouvelles instances de Croix autour de la GrandeCroix
        for _ in range(2):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(0, 20)
            x_offset = distance * math.cos(angle)
            y_offset = distance * math.sin(angle)

            x = self.rect.x + 25 + x_offset  # 25 pour le centre de la GrandeCroix (taille de 50x50)
            y = self.rect.y + 25 + y_offset

            croix = Croix(x, y)
            croix.current_checkpoint = self.current_checkpoint  # Ajouter cette ligne
            croix.destination = self.destination  # Ajouter cette ligne
            croix.tempx = x  # Ajouter cette ligne
            croix.tempy = y  # Ajouter cette ligne
            enemy_group.add(croix)

#-------------------------------------------------------------------------------------------------------------------------------------------#

class Losange(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Assets/Enemies/losange.png")
        self.speed = 1  # vitesse initiale lente
        self.original_speed = self.speed
        self.health = 6  # vie faible
        self.ignore_square = True  # ignore quasiment le carré
        self.speed_increase_rate = 0.02  # taux d'augmentation de la vitesse

    def update(self):
        super().update()
        self.increase_speed()

    def increase_speed(self):
        if self.speed < 20:  # vitesse maximale super rapide
            self.speed += self.speed_increase_rate
        else:
            self.speed = 20

#-------------------------------------------------------------------------------------------------------------------------------------------#
    
class Rectangle(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Assets/Enemies/rectangle.png")
        self.speed = 2.5
        self.original_speed = self.speed
        self.health = 15

#-------------------------------------------------------------------------------------------------------------------------------------------#

class Hexagone(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Assets/Enemies/hexagone.png")
        self.speed = 0.5
        self.original_speed = self.speed
        self.health = 50

#-------------------------------------------------------------------------------------------------------------------------------------------#

class Fleche(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Assets/Enemies/fleche.png")
        self.speed = 3
        self.original_speed = self.speed
        self.health = 10
        self.buff_radius = 100
        self.buff_speed_factor = 1.5

    def update(self):
        super().update()
        self.buff_nearby_enemies()

    def buff_nearby_enemies(self):
        for enemy in self.groups()[0]:
            if enemy != self and self.distance_to(enemy) <= self.buff_radius:
                enemy.speed *= self.buff_speed_factor

    def distance_to(self, other):
        dx = self.rect.x - other.rect.x
        dy = self.rect.y - other.rect.y
        return math.hypot(dx, dy)

#-------------------------------------------------------------------------------------------------------------------------------------------#

class Coeur(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, "Assets/Enemies/coeur.png")
        self.speed = 2
        self.original_speed = self.speed
        self.health = 10
        self.heal_radius = 100
        self.heal_amount = 2

    def update(self):
        super().update()
        self.heal_nearby_enemies()

    def heal_nearby_enemies(self):
        for enemy in self.groups()[0]:
            if enemy != self and self.distance_to(enemy) <= self.heal_radius:
                enemy.health += self.heal_amount

    def distance_to(self, other):
        dx = self.rect.x - other.rect.x
        dy = self.rect.y - other.rect.y
        return math.hypot(dx, dy)

