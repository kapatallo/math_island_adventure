import pygame

class HomePage:
    def __init__(self, screen, start_game_callback, show_profile_callback):
        self.screen = screen
        self.start_game_callback = start_game_callback
        self.show_profile_callback = show_profile_callback
        self.load_assets()
        self.create_buttons()

    def load_assets(self):
        self.background = pygame.image.load('login_back.png')
        self.button_start = pygame.image.load('user_btn.png')
        self.button_profile = pygame.image.load('user_btn.png')
    
    def create_buttons(self):
        self.button_start_rect = self.button_start.get_rect(center=(self.screen.get_width() // 2, 200))
        self.button_profile_rect = self.button_profile.get_rect(center=(self.screen.get_width() // 2, 400))
    
    def update(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.button_start, self.button_start_rect.topleft)
        self.screen.blit(self.button_profile, self.button_profile_rect.topleft)
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button_start_rect.collidepoint(event.pos):
                self.start_game_callback()
            elif self.button_profile_rect.collidepoint(event.pos):
                self.show_profile_callback()

        if event.type == pygame.MOUSEMOTION:
            if (self.button_start_rect.collidepoint(event.pos) or
                self.button_profile_rect.collidepoint(event.pos)):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
