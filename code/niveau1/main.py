import pygame

def start():
    print("On ouvre la fenêtre")
    pygame.init()
    width = 800
    height = 600
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    bg = pygame.image.load("map.png")
    pygame.display.set_caption("Pygame Example")
    screen.fill((255, 255, 255))
    pygame.display.update()
    bg = pygame.transform.scale(bg, (1280, 720))
    rect = bg.get_rect()

    # Par défaut, le joueur est immobile
    mouvements = {"jump": False, "left": False, "right": False, "up": False, "down": False}

    posx = 0
    posy = 0
    speed = 2.5

    running = True
    while running:

        if mouvements["left"]:
            posx += speed
        if mouvements["right"]:
            posx -= speed
        if mouvements["up"]:
            posy += speed
        if mouvements["down"]:
            posy -= speed

        print(f"x = {posx}    y = {posy}")

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    mouvements["jump"] = True
                if event.key == pygame.K_LEFT:
                    mouvements["left"] = True
                if event.key == pygame.K_RIGHT:
                    mouvements["right"] = True
                if event.key == pygame.K_UP:
                    mouvements["up"] = True
                if event.key == pygame.K_DOWN:
                    mouvements["down"] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    mouvements["jump"] = False
                if event.key == pygame.K_LEFT:
                    mouvements["left"] = False
                if event.key == pygame.K_RIGHT:
                    mouvements["right"] = False
                if event.key == pygame.K_UP:
                    mouvements["up"] = False
                if event.key == pygame.K_DOWN:
                    mouvements["down"] = False

            if event.type == pygame.QUIT:
                running = False
                quit()
            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        #background_image = pygame.transform.scale(background_image, (width, height))
        #screen.blit(background_image, (0, 0))
        #screen.blit(bg, (0, 0))
        screen.fill((255, 255, 255))
        rect = rect.move(0, 0)
        screen.blit(bg, rect)

        pygame.draw.rect(screen, 'BLUE',(-posx,-posy,30,30))

        pygame.display.update()

def quit():
    print("On quitte le programme")
    pygame.quit()

start()

