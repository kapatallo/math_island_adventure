import os
import pygame
import json

class CoursePage:
    def __init__(self, screen, images, return_callback, operation):
        self.screen = screen
        self.images_paths = images
        self.current_image_index = 0
        self.return_callback = return_callback
        self.operation = operation

        self.back_button = None
        self.back_button_rect = None
        self.inputs = []
        self.input_rects = []
        self.expected_answers = []
        self.input_positions = []
        self.input_active_states = []

        self.load_images()
        self.scale_images()
        self.create_buttons()

        self.setup_inputs()
        self.font_input = pygame.font.Font(None, 36)

    def load_images(self):
        self.images = [pygame.image.load(image_path) for image_path in self.images_paths]
        self.button_prev = pygame.image.load('retour.png')
        self.button_next = pygame.image.load('suivant.png')
        self.button_finish = pygame.image.load('terminer.png')
        self.back_button = pygame.image.load('back_button.png')

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

    def scale_images(self):
        self.images = [self.scale_image(image, self.screen.get_width(), self.screen.get_height()) for image in self.images]
        self.button_prev = self.scale_image(self.button_prev, 150, 150)
        self.button_next = self.scale_image(self.button_next, 150, 150)
        self.button_finish = self.scale_image(self.button_finish, 150, 150)
        self.back_button = self.scale_image(self.back_button, 50, 50)  # Adjust size as needed

    def create_buttons(self):
        self.button_prev_rect = self.button_prev.get_rect(topleft=(150, self.screen.get_height() - 70))
        self.button_next_rect = self.button_next.get_rect(topright=(self.screen.get_width() - 250, self.screen.get_height() - 70))
        self.button_finish_rect = self.button_finish.get_rect(topright=(self.screen.get_width() - 250, self.screen.get_height() - 70))
        self.back_button_rect = self.back_button.get_rect(topleft=(10, 10))  # Position at top left

    def setup_inputs(self):
        self.inputs = []
        self.input_rects = []
        self.expected_answers = []
        self.input_positions = []
        self.input_active_states = []

        if self.operation == "Addition" and self.current_image_index == len(self.images) - 2:
            self.expected_answers = [5, 7, 5, 2, 1]
            self.input_positions = [(235, 370), (277, 370), (530, 370), (572, 370), (530, 230)]
        elif self.operation == "Soustraction" and self.current_image_index == len(self.images) - 2:
            self.expected_answers = [1, 3, 3, 7, 5, 1]
            self.input_positions = [(235, 370), (277, 370), (530, 370), (572, 370), (512, 243), (554, 243)]
        elif self.operation == "Multiplication" and self.current_image_index == len(self.images) - 2:
            self.expected_answers = [2, 6, 8, 1, 2]
            self.input_positions = [(235, 370), (277, 370), (530, 370), (572, 370), (530, 230)]
        elif self.operation == "Division" and self.current_image_index == len(self.images) - 2:
            self.expected_answers = [7, 3]
            self.input_positions = [(335, 305), (517, 345)]

        for position in self.input_positions:
            rect = pygame.Rect(position[0], position[1], 30, 30)
            self.input_rects.append(rect)
            self.inputs.append('')
            self.input_active_states.append(False)

    def draw_inputs(self):
        for index, rect in enumerate(self.input_rects):
            input_color = (pygame.Color('green') if self.inputs[index] == str(self.expected_answers[index]) else pygame.Color('red')) if self.inputs[index] else pygame.Color('lightskyblue3')
            fill_color = pygame.Color('gray') if self.input_active_states[index] else pygame.Color('white')
            pygame.draw.rect(self.screen, fill_color, rect, 0, border_radius=5)  # Fill the input box with the appropriate color
            pygame.draw.rect(self.screen, input_color, rect, 2, border_radius=5)
            txt_surface = self.font_input.render(self.inputs[index], True, pygame.Color('black'))
            text_rect = txt_surface.get_rect(center=rect.center)
            self.screen.blit(txt_surface, text_rect)

    def draw_buttons(self):
        if self.current_image_index > 0:
            self.screen.blit(self.button_prev, self.button_prev_rect.topleft)
        if self.current_image_index < len(self.images) - 1:
            self.screen.blit(self.button_next, self.button_next_rect.topleft)
        if self.current_image_index == len(self.images) - 1:
            self.screen.blit(self.button_finish, self.button_finish_rect.topleft)

    def draw_screen(self):
        self.screen.blit(self.images[self.current_image_index], (0, 0))
        self.screen.blit(self.back_button, self.back_button_rect.topleft)
        self.draw_buttons()
        if self.current_image_index == len(self.images) - 2:
            self.draw_inputs()
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button_rect.collidepoint(event.pos):
                self.return_callback()

            if self.current_image_index > 0 and self.button_prev_rect.collidepoint(event.pos):
                self.current_image_index -= 1
                self.setup_inputs()
            elif self.current_image_index < len(self.images) - 1 and self.button_next_rect.collidepoint(event.pos):
                if self.current_image_index == len(self.images) - 2:
                    if all(self.inputs[i] == str(self.expected_answers[i]) for i in range(len(self.inputs))):
                        self.current_image_index += 1
                else:
                    self.current_image_index += 1
                self.setup_inputs()
            elif self.current_image_index == len(self.images) - 1 and self.button_finish_rect.collidepoint(event.pos):
                self.return_callback()

            # Check for clicks on input boxes
            for i, rect in enumerate(self.input_rects):
                if rect.collidepoint(event.pos):
                    self.input_active_states[i] = True
                else:
                    self.input_active_states[i] = False

        if event.type == pygame.KEYDOWN and self.current_image_index == len(self.images) - 2:
            for i, rect in enumerate(self.input_rects):
                if self.input_active_states[i]:
                    if event.key == pygame.K_BACKSPACE:
                        self.inputs[i] = self.inputs[i][:-1]
                    elif event.unicode.isnumeric():
                        self.inputs[i] += event.unicode

        if event.type == pygame.MOUSEMOTION:
            mouse_pos = event.pos
            is_cursor_set = False
            if (self.back_button_rect.collidepoint(mouse_pos) or
                self.button_prev_rect.collidepoint(mouse_pos) or
                self.button_next_rect.collidepoint(mouse_pos) or
                self.button_finish_rect.collidepoint(mouse_pos)):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                is_cursor_set = True
            else:
                for rect in self.input_rects:
                    if rect.collidepoint(mouse_pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_IBEAM)
                        is_cursor_set = True
                        break

                if not is_cursor_set:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def update(self):
        self.draw_screen()
