import pygame
import math
import time
from groups import*
from path_assets import *

class TowerDefense(pygame.sprite.Sprite):
    def __init__(self, x, y, image,size):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image), size)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.target = None
        self.range = 0
        self.show_range = True
        self.range_offset = self.rect.width / 2
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def set_target(self, enemies):
        closest_distance = float("inf") 
        for enemy in enemies:
            speed = ((self.x - enemy.rect.x) ** 2 + (self.y - enemy.rect.y) ** 2) ** 0.5
            if speed < closest_distance:
                closest_distance = speed
                self.target = enemy

    def in_range(self, enemy):
        def point_in_circle(x, y, circle_x, circle_y, radius):
            return (x - circle_x) ** 2 + (y - circle_y) ** 2 <= radius ** 2

        circle_x, circle_y = self.rect.centerx, self.rect.centery
        radius = self.range

        # Vérifier si l'un des coins du rectangle de l'ennemi est à l'intérieur du cercle
        in_range = (
            point_in_circle(enemy.rect.left, enemy.rect.top, circle_x, circle_y, radius) or
            point_in_circle(enemy.rect.right, enemy.rect.top, circle_x, circle_y, radius) or
            point_in_circle(enemy.rect.left, enemy.rect.bottom, circle_x, circle_y, radius) or
            point_in_circle(enemy.rect.right, enemy.rect.bottom, circle_x, circle_y, radius)
        )

        return in_range


    def sell(self, refund_rate=0.75):
        self.kill()
        return int(self.cost * refund_rate), self.original_pos
    
    def update(self, enemy_group):
        pass
    
    def toggle_range(self):
        self.show_range = not self.show_range


class SquareTower(TowerDefense, pygame.sprite.Sprite):
    def __init__(self, x, y,size):
        pygame.sprite.Sprite.__init__(self)  
        TowerDefense.__init__(self, x, y,path_assets+'/towers/square_tower.png',size)
        self.original_pos = (x,y)
        self.cooldown = 3
        self.cost = 20
        self.range = 200
        self.slowing_factor = 0.6
        self.range_rect = pygame.Rect((self.x +((self.rect.width - self.range)  / 2), self.y + ((self.rect.height - self.range) / 2 ), self.range, self.range))
        self.last_attack_time = 0
        self.stun_duration = 1





    def in_range(self,enemy) : 
        return enemy.rect.colliderect(self.range_rect)


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
        if self.show_range:
            gap_x = (self.rect.width - self.range)  / 2
            gap_y = (self.rect.height - self.range) / 2
            coord_x = self.x + gap_x
            coord_y = self.y + gap_y 

            pygame.draw.rect(screen, (0, 255, 255), (coord_x,coord_y, self.range, self.range),width=5)

    def  animation(self, screen):
        gap_x = (self.rect.width - self.range)  / 2
        gap_y = (self.rect.height - self.range) / 2
        coord_x = self.x + gap_x
        coord_y = self.y + gap_y 

        pygame.draw.rect(screen, (255, 0, 0), (coord_x,coord_y, self.range, self.range),width=5)
            
    def stun (self,enemy_group,screen):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_attack_time
        if elapsed_time >= self.cooldown * 1000:
            for enemy in enemy_group :
                if self.in_range(enemy):
                    if enemy.stun == 0:
                        enemy.when_stunned = pygame.time.get_ticks()
                    enemy.stun += self.stun_duration 
                    self.last_attack_time = pygame.time.get_ticks()
                    self.animation(screen)
        



    def update(self, enemy_group,screen):
        self.stun(enemy_group,screen)
        self.slow_enemies_in_range(enemy_group)
        

class RoundTower(TowerDefense, pygame.sprite.Sprite):
    def __init__(self, x, y,size):
        pygame.sprite.Sprite.__init__(self)  
        TowerDefense.__init__(self, x, y,path_assets+'/towers/circle_tower.png',size)
        self.original_pos = (x,y)
        self.cooldown = 2
        self.last_attack_time = 0
        self.damage = 20
        self.cost = 30
        self.range = 100



    def attack_animation(self, screen_to_blit):
        center_x = self.rect.x + self.rect.width // 2
        center_y = self.rect.y + self.rect.height // 2
        pygame.draw.circle(screen_to_blit, (255, 0, 0), (center_x, center_y), self.range, 5)

    def attack(self, enemy_group, screen):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_attack_time
        if elapsed_time >= self.cooldown * 1000:
            for enemy in enemy_group:
                if self.in_range(enemy):
                    enemy.take_damage(self.damage)
                    elapsed_time = 0
                    self.last_attack_time = pygame.time.get_ticks()
                    self.attack_animation(screen)




    def update(self, enemy_group, screen):
        self.attack(enemy_group, screen)
        
    def draw_range(self, screen):
        if self.show_range:
            center_x = self.rect.x + self.rect.width // 2
            center_y = self.rect.y + self.rect.height // 2
            pygame.draw.circle(screen, (0, 255, 0), (center_x, center_y), self.range, width=5)
            
class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target, damage, image):
        super().__init__()
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.has_hit = False

    def update(self):
        if not self.target.is_dead():
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            distance = math.sqrt(dx * dx + dy * dy)
            self.rect.x += (dx / distance) * self.speed
            self.rect.y += (dy / distance) * self.speed

            if self.rect.colliderect(self.target.rect):
                self.target.take_damage(self.damage)
                self.has_hit = True
        else:
            self.has_hit = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class TriangleTower(TowerDefense, pygame.sprite.Sprite):
    def __init__(self, x, y,size):
        pygame.sprite.Sprite.__init__(self)
        TowerDefense.__init__(self, x, y,path_assets+'/towers/triangle_tower.png',size)
        self.original_image = self.image 
        self.original_pos = (x, y)
        self.cooldown = 0.5
        self.last_attack_time = 0
        self.damage = 10
        self.cost = 40
        self.projectiles = []
        self.range = 150



    def point_to_enemy(self):
        if self.target:
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            angle = math.degrees(math.atan2(dy, dx))
            self.image = pygame.transform.rotate(self.original_image, -angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self):
        if self.target and not self.target.is_dead():
            self.projectiles.append(Projectile(self.rect.centerx, self.rect.centery, self.target, self.damage, path_assets+'/Projectiles/small_bullet.png'))

    def attack(self, enemy_group, screen):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_attack_time

        if elapsed_time >= self.cooldown * 1000:
            self.set_target(enemy_group)
            if self.target and self.in_range(self.target):
                self.point_to_enemy()
                self.shoot()
                self.last_attack_time = pygame.time.get_ticks()

    def update(self, enemy_group, screen):
        self.attack(enemy_group, screen)
        for projectile in self.projectiles:
            projectile.update()
            if projectile.has_hit:
                self.projectiles.remove(projectile)

    def draw_projectiles(self, screen):
        for projectile in self.projectiles:
            projectile.draw(screen)

    def draw_range(self, screen):
        if self.show_range:
            center_x = self.rect.x + self.rect.width // 2
            center_y = self.rect.y + self.rect.height // 2
            pygame.draw.circle(screen, (255, 165, 0), (center_x, center_y), self.range, width=5)


class TrapezeTower(TriangleTower):
    def __init__(self, x, y,size):
        super().__init__(x, y,size)
        self.image = pygame.transform.scale(pygame.image.load(path_assets+'/towers/trapeze_tower.png'), size)
        self.original_image = self.image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.cooldown = 3
        self.damage = 50
        self.cost = 50
        self.range = 200


    def shoot(self):
        if self.target and not self.target.is_dead():
            self.projectiles.append(ExplosiveProjectile(self.rect.centerx, self.rect.centery, self.target, self.damage, path_assets+'/Projectiles/big_bullet.png'))

    def attack(self, enemy_group, screen):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.last_attack_time

        if elapsed_time >= self.cooldown * 1000:
            self.set_target(enemy_group)
            if self.target and self.in_range(self.target):
                self.point_to_enemy()
                self.shoot()
                self.last_attack_time = pygame.time.get_ticks()
                
    def draw_range(self, screen):
        if self.show_range:
            center_x = self.rect.x + self.rect.width // 2
            center_y = self.rect.y + self.rect.height // 2
            pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), self.range, width=5)



class ExplosiveProjectile(Projectile):
    def __init__(self, x, y, target, damage, image):
        super().__init__(x, y, target, damage, image)
        self.explosion_radius = 50

    def update(self):
        if not self.target.is_dead():
            dx = self.target.rect.centerx - self.rect.centerx
            dy = self.target.rect.centery - self.rect.centery
            distance = math.sqrt(dx * dx + dy * dy)
            self.rect.x += (dx / distance) * self.speed
            self.rect.y += (dy / distance) * self.speed

            if self.rect.colliderect(self.target.rect):
                self.explode()
                self.has_hit = True
        else:
            self.has_hit = True

    def explode(self):
        for enemy in enemy_group:
            dx = self.rect.centerx - enemy.rect.centerx
            dy = self.rect.centery - enemy.rect.centery
            distance = math.sqrt(dx * dx + dy * dy)

            if distance <= self.explosion_radius:
                enemy.take_damage(self.damage)