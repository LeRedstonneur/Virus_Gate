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
        
        self.path = [(600, 50), (50, 50), (50, 600), (400, 600), (400, 300), (700, 300), (700, 700)]
        self.current_checkpoint = 0
        self.destination = self.path[self.current_checkpoint]
        self.speed = 2

    def update(self):
        # Calculer la distance entre l'ennemi et sa destination
        dx = self.destination[0] - self.rect.x
        dy = self.destination[1] - self.rect.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Si l'ennemi est arrivé à sa destination, choisir un nouveau checkpoint
        if distance < self.speed:
            self.current_checkpoint += 1
            if self.current_checkpoint >= len(self.path):
                self.kill()
                return
            self.destination = self.path[self.current_checkpoint]
            dx = self.destination[0] - self.rect.x
            dy = self.destination[1] - self.rect.y
            distance = math.sqrt(dx ** 2 + dy ** 2)

        # Calculer la direction et la distance de déplacement
        direction = (dx / distance, dy / distance)
        movement = (direction[0] * self.speed, direction[1] * self.speed)

        # Mettre à jour la position de l'ennemi
        self.rect.x += movement[0]
        self.rect.y += movement[1]




    def take_damage(self, damage):
        self.health -= damage
    
    def is_slowed(self, slow_factor):
        self.speed *= (1 - slow_factor)

    def is_dead(self):
        return self.health <= 0

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
