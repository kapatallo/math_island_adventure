import pygame
import json

# Définir la police
pygame.font.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
font = pygame.font.Font(None, 36)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Fonction pour afficher le texte
with open('question.json', 'r') as file:
    data = json.load(file)

def draw_text(screen, text, position, font, color=BLACK):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, position)
class ProfilePage:
    def __init__(self, screen, return_callback):
        self.screen = screen
        self.return_callback = return_callback
        self.load_assets()
        self.create_back_button()
        self.scroll_y = 0

    def load_assets(self):
        self.background = pygame.image.load('login_back.png')
        self.back_button = pygame.image.load('user_btn.png')
    
    def create_back_button(self):
        self.back_button_rect = self.back_button.get_rect(topleft=(10, 10))
        
    
    
    
    def display_profile(self, screen):
        y_offset = 10
        for island in data['islands']:
            draw_text(screen, f"Theme: {island['theme']}", (10, y_offset), font)
            y_offset += 30
            for level in island['levels']:
                y_offset += 30
                draw_text(screen, f"    Concept: {level['concept']}", (30, y_offset), font)
                y_offset += 30
                draw_text(screen, f"    Completed: {'Yes' if level['completed'] else 'No'}", (30, y_offset), font)
                y_offset += 40
            y_offset += 20  # Ajouter une ligne vide pour séparer les îles
            
    def scroll(self, amount):
        self.scroll_y += amount
    
    def update(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.back_button, self.back_button_rect.topleft)
        self.display_profile(screen)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button_rect.collidepoint(event.pos):
                self.return_callback()

        if event.type == pygame.MOUSEMOTION:
            if self.back_button_rect.collidepoint(event.pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Molette vers le haut
                self.scroll(20)
            elif event.button == 5:  # Molette vers le bas
                self.scroll(-20)
                                        
