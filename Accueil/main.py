import pygame
print(pygame.ver)
import sys
sys.path.insert(0, '..')
#import Chapitre_2.Code.main as cp2

pygame.init()
pygame.mixer.init()

# Obtenir la résolution d'écran
screen_info = pygame.display.Info()
screen_width, screen_height = screen_info.current_w, screen_info.current_h

# Charger les image de fond
menu_bg = pygame.image.load("Fond d'ecran accueil.jpg")
options_bg = pygame.image.load("Fond d'ecran accueil.jpg")

# Récupérer la taille de l'image de fond
menu_bg_width, menu_bg_height = menu_bg.get_size()
options_bg_width, options_bg_height = options_bg.get_size()

# Calculer les positions pour centrer l'image
menu_bg_x = (screen_width - menu_bg_width) // 2
menu_bg_y = (screen_height - menu_bg_height) // 2
options_bg_x = (screen_width - options_bg_width) // 2
options_bg_y = (screen_height - options_bg_height) // 2


# Définir les couleurs
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)
GRAY = (140, 140, 140)
BLUE_HACKER = (45, 53, 82)
GREEN = (0, 220, 0)

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
button1 = Button("Niveau 1", 300, 100, 50, screen_height / 1.3 - 100 / 1.3, BLUE_HACKER, BLACK)

# Définir les dimensions et l'emplacement du second boutton
button2 = Button("Niveau 2", 300, 100, 50, screen_height / 1.1 - 100 / 1.3, BLUE_HACKER, BLACK)

# Définir les dimensions et l'emplacement du bouton option
options = Button("Options", 300, 100, screen_width - 350, screen_height / 1.3 - 100 / 1.3, GRAY, BLACK)

# Définir les dimensions et l'emplacement du bouton quitter
quitter = Button("Quitter", 300, 100, screen_width - 350, screen_height / 1.1 - 100 / 1.3, GRAY, BLACK)

# Définir les dimensions et l'emplacement du bouton retour (dans les options)
retour = Button("Retour", 300, 100, screen_width - 350, screen_height / 1.3 - 100 / 1.3, GRAY, BLACK)

# Créer la fenêtre en mode plein écran
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)

# Initialisation de la variable pour vérifier si nous sommes dans le menu principal
in_menu = True
in_options = False

class Barre:
    def __init__(self, width, height, x, y, x_curseur):
        self.x = x
        self.y = y
        self.curseur_x = x_curseur
        self.curseur_y = self.y

        self.surface = pygame.Surface((width, height))
        self.surface.fill(GREEN)
        self.rect = self.surface.get_rect(topleft=(self.x, self.y))

        self.curseur_surface = pygame.Surface((15, height))
        self.curseur_surface.fill((0, 0, 0)) # couleur noire
        self.curseur_rect = self.curseur_surface.get_rect(topleft=(self.curseur_x, self.curseur_y))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Définir la barre du volume avec son curseur
barre_volume = Barre(1000, 50, screen_width / 15, screen_height / 4 + 100, int(volume_bande_son_accueil * 1000))

# Définir la barre des effets sonores avec son curseur
barre_lumi = Barre(1000, 50, screen_width / 15, screen_height / 2 + 100, int(screen_width / 15 + 740))

def afficher_options():
    global in_menu, in_options, running
    global volume_bande_son_accueil

    while in_options:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                # Vérifier si l'utilisateur a cliqué sur le bouton "Echap"
                if event.key == pygame.K_ESCAPE:
                    in_options = False
                    in_menu = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 1 pour le bouton gauche de la souris
                    # Vérifier si l'utilisateur a cliqué sur le bouton "retour"
                    if retour.is_clicked(event.pos):
                        in_options = False
                        in_menu = True
                    if quitter.is_clicked(event.pos):
                        pygame.quit()
                        quit()

                    # Vérifier si l'utilisateur a cliqué sur la barre de progression du volume de la bande son
                    if barre_volume.is_clicked(event.pos):
                        # Régler le volume de la bande son en fonction de la position du curseur
                        volume_bande_son_accueil = ((event.pos[0] - (barre_volume.x)) / 1000)
                        son_accueil.set_volume(volume_bande_son_accueil)
                        barre_volume.curseur_x = int((barre_volume.x) + volume_bande_son_accueil * 1000)

                    # Vérifier si l'utilisateur a cliqué sur la barre de progression du volume de la luminosité
                    if barre_lumi.is_clicked(event.pos):
                        # Régler la luminosité en fonction de la position du curseur
                        pygame.display.set_gamma((event.pos[0]+180)/ 1000)
                        barre_lumi.curseur_x = event.pos[0]

        # Afficher l'image de fond
        screen.blit(options_bg, (options_bg_x, options_bg_y))

        # Afficher les boutons
        screen.blit(quitter.surface, quitter.rect)
        screen.blit(retour.surface, retour.rect)

        # Afficher le titre "Options"
        font = pygame.font.Font("freesansbold.ttf", 100)
        titre_surface = font.render("Options", True, WHITE)
        titre_rect = titre_surface.get_rect(center=(screen_width / 2, screen_height / 8))
        screen.blit(titre_surface, titre_rect)

        font = pygame.font.Font("freesansbold.ttf", 50)
        # Afficher le texte "Volume de la bande son"
        texte_volume_bande_son = font.render("Volume de la bande son", True, GRAY)
        texte_volume_bande_son_rect = texte_volume_bande_son.get_rect(topleft=(screen_width / 14, screen_height / 4))
        screen.blit(texte_volume_bande_son, texte_volume_bande_son_rect)

        # Afficher le texte "Luminosité de l'écran"
        texte_lumi = font.render("Luminosité de l'écran", True, GRAY)
        texte_lumi_rect = texte_lumi.get_rect(topleft=(screen_width / 14, screen_height / 2))
        screen.blit(texte_lumi, texte_lumi_rect)

        # Afficher les barres de réglages
        screen.blit(barre_volume.surface, barre_volume.rect)
        screen.blit(barre_lumi.surface, barre_lumi.rect)

        # Afficher le curseur à propos du volume
        barre_volume.curseur_rect = barre_volume.curseur_surface.get_rect(topleft=(barre_volume.curseur_x, barre_volume.curseur_y))
        barre_lumi.curseur_rect = barre_lumi.curseur_surface.get_rect(topleft=(barre_lumi.curseur_x, barre_lumi.curseur_y))
        screen.blit(barre_volume.curseur_surface, barre_volume.curseur_rect)
        screen.blit(barre_lumi.curseur_surface, barre_lumi.curseur_rect)

        pygame.display.update()


def afficher_menu():
    global in_options, in_menu, running
    global menu_bg

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1 pour le bouton gauche de la souris
                if options.is_clicked(event.pos): # Si l'utilisateur appuie sur "options", accède à la partie "options"
                    in_options = True
                    in_menu = False
                elif quitter.is_clicked(event.pos): # Si l'utilisateur appuie sur "quitter", le jeu s'arrête
                    pygame.quit()
                    quit()
                elif button1.is_clicked(event.pos):                   
                    in_menu = False
                    running = False
                elif button2.is_clicked(event.pos):
                    print("Niveau 2")
                    #cp2.start()
                    in_menu = False
                    running = False

        # Afficher le bg
        screen.blit(menu_bg, (menu_bg_x, menu_bg_y))

        # Définir la police et la couleur du texte
        font = pygame.font.Font("freesansbold.ttf", 150)
        text = font.render("Virus Gate", True, (GRAY))
        text_rect = text.get_rect()
        text_rect.center = (screen_width // 2, screen_height // 9)  # Centrer le texte dans la fenêtre
        screen.blit(text, text_rect)

        # Afficher les boutons à gauche de l'écran      
        screen.blit(button1.surface, button1.rect)
        screen.blit(button2.surface, button2.rect)
        screen.blit(options.surface, options.rect)
        screen.blit(quitter.surface, quitter.rect)

        pygame.display.flip()

# Boucle principale du jeu
def main():
    running = True
    while running:
        if in_options :
            afficher_options()
        elif in_menu :
            afficher_menu()

        # Mettre à jour l'affichage
        pygame.display.flip()

main()