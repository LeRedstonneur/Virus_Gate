import pygame

pygame.init()
pygame.mixer.init()

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

# Charger les fichiers audios dans un objet de son
son_accueil = pygame.mixer.Sound("Bande son accueil.mp3")
son_accueil.play(-1)
son_accueil.set_volume(0.1)

son_effets_sonores = pygame.mixer.Sound("Menu click button.mp3")
son_effets_sonores.play()
son_effets_sonores.set_volume(0.5)

# Définir les dimensions et l'emplacement du premier bouton
button1_x = 50
button1_y = height / 1.3 - 77

button1 = pygame.Surface((300, 100))
button1.fill(BLUE_HACKER )
button1_text = font.render("Niveau 1", True, BLACK)
button1_text_rect = button1_text.get_rect(center=(150, 50))
button1.blit(button1_text, button1_text_rect)

# Définir les dimensions et l'emplacement du second boutton
button2_x = 50
button2_y = width / 2 - 50
button2 = pygame.Surface((300, 100))
button2.fill(BLUE_HACKER )
button2_text = font.render("Niveau 2", True, BLACK)
button2_text_rect = button2_text.get_rect(center=(150, 50))
button2.blit(button2_text, button2_text_rect)
in_options = False

# Définir les dimensions et l'emplacement du bouton option
options_width = 200
options_height = 70
options_x = 1475
options_y = height / 1.05 - options_height / 1.05

options = pygame.Surface((options_width, options_height))
options.fill(GRAY)
options_text = font.render("Options", True, BLACK)
options_text_rect = options_text.get_rect(center=(options_width / 2, options_height / 2))
options.blit(options_text, options_text_rect)
options_rect = options.get_rect(topleft=(options_x, options_y))

# Définir les dimensions et l'emplacement du bouton quitter
quitter_width = 200
quitter_height = 70
quitter_x = 1700
quitter_y = height / 1.05 - quitter_height / 1.05

quitter = pygame.Surface((quitter_width, quitter_height))
quitter.fill(GRAY)
quitter_text = font.render("Quitter", True, BLACK)
quitter_text_rect = quitter_text.get_rect(center=(quitter_width / 2, quitter_height / 2))
quitter.blit(quitter_text, quitter_text_rect)
quitter_rect = quitter.get_rect(topleft=(quitter_x, quitter_y))

# Créer la fenêtre en mode plein écran
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Initialisation de la variable pour vérifier si nous sommes dans le menu principal
in_menu = True

def barre_volume(volume):
    global volume_bande_son_accueil
    global barre_volume_bande_son
    global barre_volume_bande_son_rect
    global curseur_volume_bande_son
    global curseur_volume_bande_son_rect

    volume_bande_son_accueil = volume

    # Mettre à jour la barre de progression du volume de la bande son
    barre_volume_bande_son = pygame.Surface((int(volume_bande_son_accueil * 5000), 50))
    barre_volume_bande_son.fill((0, 255, 0))  # couleur verte
    barre_volume_bande_son_rect = barre_volume_bande_son.get_rect()
    barre_volume_bande_son_rect.x = 710
    barre_volume_bande_son_rect.y = 250

    # Curseur pour régler le volume de la bande son
    curseur_volume_bande_son = pygame.Surface((500, 50))
    curseur_volume_bande_son.fill((0, 0, 0))  # couleur noire
    curseur_volume_bande_son_rect = curseur_volume_bande_son.get_rect()
    curseur_volume_bande_son_rect.x = int(710 + volume_bande_son_accueil * 200 - 10)
    curseur_volume_bande_son_rect.y = 250

    # Réduire le volume de la bande son en fonction du réglage
    son_accueil.set_volume(volume)

def barre_effets_sonores(effets_sonores):
    global volume_effets_sonores
    global barre_volume_effets_sonores
    global barre_volume_effets_sonores_rect
    global curseur_volume_effets_sonores
    global curseur_volume_effets_sonores_rect

    volume_effets_sonores = effets_sonores

    # Mettre à jour la barre de progression du volume de la bande son
    barre_volume_effets_sonores = pygame.Surface((int(volume_effets_sonores * 5000), 50))
    barre_volume_effets_sonores.fill((0, 255, 0))  # couleur verte
    barre_volume_effets_sonores_rect = barre_volume_effets_sonores.get_rect()
    barre_volume_effets_sonores_rect.x = 710
    barre_volume_effets_sonores_rect.y = 500

    # Curseur pour régler le volume de la bande son
    curseur_volume_effets_sonores = pygame.Surface((500, 50))
    curseur_volume_effets_sonores.fill((0, 0, 0))  # couleur noire
    curseur_volume_effets_sonores_rect = curseur_volume_effets_sonores.get_rect()
    curseur_volume_effets_sonores_rect.x = int(710 + volume_effets_sonores * 200 - 10)
    curseur_volume_effets_sonores_rect.y = 500

def barre_luminosite_fun(luminosite):
    global luminosite_reglages
    global barre_luminosite
    global barre_luminosite_rect
    global curseur_luminosite
    global curseur_luminosite_rect

    luminosite_reglages = luminosite

    # Mettre à jour la barre de progression du volume de la bande son
    barre_luminosite = pygame.Surface((int(luminosite_reglages * 5000), 50))
    barre_luminosite.fill((0, 255, 0))  # couleur verte
    barre_luminosite_rect = barre_luminosite.get_rect()
    barre_luminosite_rect.x = 710
    barre_luminosite_rect.y = 750

    # Curseur pour régler le volume de la bande son
    curseur_luminosite = pygame.Surface((500, 50))
    curseur_luminosite.fill((0, 0, 0))  # couleur noire
    curseur_luminosite_rect = curseur_luminosite.get_rect()
    curseur_luminosite_rect.x = int(710 + luminosite_reglages * 200 - 10)
    curseur_luminosite_rect.y = 750

def afficher_options():
    global in_options
    global in_menu
    global return_rect
    global options_page

    # Si l'utilisateur clique sur le bouton "Options", changez la valeur de "in_options" à True
    in_options = True
    in_menu = False

    # Si "in_options" est True, afficher les éléments que vous souhaitez afficher pour la page "Options"

    son_accueil.set_volume(0.1)

    options_page = pygame.Surface((width, height))
    options_page.fill(WHITE)
    options_title = font.render("Options", True, BLACK)
    options_title_rect = options_title.get_rect(center=(width / 2, height / 10))
    options_page.blit(options_title, options_title_rect)

    # Correction : supprimer le code redondant pour la création du bouton "Retour"
    return_button = pygame.Surface((options_width, options_height))
    return_button.fill(GRAY)
    return_text = font.render("Retour", True, BLACK)
    return_text_rect = return_text.get_rect(center=(options_width / 2, options_height / 2))
    return_button.blit(return_text, return_text_rect)
    return_rect = return_button.get_rect(center=(width / 2, height / 1.1)) 
    options_page.blit(return_button, return_rect)

    # Appeler les fonction des barres après la création du curseur et avant l'affichage de la page
    barre_volume(0.1)

    options_page.blit(curseur_volume_bande_son, curseur_volume_bande_son_rect)
    options_page.blit(barre_volume_bande_son, barre_volume_bande_son_rect)

    barre_effets_sonores(0.1)

    options_page.blit(curseur_volume_effets_sonores, curseur_volume_effets_sonores_rect)
    options_page.blit(barre_volume_effets_sonores, barre_volume_effets_sonores_rect)

    barre_luminosite_fun(0.1)   

    options_page.blit(curseur_luminosite, curseur_luminosite_rect)
    options_page.blit(barre_luminosite, barre_luminosite_rect)
    
    screen.blit(options_page, (0, 0))

    pygame.display.flip()

def afficher_menu():
    global in_options
    global in_menu
    global background_image

    # Charger l'image de fond
    background_image = pygame.image.load("Fond d'ecran accueil.jpg")
    options_bg = pygame.image.load("Fond d'ecran accueil.jpg")
    screen.blit(options_bg, (0, 0))

    # Définir la police et la couleur du texte
    font = pygame.font.Font("freesansbold.ttf", 150)
    text = font.render("Virus Gate", True, (GRAY))
    text_rect = text.get_rect()
    text_rect.center = (width // 2, height // 9)  # Centrer le texte dans la fenêtre
    screen.blit(text, text_rect)

    # Afficher les boutons à gauche de l'écran      
    screen.blit(button1, (button1_x, button1_y))
    screen.blit(button2, (button2_x, button2_y))
    screen.blit(options, (options_x, options_y))
    screen.blit(quitter, (quitter_x, quitter_y))

    options_rect = options.get_rect(topleft=(options_x, options_y))
    in_options = False
    in_menu = True
    pygame.display.flip()

# Boucle principale du jeu
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 pour le bouton gauche de la souris
                if in_menu:
                    if options_rect.collidepoint(event.pos):
                        afficher_options() # Accède à la partie "options"
                    elif quitter_rect.collidepoint(event.pos):
                        running = False # Si l'utilisateur appuie sur "quitter", le jeu s'arrête
                elif in_options:
                    if return_rect.collidepoint(event.pos):
                        in_options = False # Si l'utilisateur clique sur le bouton "Retour", changez la valeur de "in_options" à False

    if in_options:
        screen.blit(background_image,(0,0))  # Effacer l'écran en blanc si on est dans la page Options
        afficher_options()
    else:
        afficher_menu()

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter le jeu 
pygame.quit()
