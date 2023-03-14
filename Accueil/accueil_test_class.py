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
    def __init__(self, width, height, x, y, color, text, text_color):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.text = text
        self.text_color = text_color

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        self.text_surface = font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surface.get_rect(center=(self.width / 2, self.height / 2))
        self.surface.blit(self.text_surface, self.text_rect)
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

    def draw(self, surface):
        surface.blit(self.surface, self.rect)


class Slider:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 500
        self.height = 50
        self.value = 0.5

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(BLACK)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
        self.cursor_surface = pygame.Surface((30, self.height))
        self.cursor_surface.fill(WHITE)
        self.cursor_rect = self.cursor_surface.get_rect(center=(self.rect.x + self.value * self.width, self.rect.centery))

    def draw(self, surface):
        self.cursor_rect.centerx = self.rect.x + self.value * self.width
        self.surface.fill(BLACK)
        pygame.draw.rect(self.surface, (0, 255, 0), (0, 0, int(self.value * self.width), self.height))
        self.surface.blit(self.cursor_surface, self.cursor_rect)
        surface.blit(self.surface, self.rect)

    def update(self, pos):
        if self.rect.collidepoint(pos):
            self.value = (pos[0] - self.rect.x) / self.width



buttons = []
sliders = []

button1 = Button(300, 100, 50, height / 1.3 - 100, BLUE_HACKER, "Niveau 1", BLACK)
button2 = Button(300, 100, 50, width / 2 - 50, BLUE_HACKER, "Niveau 2", BLACK)
options = Button(200, 70, 1475, height / 1.05 - 70, GRAY, "Options", BLACK)
quitter = Button(200, 70, 1700, height / 1.05 - 70, GRAY, "Quitter", BLACK)

slider_volume = Slider(500, 50)

buttons.append(button1)
buttons.append(button2)
buttons.append(options)
buttons.append(quitter)


# Définir les dimensions et l'emplacement du curseur volume
curseur_volume_x = 500
curseur_volume_y = 50

curseur_volume = pygame.Surface((curseur_volume_x, curseur_volume_y))
curseur_volume.fill(BLACK)
curseur_volume_rect = curseur_volume.get_rect(center=(curseur_volume_x, curseur_volume_y))


# Créer la fenêtre en mode plein écran
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Initialisation des variables pour se situer
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

    

    # Réduire le volume de la bande son en fonction du réglage
    son_accueil.set_volume(volume)

def afficher_options():
    global in_options, in_menu
    global options, curseur_volume
    global return_rect

    # Si l'utilisateur clique sur le bouton "Options", changez la valeur de "in_options" à True
    in_options = True
    in_menu = False

    # Si "in_options" est True, afficher les éléments que vous souhaitez afficher pour la page "Options"

    son_accueil.set_volume(0.1)

    options_page = pygame.Surface((width, height))
    options_page.fill(WHITE)
    options_title = font.render("Options", True, BLACK)
    options_title_rect = options_title.get_rect(center=(width / 2, height / 2))
    options_page.blit(options_title, options_title_rect)

    # Correction : supprimer le code redondant pour la création du bouton "Retour"
    return_button = pygame.Surface((options_width, options_height))
    return_button.fill(GRAY)
    return_text = font.render("Retour", True, BLACK)
    return_text_rect = return_text.get_rect(center=(options_width / 2, options_height / 2))
    return_button.blit(return_text, return_text_rect)
    return_rect = return_button.get_rect(center=(width / 2, height / 1.5)) 
    options_page.blit(return_button, return_rect)

    # Appeler la fonction barre_volume après la création du curseur et avant l'affichage de la page
    barre_volume(0.1)

    options_page.blit(curseur_volume, curseur_volume_rect)
    options_page.blit(barre_volume, barre_volume_rect)
    
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
                    if options_rect.collidepoint(event.pos): # Si l'utilisateur appuie sur "options", accède à la partie "options"
                        afficher_options() 
                    elif quitter_rect.collidepoint(event.pos): # Si l'utilisateur appuie sur "quitter", le jeu s'arrête
                        running = False 
                elif in_options:
                    if return_rect.collidepoint(event.pos): # Si l'utilisateur clique sur le bouton "Retour", changez la valeur de "in_options" à False
                        in_options = False 

    if in_options:
        screen.blit(background_image,(0,0))  # Effacer l'écran en blanc si on est dans la page Options
        afficher_options()
    else:
        afficher_menu()

    # Mettre à jour l'affichage
    pygame.display.flip()

# Quitter le jeu 
pygame.quit()