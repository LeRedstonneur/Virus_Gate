import pygame
from groups import*

class Base(pygame.sprite.Sprite):
    def __init__(self, x, y,width,height,index):
        super().__init__()
        self.ratio = (index[0],index[1])
        self.dimensions = (width,height)
        self.x= x
        self.y= y
        self.rect = pygame.Rect(x,y,width,height)
        self.choice = False
        self.tower_rect = []
        self.tower = None
    
    def add_tower(self, tower):
        if not self.tower:
            self.tower = tower
            tower_group.add(self.tower)
            
    def remove_tower(self, base_group):
        base_group.add(self.base_sprite)

    def remove(self):
        del self

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
        try :
            self.tower_rect[0]=(pygame.Rect(coord_twr[0],coord_twr[1],dimensions_twr[0],dimensions_twr[1]))
        except IndexError :
            self.tower_rect.append(pygame.Rect(coord_twr[0],coord_twr[1],dimensions_twr[0],dimensions_twr[1]))
        

    def update(self,mouse_pos):
        for rect in self.tower_rect :
            if rect.collidepoint(mouse_pos): 
                print("square")
                
        if self.rect.collidepoint(mouse_pos):
            self.choice = True  
        else : 
            self.choice = False
            self.tower_rect = []