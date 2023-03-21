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

# Charger le fichier audio dans un objet de son 
son_accueil = pygame.mixer.Sound("Bande son accueil.mp3")
son_accueil.play(-1)
son_accueil.set_volume(0.1)

# Volume de la bande son accueil (par défaut à 50%)
volume_bande_son_accueil = 0.5

# Volume des effets sonores (par défaut à 50%)
volume_effets_sonores = 0.5

# Luminosité (par défaut à 50%)
luminosite = 0.5

class Button:
    def __init__(self, text, width, height, x, y, color, font_color):
        self.text = text
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.font_color = font_color

        self.surface = pygame.Surface((self.width, self.height))
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))
        self.font = pygame.font.Font(None, 36)
        self.text_surface = self.font.render(self.text, True, self.font_color)
        self.text_rect = self.text_surface.get_rect(center=(self.width / 2, self.height / 2))
        self.surface.fill(self.color)
        self.surface.blit(self.text_surface, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Définir les dimensions et l'emplacement du premier bouton
button1 = Button("Niveau 1", 300, 100, 50, height / 1.3 - 100 / 1.3, BLUE_HACKER, BLACK)

# Définir les dimensions et l'emplacement du second boutton
button2 = Button("Niveau 2", 300, 100, 50, width / 2 - 100 / 2, BLUE_HACKER, BLACK)

# Définir les dimensions et l'emplacement du bouton option
options = Button("Options", 200, 70, 1475, height / 1.05 - 70 / 1.05, GRAY, BLACK)

# Définir les dimensions et l'emplacement du bouton quitter
quitter = Button("Quitter", 200, 70, 1700, height / 1.05 - 70 / 1.05, GRAY, BLACK)

# Définir les dimensions et l'emplacement du bouton retour (dans les options)
retour = Button("Retour", 200, 70, 1000, width / 2 - height / 1.5, GRAY, BLACK)

# Créer la fenêtre en mode plein écran
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Initialisation de la variable pour vérifier si nous sommes dans le menu principal
in_menu = True
in_options = False

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
    barre_volume_bande_son_rect.x = 300
    barre_volume_bande_son_rect.y = 200

    # Curseur pour régler le volume de la bande son
    curseur_volume_bande_son = pygame.Surface((500, 50))
    curseur_volume_bande_son.fill((0, 0, 0))  # couleur noire
    curseur_volume_bande_son_rect = curseur_volume_bande_son.get_rect()
    curseur_volume_bande_son_rect.x = int(300 + volume_bande_son_accueil * 200 - 10)
    curseur_volume_bande_son_rect.y = 200

    # Réduire le volume de la bande son en fonction du réglage
    son_accueil.set_volume(volume)

def afficher_options():
    global in_options, in_menu
    global return_rect
    global options_page

    # Si l'utilisateur clique sur le bouton "Options", changez la valeur de "in_options" à True
    in_options = True
    in_menu = False

    # Si "in_options" est True, afficher les éléments que vous souhaitez afficher pour la page "Options"
    screen.blit(background_image,(0,0))
    son_accueil.set_volume(0.1)

    options_page = pygame.Surface((width, height))
    options_page.fill(WHITE)
    options_title = font.render("Options", True, BLACK)
    options_title_rect = options_title.get_rect(center=(width / 2, height / 2.6))
    options_page.blit(options_title, options_title_rect)

    # Afficher le bouton retour à l'écran      
    screen.blit(retour.surface, retour.rect)

    # Appeler la fonction barre_volume après la création du curseur et avant l'affichage de la page
    barre_volume(0.1)
    options_page.blit(curseur_volume_bande_son, curseur_volume_bande_son_rect)
    options_page.blit(barre_volume_bande_son, barre_volume_bande_son_rect)    
    screen.blit(options_page, (0, 0))

    pygame.display.flip()

def afficher_menu():
    global in_options
    global in_menu, in_options
    global background_image

    in_options = False
    in_menu = True

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
    screen.blit(button1.surface, button1.rect)
    screen.blit(button2.surface, button2.rect)
    screen.blit(options.surface, options.rect)
    screen.blit(quitter.surface, quitter.rect)

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
                    if options.is_clicked(event.pos): # Si l'utilisateur appuie sur "options", accède à la partie "options"
                        afficher_options() 
                    elif quitter.is_clicked(event.pos): # Si l'utilisateur appuie sur "quitter", le jeu s'arrête
                        running = False 
                elif in_options:
                    if retour.is_clicked(event.pos): # Si l'utilisateur clique sur le bouton "Retour", changez la valeur de "in_options" à False
                        in_options = False 

    if in_options:
        afficher_options()
    else:
        afficher_menu()

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter le jeu 
pygame.quit()