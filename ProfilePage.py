import pygame
import os
import json
import random

class ProfilePage:
    def __init__(self, screen, screen_width, screen_height, background_image, return_callback):
        self.screen = screen
        self.background_image_path = background_image
        self.return_callback = return_callback
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.offset_x = 190
        self.offset_y = 50

        self.load_images()
        self.scale_images()
        self.create_buttons()
        self.load_json_data()

        self.current_tab = 'Addition'  # Default tab
        self.selected_progress_images = {}  # Store selected progress images for each tab

    def load_json_data(self):
        # Charger les données du fichier JSON
        with open('question.json', 'r', encoding='utf-8') as file:
            self.archipelago_data = json.load(file)

        # Retirer le deuxième concept de chaque liste de niveaux
        for island in self.archipelago_data['islands']:
            if len(island['levels']) > 1:
                del island['levels'][1]

        self.calculate_progress_image()

    def load_images(self):
        self.background = pygame.image.load(self.background_image_path)
        self.back_button = pygame.image.load('back_button.png')
        self.done_image = pygame.image.load('done.png')
        self.not_done_image = pygame.image.load('not_done.png')
        self.tab_images = {
            'Addition_active': pygame.image.load('btn_add_act.png'),
            'Addition_inactive': pygame.image.load('btn_add_una.png'),
            'Soustraction_active': pygame.image.load('btn_sous_act.png'),
            'Soustraction_inactive': pygame.image.load('btn_sous_una.png'),
            'Multiplication_active': pygame.image.load('btn_mul_act.png'),
            'Multiplication_inactive': pygame.image.load('btn_mul_una.png'),
            'Division_active': pygame.image.load('btn_div_act.png'),
            'Division_inactive': pygame.image.load('btn_div_una.png')
        }
        self.progress_images = {
            0: ['0_v1.png'],
            20: ['20_v2.png'],
            40: ['40_v1.png'],
            60: ['60_v2.png'],
            80: ['80_v1.png'],
            100: ['100_v1.png']
        }

    def scale_images(self):
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.back_button = self.scale_image(self.back_button, 50, 50)  # Scale back button
        self.done_image = self.scale_image(self.done_image, 30, 30)
        self.not_done_image = self.scale_image(self.not_done_image, 30, 30)

        for key in self.tab_images:
            self.tab_images[key] = self.scale_image(self.tab_images[key], 150, 40)
        
        for key in self.progress_images:
            self.progress_images[key] = [self.scale_image(pygame.image.load(img), 280, 280) for img in self.progress_images[key]]

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

    def create_buttons(self):
        self.back_button_rect = self.back_button.get_rect(topleft=(10, 10))  # Position at top left
        self.tab_buttons = {
            'Addition': pygame.Rect(10 + self.offset_x, 60 + self.offset_y, 150, 40),
            'Soustraction': pygame.Rect(170 + self.offset_x, 60 + self.offset_y, 150, 40),
            'Multiplication': pygame.Rect(330 + self.offset_x, 60 + self.offset_y, 150, 40),
            'Division': pygame.Rect(490 + self.offset_x, 60 + self.offset_y, 150, 40)
        }

    def draw_tab_buttons(self):
        for tab, rect in self.tab_buttons.items():
            if self.current_tab == tab:
                self.screen.blit(self.tab_images[f'{tab}_active'], rect.topleft)
            else:
                self.screen.blit(self.tab_images[f'{tab}_inactive'], rect.topleft)

    def draw_concepts(self):
        font = pygame.font.Font(None, 24)
        header_font = pygame.font.Font(None, 28)
        y_offset = 120 + self.offset_y

        # Draw table headers
        concept_header = header_font.render("Concept", True, (0, 0, 0))
        mastered_header = header_font.render("maitrisé", True, (0, 0, 0))
        self.screen.blit(concept_header, (20 + self.offset_x - 65, y_offset))
        self.screen.blit(mastered_header, (450 + self.offset_x - 65, y_offset))
        y_offset += 40

        for island in self.archipelago_data['islands']:
            if island['theme'] == self.current_tab:
                for level in island['levels']:
                    concept = level['concept']
                    completed = level['completed']
                    text_surface = font.render(concept, True, (0, 0, 0))
                    self.screen.blit(text_surface, (20 + self.offset_x - 65, y_offset))
                    status_image = self.done_image if completed else self.not_done_image
                    self.screen.blit(status_image, (470 + self.offset_x - 65, y_offset))
                    y_offset += 40

    def calculate_progress_image(self):
        self.selected_progress_images = {}  # Reset the cache
        for island in self.archipelago_data['islands']:
            completed_levels = sum(level['completed'] for level in island['levels'])
            total_levels = len(island['levels'])
            completion_percentage = (completed_levels / total_levels) * 100
            progress_key = round(completion_percentage / 20) * 20
            self.selected_progress_images[island['theme']] = random.choice(self.progress_images[progress_key])

    def draw_progress_image(self):
        progress_image = self.selected_progress_images.get(self.current_tab)
        if progress_image:
            self.screen.blit(progress_image, (600 + self.offset_x - 130, 150 + self.offset_y - 20))

    def draw_screen(self):
        self.load_json_data()  # Recharger les données et recalculer les images de progression
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.back_button, self.back_button_rect.topleft)  # Draw back button
        self.draw_tab_buttons()
        self.draw_concepts()
        self.draw_progress_image()
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button_rect.collidepoint(event.pos):
                self.return_callback()  # Call the return callback
            for tab, rect in self.tab_buttons.items():
                if rect.collidepoint(event.pos):
                    self.current_tab = tab
                    self.calculate_progress_image()  # Recalculate progress image for new tab

    def update(self):
        self.draw_screen()
