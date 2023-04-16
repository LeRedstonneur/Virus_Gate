import pygame

class Button:
    def __init__(self, x, y, width, height, text, color=(200, 200, 200)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = color
        self.activated = False

    def draw(self, screen, button_color):
        pygame.draw.rect(screen, button_color, self.rect)
        screen.blit(self.text_surface, (self.x + self.width // 2 - self.text_surface.get_width() // 2, self.y + self.height // 2 - self.text_surface.get_height() // 2))

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def verify_clik(self,mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.activated = True
    
    def verify_clik_alt(self,mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.activated = not self.activated