import pygame
import math

class TowerDefense(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.target = None
        self.range = 0
        self.mouse_down = False
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_target(self, enemies):
        closest_distance = float("inf") 
        for enemy in enemies:
            speed = ((self.x - enemy.rect.x) ** 2 + (self.y - enemy.rect.y) ** 2) ** 0.5
            if speed < closest_distance:
                closest_distance = speed
                self.target = enemy

    def slow(self, factor):
        if self.target:
            self.target.slow(factor)
            
    def in_range(self, enemy):
        speed = ((self.x - enemy.rect.x) ** 2 + (self.y - enemy.rect.y) ** 2) ** 0.5
        return speed <= self.range

    def sell(self):
        #money += price*70/100
        del self
    
          

class SquareTower(TowerDefense):
    def __init__(self, x, y, image, level):
        TowerDefense.__init__(self, x, y, image)
        self.level = level
        self.update_stats()

    def update_stats(self):
        self.range = 100 + (10 * self.level)
        self.slowing_factor = self.level * 0.1

    def attack(self):
        if self.target:
            self.target.take_damage(2)
            self.slow(self.slowing_factor)
            self.target = None
    
    def draw_range(self, screen):
        if self.mouse_down:
            pygame.draw.rect(screen, (0, 255, 255), (self.x-5, self.y-5, 110, 110))
            
class RoundTower(TowerDefense):
    def __init__(self, x, y, image, level):
        TowerDefense.__init__(self, x, y, image)
        self.level = level
        self.update_stats()

    def update_stats(self):
        self.range = 150 + (10 * self.level)
        self.damage = 10 + (5 * self.level)

    def attack(self):
        if self.target:
            self.target.take_damage(self.damage)
            if self.target.is_dead():
                self.target = None

        


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
        self.speed = 10
        self.has_traversed = False 
        
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
                self.has_traversed = True
                # on est arrivé au dernier checkpoint, on peut supprimer l'ennemi
                del self
                
            else:
                self.destination = self.path[self.current_checkpoint]

    def take_damage(self, damage):
        self.health -= damage
    
    def is_slowed(self, slow_factor):
        self.speed *= (1 - slow_factor)

    def is_dead(self):
        return self.health <= 0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Base():
    def __init__(self, x, y, image):
        self.x=x
        self.y=y
        self.image= pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def remove(self):
        del self

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Upgrade:
    def __init__(self):
        self.level = 1
        self.costs = {1: 100, 2: 200, 3: 300} 

    def upgrade_level(self, tower):
        if self.level < 3:
            current_level = tower.level
            next_level = current_level + 1
            cost = self.costs[next_level]
            if score >= cost:
                tower.level = next_level
                tower.update_stats()
                score -= cost
                print(f"Tour mis à niveau au niveau {next_level} pour {cost} or")
            else:
                print(f"Vous n'avez pas assez de points pour mettre à niveau la tour. Il vous manque {cost - score} or.")
        else:
            print("La tour est déjà au niveau maximum.")
