import os
import pygame
import json

class MainPage:
    def __init__(self, screen, screen_width, screen_height):
        # Autres initialisations
        self.load_json_data()  # Charger les données JSON
        self.question_progress = {}  # Dictionnaire pour stocker la progression des questions
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.load_images()
        self.scale_images()
        self.set_positions()
        self.avatar_target = None
        self.current_archipelago = None
        self.show_welcome_message = True

    def load_json_data(self):
        # Charger les données du fichier JSON
        with open('question.json', 'r', encoding='utf-8') as file:
            self.archipelago_data = json.load(file)

    def set_question_progression(self, level_title, is_completed):
        # Définir la progression d'une question spécifique
        self.question_progress[level_title] = is_completed

    def get_question_progression(self, level_title):
        # Obtenir la progression d'une question spécifique
        return self.question_progress.get(level_title, False)

    def is_archipelago_completed(self, theme):
        for island in self.archipelago_data["islands"]:
            if island["theme"] == theme:
                for level in island["levels"]:
                    if not level["completed"]:
                        return False
        return True
        
        
    

    def load_images(self):
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        self.background = pygame.image.load('back.png')
        self.addition_island = pygame.image.load('addition.png')
        self.soustraction_island = pygame.image.load('soustraction.png')
        self.multiplication_island = pygame.image.load('multiplication.png')
        self.division_island = pygame.image.load('division.png')
        self.avatar = pygame.image.load('avatar.png')
        self.avatar_moving = pygame.image.load('avatar_moving.png')
        self.logo = pygame.image.load('logo.png')
        self.welcome_message = pygame.image.load('msg_welcome.png')
        self.add_trophy=pygame.image.load('add_trophy.png')
        self.mul_trophy=pygame.image.load('mul_trophy.png')
        self.div_trophy=pygame.image.load('div_trophy.png')
        self.sous_trophy=pygame.image.load('sous_trophy.png')

    def scale_images(self):
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.addition_island = self.scale_image(self.addition_island, 350, 350)
        self.soustraction_island = self.scale_image(self.soustraction_island, 350, 330)
        self.multiplication_island = self.scale_image(self.multiplication_island, 300, 300)
        self.division_island = self.scale_image(self.division_island, 300, 300)
        self.avatar = self.scale_image(self.avatar, 100, 100)
        self.avatar_moving = self.scale_image(self.avatar_moving, 100, 100)
        self.logo = self.scale_image(self.logo, 250, 250)
        self.welcome_message = self.scale_image(self.welcome_message, 600, 150)
        self.add_trophy=self.scale_image(self.add_trophy,50,50)
        self.sous_trophy=self.scale_image(self.sous_trophy,50,50)
        self.mul_trophy=self.scale_image(self.mul_trophy,50,50)
        self.div_trophy=self.scale_image(self.div_trophy,50,50)

    def scale_image(self, image, max_width, max_height):
        width, height = image.get_size()
        aspect_ratio = width / height
        if width > max_width:
            width = max_width
            height = int(width / aspect_ratio)
        if height > max_height:
            height = max_height
            width = int(height * aspect_ratio)
        return pygame.transform.scale(image, (width, height))

    def set_positions(self):
        self.addition_pos = (50, 80)
        self.soustraction_pos = (600, 150)
        self.multiplication_pos = (20, 300)
        self.division_pos = (650, 350)
        self.logo_pos = (380, 3)
        self.avatar_pos = [(self.screen_width // 2 - self.avatar.get_width() // 2)-20, self.screen_height // 2 - self.avatar.get_height() // 2]
        self.welcome_message_pos = (450,100)
        self.add_trophy_pos = (40,20)
        self.sous_trophy_pos = (80,20)
        self.mul_trophy_pos = (120,20)
        self.div_trophy_pos = (160,20)
        

    def draw_screen(self):
        self.load_json_data()
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.addition_island, self.addition_pos)
        self.screen.blit(self.soustraction_island, self.soustraction_pos)
        self.screen.blit(self.multiplication_island, self.multiplication_pos)
        self.screen.blit(self.division_island, self.division_pos)
        self.screen.blit(self.avatar, self.avatar_pos)
        self.screen.blit(self.logo, self.logo_pos)
        if self.is_archipelago_completed("Addition"):
            self.screen.blit(self.add_trophy, self.add_trophy_pos)
        if self.is_archipelago_completed("Soustraction"):
            self.screen.blit(self.sous_trophy, self.sous_trophy_pos)
        if self.is_archipelago_completed("Multiplication"):
            self.screen.blit(self.mul_trophy, self.mul_trophy_pos)
        if self.is_archipelago_completed("Division"):
            self.screen.blit(self.div_trophy, self.div_trophy_pos)

        if self.show_welcome_message:
            self.screen.blit(self.welcome_message, self.welcome_message_pos)
        
        pygame.display.flip()

    def draw_screen_moving(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.addition_island, self.addition_pos)
        self.screen.blit(self.soustraction_island, self.soustraction_pos)
        self.screen.blit(self.multiplication_island, self.multiplication_pos)
        self.screen.blit(self.division_island, self.division_pos)
        self.screen.blit(self.avatar_moving, self.avatar_pos)
        self.screen.blit(self.logo, self.logo_pos)
        pygame.display.flip()

    def move_avatar(self, target_island_pos, target_island_img):
        offset_y = -100
        target_x = target_island_pos[0] + target_island_img.get_width() // 2 - self.avatar.get_width() // 2
        target_y = target_island_pos[1] + target_island_img.get_height() + offset_y
        steps = 30
        x_step = (target_x - self.avatar_pos[0]) / steps
        y_step = (target_y - self.avatar_pos[1]) / steps
        for _ in range(steps):
            self.avatar_pos[0] += x_step
            self.avatar_pos[1] += y_step
            self.draw_screen_moving()
            pygame.time.delay(2)
        self.current_archipelago = self.avatar_target

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if self.show_welcome_message:
                self.show_welcome_message = False

            if self.addition_island.get_rect(topleft=self.addition_pos).collidepoint(mouse_pos):
                self.avatar_target = "addition"
                self.move_avatar(self.addition_pos, self.addition_island)
            elif self.soustraction_island.get_rect(topleft=self.soustraction_pos).collidepoint(mouse_pos):
                self.avatar_target = "soustraction"
                self.move_avatar(self.soustraction_pos, self.soustraction_island)
            elif self.multiplication_island.get_rect(topleft=self.multiplication_pos).collidepoint(mouse_pos):
                self.avatar_target = "multiplication"
                self.move_avatar(self.multiplication_pos, self.multiplication_island)
            elif self.division_island.get_rect(topleft=self.division_pos).collidepoint(mouse_pos):
                self.avatar_target = "division"
                self.move_avatar(self.division_pos, self.division_island)
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            if (self.addition_island.get_rect(topleft=self.addition_pos).collidepoint(mouse_pos) or
                self.soustraction_island.get_rect(topleft=self.soustraction_pos).collidepoint(mouse_pos) or
                self.multiplication_island.get_rect(topleft=self.multiplication_pos).collidepoint(mouse_pos) or
                self.division_island.get_rect(topleft=self.division_pos).collidepoint(mouse_pos)):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
    def update(self):
        self.draw_screen()
