import pygame
import math
import time
from groups import*

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
        self.range_offset = self.rect.width / 2
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_target(self, enemies): # pour les towers qui n'ont pas de degs de zone
        closest_distance = float("inf") 
        for enemy in enemies:
            speed = ((self.x - enemy.rect.x) ** 2 + (self.y - enemy.rect.y) ** 2) ** 0.5
            if speed < closest_distance:
                closest_distance = speed
                self.target = enemy

    def in_range(self, enemy): # pour les towers a deg de zone
        dx = self.rect.centerx - enemy.rect.centerx
        dy = self.rect.centery - enemy.rect.centery
        distance = math.sqrt(dx*dx + dy*dy) + self.range_offset  # addition du range_offset
        return distance <= self.range


    def sell(self):
        del self


class SquareTower(TowerDefense, pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)  
        TowerDefense.__init__(self, x, y, image)
        self.cooldown = 1
        self.level = 1
        self.update_stats()

    def update_stats(self):
        self.range = 200 + (10 * self.level)
        self.slowing_factor = self.level * 0.2

    def slow_enemies_in_range(self, enemy_group):
        for enemy in enemy_group:
            if self.in_range(enemy):
                enemy.slow(self.slowing_factor, self)
                if self not in enemy.slowed_by:
                    enemy.slowed_by.append(self)
            elif self in enemy.slowed_by:
                enemy.slowed_by.remove(self)
                enemy.reset_speed()

    def slow(self, enemy):
        enemy.slow(self.slowing_factor,self)
    
    def draw_range(self, screen):
        if self.mouse_down:
            reduction = (self.range - 100) / 2
            pygame.draw.rect(screen, (0, 255, 255), (self.x-int(reduction), self.y-int(reduction), self.range, self.range),width=5)
    
    def update(self, enemy_group):
        self.slow_enemies_in_range(enemy_group)


class RoundTower(TowerDefense, pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)  
        TowerDefense.__init__(self, x, y, image)
        self.cooldown = 1
        self.last_attack_time = 0
        self.damage = 2
        self.level = 1
        self.update_stats()

    def update_stats(self):
        self.range = 150 + (10 * self.level)
        self.damage = 10 + (5 * self.level)

    def attack_animation(self, screen_to_blit):
        reduction = (self.range - 100) / 2
        pygame.draw.rect(screen_to_blit, (255, 0, 0), (self.x-int(reduction), self.y-int(reduction), self.range, self.range), width=5)

    def attack(self, enemy_group, screen):
        current_time = time.time()
        elapsed_time = current_time - self.last_attack_time
        if elapsed_time >= self.cooldown:
            for enemy in enemy_group:
                if self.in_range(enemy):
                    enemy.health -= self.damage
                    if enemy.is_dead():
                        enemy_group.remove(enemy)
                    elapsed_time = 0
                    self.last_attack_time = time.time()
                    self.attack_animation(screen)


            return True

        return False

    def update(self, enemy_group, screen):
        self.attack(enemy_group, screen)
