import pygame
import math
import time



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

    def set_target(self, enemies):
        closest_distance = float("inf") 
        for enemy in enemies:
            speed = ((self.x - enemy.rect.x) ** 2 + (self.y - enemy.rect.y) ** 2) ** 0.5
            if speed < closest_distance:
                closest_distance = speed
                self.target = enemy

    def in_range(self, enemy):
        dx = self.rect.centerx - enemy.rect.centerx
        dy = self.rect.centery - enemy.rect.centery
        distance = math.sqrt(dx*dx + dy*dy) + self.range_offset  # addition du range_offset
        return distance <= self.range


    def sell(self):
        #money += price*70/100
        del self


class SquareTower(TowerDefense):
    def __init__(self, x, y, image, level):
        TowerDefense.__init__(self, x, y, image)
        self.level = level
        self.cooldown = 1
        self.last_attack_time = 0  # temps de la dernière attaque en secondes
        self.update_stats()
        self.damage = 2

    def update_stats(self):
        self.range = 200 + (10 * self.level)
        self.slowing_factor = self.level * 0.1

    def slow(self, factor):
        if self.target:
            self.target.slow(factor)

    def attack_animation(self,screen_to_blit):

        reduction = (self.range - 100) / 2
        pygame.draw.rect(screen_to_blit,(255, 0, 0), (self.x-int(reduction), self.y-int(reduction), self.range, self.range),width=5)
        
    def attack(self, enemy, screen):
        current_time = time.time()  
        elapsed_time = current_time - self.last_attack_time  
        if elapsed_time >= self.cooldown:  # si le temps écoulé est supérieur ou égal au temps de recharge
            if self.in_range(enemy):
                enemy.health -= self.damage
                elapsed_time = 0
                self.last_attack_time = time.time()  # mettre à jour le temps de la dernière attaque
                self.attack_animation(screen)
                print('attaque')
                
                return True  # l'attaque a réussi
        return False  # l'attaque n'a pas pu être effectuée (cooldown en cours)
    
    def draw_range(self, screen):
        if self.mouse_down:
            reduction = (self.range - 100) / 2
            pygame.draw.rect(screen, (0, 255, 255), (self.x-int(reduction), self.y-int(reduction), self.range, self.range),width=5)
    
    
    


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
        self.speed = 1
        self.has_traversed = False 
        self.health = 5
        
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
        del self

    def draw(self, screen):
        screen.blit(self.image, self.rect)
    
    def get_pos(self):
        return self.x, self.y

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
        
 class Base():
    def __init__(self, x, y, image,width,height,index):
        self.ratio = (index[0],index[1])
        self.dimensions = (width,height)
        self.x= x
        self.y= y
        self.image= pygame.image.load(image)
        self.rect = pygame.Rect(x,y,width,height)
        self.choice = False
        self.tower_rect = []

    def remove(self):
        del self

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def resize(self,size) :
        self.dimensions = size
        width = size[0]
        height = size[1]
        self.x = width * self.ratio[0]
        self.y = height * self.ratio[1]
        self.rect = pygame.Rect(self.x,self.y,width,height)
        

    def chose(self,screen,tower_list):
        centre = (self.x+(self.dimensions[0]//2),self.y+(self.dimensions[1]//2))
        pygame.draw.circle(screen,(0,0,0),centre,self.dimensions[0],5)
        dimensions_twr =  (self.dimensions[0]//1.5,self.dimensions[1]//1.5)
        coord_twr = (centre[0]+self.dimensions[0]//2,centre[1]+self.dimensions[1]//2)
        screen.blit(pygame.transform.scale(tower_list[0], dimensions_twr) , coord_twr)
        self.tower_rect.append(pygame.Rect(dimensions_twr[0],dimensions_twr[1],coord_twr[0],coord_twr[1]))

    def update(self,mouse_pos):
        for rect in self.tower_rect :
            if rect.collidepoint(mouse_pos): 
                print("square")
                
        if self.rect.collidepoint(mouse_pos):
            self.choice = True  
        else : 
            self.choice = False
            self.tower_rect = []

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
