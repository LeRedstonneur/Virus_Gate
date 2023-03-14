import pygame

class EmptyFile(Exception):
    pass

def read(fichier):
    with open(fichier, "r") as f:
        contenu = f.read()
    if contenu=="" :
        raise EmptyFile("File was found to be empty")
    else :
        return contenu


def generate_map(fichier):
    start = pygame.image.load("start.png")
    end = pygame.image.load("end.png")
    path = pygame.image.load("path.png")
    try :
        fd=read(fichier)
    except EmptyFile :
        print("File was found to be empty")
        return False
    except FileNotFoundError :
        print("File not found")
        return False
    x,y=200,200
    for char in fd :
        if char=="\n" :
            print("return à la ligne")
            y+=100
        elif char =="!" :
            print("start")
            screen.blit(start, (x, y))

        elif char =="?" :
            print("End")
            screen.blit(end, (x, y))


        elif char =="#" :
            print("void")

        elif char =="=" :
            print("path")
            screen.blit(path, (x, y))
        x+=100


valeur=True
while True:
    if valeur :
        generate_map("map")
        valeur=False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.flip()