import pygame
import math
import time
import random 
import Chapitre_1.Code.groups as groups
import Chapitre_1.Code.path_assets as path_assets

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tempx = float(x)
        self.tempy = float(y)
        self.path = [(1042, 160), (1160, 160), (1160, 320), (1094, 320), (1094, 480), (1160, 480), (1160, 720), (1094, 720), (1094, 800), (972, 800), (972, 560), (708, 560), (706, 880), (566, 880), (566, 320), (632, 320), (632, 400), (962, 400), (962, 240), (698, 240), (698, 160)]
        self.current_checkpoint = 0
        self.destination = self.path[self.current_checkpoint]
        self.has_traversed = False 
        self.slowed_by = []
        self.slowing_towers = []
        self.stun = False
        self.when_stunned = 0
    
    def is_dead(self):
        if self.health <= 0:
            if self.groups():
                self.groups()[0].remove(self)
            return True
        return False
    
    def update(self):
        if self.speed < 0:
            self.speed = self.original_speed
        self.is_dead()
        # calculer la distance et la direction vers la destination actuelle
        if  self.stun == 0 :
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
        elif pygame.time.get_ticks() - self.when_stunned >= self.stun * 1000:
            self.stun = 0

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
        if not isinstance(self,Hexagone):       
            if not isinstance(self, Losange):
                self.speed = self.original_speed
                for tower in self.slowing_towers:
                    if not tower.in_range(self):
                        self.slowing_towers.remove(tower)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

        # Ajout de la barre de vie
        health_bar_width = 30
        health_bar_height = 5
        health_bar_x = self.rect.x + (self.rect.width / 2) - (health_bar_width / 2)
        health_bar_y = self.rect.y - health_bar_height - 5

        # Barre de vie rouge (vie manquante)
        missing_health_bar = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        pygame.draw.rect(screen, (255, 0, 0), missing_health_bar)

        # Barre de vie verte (vie actuelle)
        health_percentage = self.health / self.max_health
        current_health_width = health_bar_width * health_percentage
        current_health_bar = pygame.Rect(health_bar_x, health_bar_y, current_health_width, health_bar_height)
        pygame.draw.rect(screen, (0, 255, 0), current_health_bar)
    
    def get_pos(self):
        return self.x, self.y

#-------------------------------------------------------------------------------------------------------------------------------------------#

class Croix(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, path_assets.path_assets+"/Enemies/croix.png")
        self.speed = 3
        self.original_speed = 3
        self.health = 50
        self.max_health = 50
        self.value = 1

#-------------------------------------------------------------------------------------------------------------------------------------------#

class GrandeCroix(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, path_assets.path_assets+"/Enemies/grande_croix.png")
        self.speed = 1
        self.original_speed = 1
        self.health = 200
        self.max_health = 200
        self.last_spawn_time = time.time()  # enregistrer l'heure actuelle
        self.spawn_interval = 5  # intervalle de spawn de 10 secondes
        self.value = 5

    def update(self):
        super().update()
        self.check_spawn_croix(groups.enemy_group)  # vérifier si une nouvelle instance doit être créée

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
        super().__init__(x, y, path_assets.path_assets+"/Enemies/losange2.png")
        self.speed = 1
        self.original_speed = 1
        self.health = 60
        self.max_health = 60
        self.speed_increase_rate = 0.02
        self.value = 1

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
        super().__init__(x, y, path_assets.path_assets+"/Enemies/rectangle.png")
        self.speed = 1
        self.original_speed = self.speed
        self.health = 100
        self.max_health = 100
        self.value = 5

        # Ajout du bouclier
        self.shield_health = 200
        self.shield_max_health = 200
        self.shield_radius = 25
        self.shield_image = pygame.transform.scale(pygame.image.load(path_assets.path_assets+"/Enemies/shield.png"), (self.shield_radius * 3, self.shield_radius * 3))
        self.shield_broken = False

    def update(self):
        super().update()

        # Mettre à jour le bouclier
        if self.shield_health <= 0 and not self.shield_broken:
            self.shield_health = 0
            self.shield_broken = True

    def draw_shield_health_bar(self, screen):
        health_bar_width = 30
        health_bar_height = 5
        health_bar_x = self.rect.x + (self.rect.width / 2) - (health_bar_width / 2)
        health_bar_y = self.rect.y - health_bar_height - 15

        # Barre de vie rouge (vie manquante)
        missing_health_bar = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        pygame.draw.rect(screen, (255, 255, 255), missing_health_bar)

        # Barre de vie verte (vie actuelle)
        health_percentage = self.shield_health / self.shield_max_health
        current_health_width = health_bar_width * health_percentage
        current_health_bar = pygame.Rect(health_bar_x, health_bar_y, current_health_width, health_bar_height)
        pygame.draw.rect(screen, (0, 0, 255), current_health_bar)

    def draw(self, screen):
        # Dessiner le Rectangle
        super().draw(screen)

        # Dessiner le bouclier et sa barre de vie s'il a des points de vie et n'est pas cassé
        if not self.shield_broken:
            shield_rect = self.shield_image.get_rect()
            shield_rect.center = self.rect.center
            screen.blit(self.shield_image, shield_rect)
            self.draw_shield_health_bar(screen)

    def take_damage(self, damage):
        # Appliquer les dégâts au bouclier s'il a des points de vie
        if self.shield_health > 0:
            self.shield_health -= damage
            if self.shield_health < 0:
                self.shield_broken = True
                damage = abs(self.shield_health)
                self.shield_health = 0
            else:
                damage = 0
        if self.shield_broken:
            self.health -= damage
    







#-------------------------------------------------------------------------------------------------------------------------------------------#

class Hexagone(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, path_assets.path_assets+"/Enemies/hexagone.png")
        self.image = pygame.transform.scale(self.image, (self.rect.width * 1.5, self.rect.height * 1.5))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 0.5
        self.original_speed = self.speed
        self.health = 700
        self.max_health = 700
        self.value = 50
        self.buff_radius = 100
        self.heal_amount = 20
        self.last_heal_time = 0
        self.heal_interval = 1000 
        self.buff_speed_factor = 1.5
        self.buffed_enemies = []
        self.shield_health = 300
        self.shield_max_health = 300
        self.shield_radius = 25
        self.shield_image = pygame.transform.scale(pygame.image.load(path_assets.path_assets+"/Enemies/shield.png"), (self.shield_radius * 3, self.shield_radius * 3))
        self.shield_broken = False
        self.speed_increase_rate = 0.002
        self.last_spawn_time = time.time()  # enregistrer l'heure actuelle
        self.spawn_interval = 6

    def update(self):
        super().update()
        self.buff_nearby_enemies()
        self.remove_buff_from_out_of_range_enemies()
        self.heal_nearby_enemies()
        self.increase_speed()
        self.check_spawn_croix(groups.enemy_group)
        # Mettre à jour le bouclier
        if self.shield_health <= 0 and not self.shield_broken:
            self.shield_health = 0
            self.shield_broken = True

    def heal_nearby_enemies(self):
        now = pygame.time.get_ticks()
        if now - self.last_heal_time >= self.heal_interval:
            try :
                for enemy in self.groups()[0]:
                    if not isinstance(enemy, Hexagone) and not isinstance(enemy, Coeur) and self.distance_to(enemy) <= self.buff_radius:
                        enemy.health = min(enemy.health + self.heal_amount, enemy.max_health)
                self.last_heal_time = now
            except IndexError :
                pass 
 
    def buff_nearby_enemies(self):
        try :
            for enemy in self.groups()[0]:
                if not isinstance(enemy, Hexagone) and not isinstance(enemy, Fleche) and self.distance_to(enemy) <= self.buff_radius:
                    if enemy not in self.buffed_enemies:
                        enemy.speed += self.buff_speed_factor
                        self.buffed_enemies.append(enemy)
                elif enemy in self.buffed_enemies and self.distance_to(enemy) > self.buff_radius:
                    enemy.speed -= self.buff_speed_factor
                    self.buffed_enemies.remove(enemy)
        except IndexError :
            pass

    def remove_buff_from_out_of_range_enemies(self):
        for enemy in self.buffed_enemies:
            if self.distance_to(enemy) > self.buff_radius:
                enemy.speed = enemy.original_speed
                self.buffed_enemies.remove(enemy)

    def distance_to(self, other):
        dx = self.rect.x - other.rect.x
        dy = self.rect.y - other.rect.y
        return math.hypot(dx, dy)
    
    def draw_shield_health_bar(self, screen):
        health_bar_width = 30
        health_bar_height = 5
        health_bar_x = self.rect.x + (self.rect.width / 2) - (health_bar_width / 2)
        health_bar_y = self.rect.y - health_bar_height - 15

        # Barre de vie rouge (vie manquante)
        missing_health_bar = pygame.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height)
        pygame.draw.rect(screen, (255, 255, 255), missing_health_bar)

        # Barre de vie verte (vie actuelle)
        health_percentage = self.shield_health / self.shield_max_health
        current_health_width = health_bar_width * health_percentage
        current_health_bar = pygame.Rect(health_bar_x, health_bar_y, current_health_width, health_bar_height)
        pygame.draw.rect(screen, (0, 0, 255), current_health_bar)

    def take_damage(self, damage):
        # Appliquer les dégâts au bouclier s'il a des points de vie
        if self.shield_health > 0:
            self.shield_health -= damage
            if self.shield_health < 0:
                self.shield_broken = True
                damage = abs(self.shield_health)
                self.shield_health = 0
            else:
                damage = 0
        if self.shield_broken:
            self.health -= damage

    def draw(self, screen):
        # Dessiner le Rectangle
        super().draw(screen)

        # Dessiner le bouclier et sa barre de vie s'il a des points de vie et n'est pas cassé
        if not self.shield_broken:
            shield_rect = self.shield_image.get_rect()
            shield_rect.center = self.rect.center
            screen.blit(self.shield_image, shield_rect)
            self.draw_shield_health_bar(screen)


    def increase_speed(self):
        if self.speed < 2:  # vitesse maximale super rapide
            self.speed += self.speed_increase_rate
        else:
            self.speed = 2

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

class Fleche(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, path_assets.path_assets+"/Enemies/arrow.png")
        self.speed = 2
        self.original_speed = self.speed
        self.health = 100
        self.max_health = 100
        self.buff_radius = 100
        self.buff_speed_factor = 1.5
        self.buffed_enemies = []
        self.value = 5

    def update(self):
        super().update()
        self.buff_nearby_enemies()
        self.remove_buff_from_out_of_range_enemies()

    def buff_nearby_enemies(self):
        try :
            for enemy in self.groups()[0]:
                if not isinstance(enemy, Hexagone) :
                    if not isinstance(enemy, Fleche) and self.distance_to(enemy) <= self.buff_radius:
                        if enemy not in self.buffed_enemies:
                            enemy.speed += self.buff_speed_factor
                            self.buffed_enemies.append(enemy)
                    elif enemy in self.buffed_enemies and self.distance_to(enemy) > self.buff_radius:
                        enemy.speed -= self.buff_speed_factor
                        self.buffed_enemies.remove(enemy)
        except IndexError :
            pass

    def remove_buff_from_out_of_range_enemies(self):
        for enemy in self.buffed_enemies:
            if self.distance_to(enemy) > self.buff_radius:
                enemy.speed = enemy.original_speed
                self.buffed_enemies.remove(enemy)

    def distance_to(self, other):
        dx = self.rect.x - other.rect.x
        dy = self.rect.y - other.rect.y
        return math.hypot(dx, dy)

#-------------------------------------------------------------------------------------------------------------------------------------------#
class Coeur(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, path_assets.path_assets+"/Enemies/coeur.png")
        self.speed = 2
        self.original_speed = self.speed
        self.health = 100
        self.max_health = 100
        self.heal_radius = 100
        self.heal_amount = 20
        self.last_heal_time = 0
        self.heal_interval = 1000  # Temps en millisecondes entre les soins
        self.value = 5

    def update(self):
        super().update()
        self.heal_nearby_enemies()

    def heal_nearby_enemies(self):
        now = pygame.time.get_ticks()
        if now - self.last_heal_time >= self.heal_interval:
            try :
                for enemy in self.groups()[0]:
                    if not isinstance(enemy, Coeur) and self.distance_to(enemy) <= self.heal_radius:
                        enemy.health = min(enemy.health + self.heal_amount, enemy.max_health)
                self.last_heal_time = now
            except IndexError :
                pass

    def distance_to(self, other):
        dx = self.rect.x - other.rect.x
        dy = self.rect.y - other.rect.y
        return math.hypot(dx, dy)


enemy_classes = {
    "Croix" :  Croix,
    "GrandeCroix" : GrandeCroix,
    "Losange" :  Losange,
    "Rectangle" : Rectangle,
    "Fleche" : Fleche,
    "Hexagone" : Hexagone,
    "Coeur" : Coeur
}