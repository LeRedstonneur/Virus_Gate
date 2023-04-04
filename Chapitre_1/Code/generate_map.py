import pygame

width,height = 600,500
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

dico_map={
    "B000" :pygame.image.load("./map/base.png"),
    "S0vE" :pygame.image.load("./map/spawnMob_east.png"),
    "S0vN" :pygame.image.load("./map/spawnMob_north.png"),
    "S0vW" :pygame.image.load("./map/spawnMob_west.png"),
    "S0vS" :pygame.image.load("./map/spawnMob_south.png"),
    "PEvW" :pygame.image.load("./map/path_east_west.png"),
    "PWvE" :pygame.image.load("./map/path_west_east.png"),
    "PNvS" :pygame.image.load("./map/path_north_south.png"),
    "PSvN" :pygame.image.load("./map/path_south_north.png"),
    "C0vE" :pygame.image.load("./map/core_east.png"),
    "C0vN" :pygame.image.load("./map/core_north.png"),
    "C0vW" :pygame.image.load("./map/core_west.png"),
    "C0vS" :pygame.image.load("./map/core_south.png"),
    "AWvN" :pygame.image.load("./map/angle_west_north.png"),
    "AWvS" :pygame.image.load("./map/angle_west_south.png"),
    "AEvS" :pygame.image.load("./map/angle_east_south.png"),
    "AEvN" :pygame.image.load("./map/angle_east_north.png"),
    "ASvE" :pygame.image.load("./map/angle_south_east.png"),
    "ASvW" :pygame.image.load("./map/angle_south_west.png"),
    "ANvE" :pygame.image.load("./map/angle_north_east.png"),
    "ANvW" :pygame.image.load("./map/angle_north_west.png")
}

class EmptyFile(Exception):
    pass

def read(fichier):
    with open(fichier, "r") as f:
        contenu = f.read()
    if contenu=="" :
        raise EmptyFile("File was found to be empty")
    else :
        return contenu

def generate_map(content,size):
    x = 0
    y = 0
    lenght = len(content)
    index = 1
    while index < lenght:
        id,index=next(content,index,lenght)
        index+=1
        if id == "\n" :
            y += size[1]
            x = 0
        elif id == "0000" :
            x+=size[0]
        else :
            screen.blit(pygame.transform.scale(dico_map[id], size),(x,y))
            x += size[0]
    

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
    

def next(content,index,lenght):
    str=""
    if content[index]=="\n":
        return "\n",index+1
    else :
        while index<lenght and content[index]!="-" :
            str+=content[index]
            index+=1
        return str,index


try :
    content=read("./map/map.txt")
    value = True
    max = max_line(content)

except EmptyFile :
    print("File was found to be empty")
    value = False

except FileNotFoundError :
    print("File not found")
    value = False


while value :
    generate_map(content,(width//max[0],height//max[1]))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            pygame.display.set_caption("Resizable Window: {} x {}".format(width, height))
    pygame.display.flip()