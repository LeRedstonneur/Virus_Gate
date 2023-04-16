import pygame
from  class_Base import Base
from path_assets import *

pygame.display.set_caption("Neon TD : BEST GAME OF 2004")
# Obtient le répertoire de travail actuel et le concaténe  avec un string pour obtener le chemin d'accés au assets


dico_tiles={
    "B000" :pygame.image.load(path_assets+"/tiles/base.png"),
    "S0vE" :pygame.image.load(path_assets+"/tiles/mob_spawners/mobSpawner_east.png"),
    "S0vN" :pygame.image.load(path_assets+"/tiles/mob_spawners/mobSpawner_north.png"),
    "S0vW" :pygame.image.load(path_assets+"/tiles/mob_spawners/mobSpawner_west.png"),
    "S0vS" :pygame.image.load(path_assets+"/tiles/mob_spawners/mobSpawner_south.png"),
    "PEvW" :pygame.image.load(path_assets+"/tiles/paths/path_east_west.png"),
    "PWvE" :pygame.image.load(path_assets+"/tiles/paths/path_west_east.png"),
    "PNvS" :pygame.image.load(path_assets+"/tiles/paths/path_north_south.png"),
    "PSvN" :pygame.image.load(path_assets+"/tiles/paths/path_south_north.png"),
    "C0vE" :pygame.image.load(path_assets+"/tiles/cores/core_east.png"),
    "C0vN" :pygame.image.load(path_assets+"/tiles/cores/core_north.png"),
    "C0vW" :pygame.image.load(path_assets+"/tiles/cores/core_west.png"),
    "C0vS" :pygame.image.load(path_assets+"/tiles/cores/core_south.png"),
    "AWvN" :pygame.image.load(path_assets+"/tiles/angles/angle_west_north.png"),
    "AWvS" :pygame.image.load(path_assets+"/tiles/angles/angle_west_south.png"),
    "AEvS" :pygame.image.load(path_assets+"/tiles/angles/angle_east_south.png"),
    "AEvN" :pygame.image.load(path_assets+"/tiles/angles/angle_east_north.png"),
    "ASvE" :pygame.image.load(path_assets+"/tiles/angles/angle_south_east.png"),
    "ASvW" :pygame.image.load(path_assets+"/tiles/angles/angle_south_west.png"),
    "ANvE" :pygame.image.load(path_assets+"/tiles/angles/angle_north_east.png"),
    "ANvW" :pygame.image.load(path_assets+"/tiles/angles/angle_north_west.png")
}

square   = pygame.image.load (path_assets+"/towers/square_tower.png")
circle   = pygame.image.load (path_assets+"/towers/circle_tower.png")
triangle = pygame.image.load (path_assets+"/towers/triangle_tower.png")
trapeze  = pygame.image.load (path_assets+"/towers/trapeze_tower.png") 


class EmptyFile(Exception):
    pass

def read(fichier):
    with open(fichier, "r") as f:
        contenu = f.read()
    if contenu=="" :
        raise EmptyFile("File was found to be empty")
    else :
        return contenu

def next(content: str,index: int,lenght: int) -> tuple:
    """Donne l'élement suivant et son index pour un index donnée dans une chaine de caractères"""
    s = ""
    if content[index]=="\n":
        return "\n",index+1
    else :
        while index<lenght and content[index]!="-" :
            s += content[index]
            index += 1
        return s,index

def generate_map(content) -> list:
    """crée une matrice composé des codes de chaque tuiles"""
    matrice = []
    liste =[]
    lenght = len(content)
    index = 1
    while index < lenght:
        id,index=next(content,index,lenght)
        index+=1
        if id == "\n" :
            matrice.append(liste)
            liste=[]
        else :
            liste.append(id)
    matrice.append(liste)
    return matrice

def generate_bases(matrice,size) :
    """retourne la liste des bases"""
    bases = []
    y = 0
    for list_index,ligne in enumerate(matrice) :
        x = 0
        for ele_index,id in enumerate(ligne) :
            if id == "B000":
                bases.append(Base(x,y,size[0],size[1],(ele_index,list_index)))
            x += size[0]
        y += size[1]
    return bases

def print_map(screen,matrice,size):
    y = 0
    for ligne in matrice :
        x = 0
        for id in ligne :
            if id != "0000":
                screen.blit(pygame.transform.scale(dico_tiles[id], size),(x,y))
            x += size[0]
        y += size[1]


def affiche(b) :
    print(f"x : {b.x}")
    print(f"y : {b.y}")
    print(f"x rect :{b.rect.x}")
    print(f"y rect :{b.rect.y}")
    print(f"dim : {b.dimensions}")
    print(f"choice : {b.choice}")
    print(b.ratio)
    print("------")

def max_line(content):
    max_len = 0
    current_len = 0
    coulumn = 1
    lenght = len(content)
    index = 1
    while index < lenght:
        id,index=next(content,index,lenght)
        index+=1
        if id == "\n":
            if current_len > max_len:
                max_len = current_len
            coulumn += 1
            current_len = 0
        else:
            current_len += 1
    if current_len > max_len:
        max_len = current_len
    return max_len, coulumn