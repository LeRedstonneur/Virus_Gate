import pygame

pygame.init()

# Obtenir la résolution d'écran
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h

# Définir les couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
BLUE_HACKER = (45, 53, 82)

# Définir la police et la taille de la police
font = pygame.font.Font(None, 36)

# Définir les dimensions et l'emplacement du premier bouton
button1_width = 300
button1_height = 100
button1_x = 50
button1_y = height / 1.3 - button1_height / 1.3

button1 = pygame.Surface((button1_width, button1_height))
button1.fill(BLUE_HACKER )
button1_text = font.render("Niveau 1", True, BLACK)
button1_text_rect = button1_text.get_rect(center=(button1_width / 2, button1_height / 2))
button1.blit(button1_text, button1_text_rect)

# Définir les dimensions et l'emplacement du second boutton
button2_width = 300
button2_height = 100
button2_x = 50
button2_y = width / 2 - button1_height / 2

button2 = pygame.Surface((button2_width, button2_height))
button2.fill(BLUE_HACKER )
button2_text = font.render("Niveau 2", True, BLACK)
button2_text_rect = button2_text.get_rect(center=(button2_width / 2, button2_height / 2))
button2.blit(button2_text, button2_text_rect)
in_options = False

# Définir les dimensions et l'emplacement du bouton option
options_width = 200
options_height = 70
options_x = 1700
options_y = height / 1.05 - options_height / 1.05

options = pygame.Surface((options_width, options_height))
options.fill(GRAY)
options_text = font.render("Options", True, BLACK)
options_text_rect = options_text.get_rect(center=(options_width / 2, options_height / 2))
options.blit(options_text, options_text_rect)
options_rect = options.get_rect(topleft=(options_x, options_y))

# Créer la fenêtre en mode plein écran
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

def afficher_menu():
    global in_options
    global background_image
    # Charger l'image de fond
    background_image = pygame.image.load("Fond d'ecran accueil.jpg")
    options_bg = pygame.image.load("Fond d'ecran accueil.jpg")
    screen.blit(options_bg, (0, 0))
    # Définir la police et la couleur du texte
    font = pygame.font.Font("freesansbold.ttf", 150)
    text = font.render("Virus Gate", True, (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.center = (width // 2, height // 9)  # Centrer le texte dans la fenêtre
    screen.blit(text, text_rect)

    # Afficher les boutons à gauche de l'écran      
    screen.blit(button1, (button1_x, button1_y))
    screen.blit(button2, (button2_x, button2_y))
    screen.blit(options, (options_x, options_y))

    options_rect = options.get_rect(topleft=(options_x, options_y))
    in_options = False
    pygame.display.flip()

def afficher_options():
    global in_options
    global return_rect
    print("afficher options")
    # Si l'utilisateur clique sur le bouton "Options", changez la valeur de "in_options" à True
    in_options = True
    # Si "in_options" est True, afficher les éléments que vous souhaitez afficher pour la page "Options"
    options_page = pygame.Surface((width, height))
    options_page.fill(WHITE)
    options_title = font.render("Options", True, BLACK)
    options_title_rect = options_title.get_rect(center=(width / 2, height / 2))
    options_page.blit(options_title, options_title_rect)
    return_button = pygame.Surface((options_width, options_height))
    return_button.fill(GRAY)
    return_text = font.render("Retour", True, BLACK)
    return_text_rect = return_text.get_rect(center=(options_width / 2, options_height / 2))
    return_button.blit(return_text, return_text_rect)
    return_rect = return_button.get_rect(center=(width / 2, height / 1.5)) # Déplacement de la définition de return_rect ici
    options_page.blit(return_button, return_rect)
    screen.blit(options_page, (0, 0))

    return_button = pygame.Surface((options_width, options_height))
    return_button.fill(GRAY)
    return_text = font.render("Retour", True, BLACK)
    return_text_rect = return_text.get_rect(center=(options_width / 2, options_height / 2))
    return_button.blit(return_text, return_text_rect)
    return_rect = return_button.get_rect(center=(width / 2, height / 1.5))
    
    pygame.display.flip()


# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if in_options:
            screen.blit(background_image,(0,0))  # Effacer l'écran en blanc si on est dans la page Options
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 pour le bouton gauche de la souris
                if in_options and return_rect.collidepoint(event.pos):
                    # Si l'utilisateur clique sur le bouton "Retour", changez la valeur de "in_options" à False
                    in_options = False
                elif options_rect.collidepoint(event.pos):
                    afficher_options()
    if in_options:
        afficher_options()
    else:
        afficher_menu()

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter le jeu    
pygame.quit()
