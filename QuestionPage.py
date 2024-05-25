import os
import pygame

class QuestionPage:
    def __init__(self, screen, background_image, title, text, questions, level_image, return_callback):
        self.screen = screen
        self.background_image_path = background_image
        self.title = title
        self.text = text
        self.questions = questions
        self.level_image_path = level_image 
        self.return_callback = return_callback  
        self.back_button = None
        self.back_button_rect = None

        self.current_question = 0
        self.user_input = ""
        self.input_active = False
        self.input_color_inactive = pygame.Color('lightskyblue3')
        self.input_color_active = pygame.Color('dodgerblue2')
        self.input_color = self.input_color_inactive

        self.avatar_state = "normal"
        self.avatar_timer = 0

        self.message = ""
        self.message_color = pygame.Color('black')

        self.correct_answer_given = False  # Flag to track if correct answer is given

        self.load_images()
        self.scale_images()
        self.load_font()
        self.create_input_box()
        self.create_buttons()

    def load_images(self):
        self.background = pygame.image.load(self.background_image_path)
        self.avatar_qst = pygame.image.load('avatar_qst.png')
        self.avatar_true = pygame.image.load('avatar_true.png')
        self.avatar_false = pygame.image.load('avatar_false.png')
        self.avatar_indice = pygame.image.load('avatar_indice.png')
        self.button_validate = pygame.image.load('valider.png')
        self.button_hint = pygame.image.load('indice.png')
        self.level_image = pygame.image.load(os.path.join('qst_image', self.level_image_path))
        self.back_button = pygame.image.load('back_button.png')

    def scale_images(self):
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        self.avatar_qst = self.scale_image(self.avatar_qst, 400, 400)
        self.avatar_true = self.scale_image(self.avatar_true, 400, 400)
        self.avatar_false = self.scale_image(self.avatar_false, 400, 400)
        self.avatar_indice = self.scale_image(self.avatar_indice, 400, 400)
        self.button_validate = self.scale_image(self.button_validate, 175, 100)
        self.button_hint = self.scale_image(self.button_hint, 150, 100)
        self.level_image = self.scale_image(self.level_image, 300, 150)  # Adjust size as needed
        self.back_button = self.scale_image(self.back_button, 50, 50)  # Adjust size as needed

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

    def load_font(self):
        self.font_title = pygame.font.Font(None, 36)  # Font for the title
        self.font_text = pygame.font.Font(None, 24)   # Font for the text and questions
        self.font_input = pygame.font.Font(None, 36)  # Font for the input text
        self.font_message = pygame.font.Font(None, 28)  # Font for the messages

    def create_input_box(self):
        self.input_box = pygame.Rect(573, 390, 200, 35)
        self.button_validate_rect = pygame.Rect(585, 435, 150, 50)
        self.button_hint_rect = pygame.Rect(598, 500, 150, 50)

    def create_buttons(self):
        self.back_button_rect = self.back_button.get_rect(topleft=(10, 10))  # Position at top left

    def draw_text(self, text, position, font, max_width, color=(0, 0, 0)):
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width + font.size(' ')[0]
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width + font.size(' ')[0]

        if current_line:
            lines.append(' '.join(current_line))

        y_offset = 0
        for line in lines:
            line_surface = font.render(line, True, color)
            self.screen.blit(line_surface, (position[0], position[1] + y_offset))
            y_offset += font.get_linesize()

    def draw_buttons(self):
        self.screen.blit(self.button_validate, self.button_validate_rect.topleft)
        self.screen.blit(self.button_hint, self.button_hint_rect.topleft)

    def draw_input_box(self):
        pygame.draw.rect(self.screen, pygame.Color('white'), self.input_box, 0, border_radius=5)
        pygame.draw.rect(self.screen, self.input_color, self.input_box, 2, border_radius=5)
        txt_surface = self.font_input.render(self.user_input, True, pygame.Color('black'))
        text_rect = txt_surface.get_rect(center=self.input_box.center)
        self.screen.blit(txt_surface, text_rect)

    def draw_message(self):
        words = self.message.split(' ')
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = self.font_message.render(word, True, pygame.Color('black'))
            word_width, word_height = word_surface.get_size()
            if current_width + word_width <= 210:
                current_line.append(word)
                current_width += word_width + self.font_message.size(' ')[0]
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width + self.font_message.size(' ')[0]

        if current_line:
            lines.append(' '.join(current_line))

        base_y_position = 208
        x_position = 339  # Centré horizontalement
        y_offset = 0

        for line in lines:
            line_surface = self.font_message.render(line, True, pygame.Color('black'))
            message_rect = line_surface.get_rect(center=(x_position, base_y_position + y_offset))
            self.screen.blit(line_surface, message_rect)
            y_offset += self.font_message.get_linesize()
    def draw_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text(self.title, (550, 70), self.font_title, 350)
        self.draw_text(self.text, (520, 120), self.font_text, 320)

        if self.current_question < len(self.questions):
            self.draw_text(self.questions[self.current_question]['question'], (520, 320), self.font_text, 320)
        
        self.screen.blit(self.level_image, (590, 160))
        self.screen.blit(self.back_button, self.back_button_rect.topleft)  # Draw back button

        if self.avatar_state == "normal":
            self.screen.blit(self.avatar_qst, (70, 150))
        elif self.avatar_state == "correct":
            self.screen.blit(self.avatar_true, (70, 150))
        elif self.avatar_state == "incorrect":
            self.screen.blit(self.avatar_false, (70, 150))
        elif self.avatar_state == "hint":
            self.screen.blit(self.avatar_indice, (70, 150))

        self.draw_input_box()
        self.draw_buttons()
        self.draw_message()
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.input_active = not self.input_active
            else:
                self.input_active = False

            self.input_color = self.input_color_active if self.input_active else self.input_color_inactive

            if self.back_button_rect.collidepoint(event.pos):
                self.return_callback()  # Call the return callback

            if self.button_validate_rect.collidepoint(event.pos):
                try:
                    user_answer = int(self.user_input)
                    correct_answer = self.questions[self.current_question]['answer']
                    if user_answer == correct_answer:
                        self.input_color = pygame.Color('green')
                        self.avatar_state = "correct"
                        self.message = "Bravo ! C'est la bonne réponse."
                        self.user_input = ""  # Clear the input
                        self.correct_answer_given = True
                        self.avatar_timer = pygame.time.get_ticks()
                    else:
                        self.input_color = pygame.Color('red')
                        self.avatar_state = "incorrect"
                        self.message = "Oups ! Ce n'est pas la bonne réponse. Essaye encore."
                    self.avatar_timer = pygame.time.get_ticks()
                except ValueError:
                    self.input_color = pygame.Color('red')
                    self.avatar_state = "incorrect"
                    self.message = "Hmm... Cela ne ressemble pas à un nombre. Réessaye !"
                    self.avatar_timer = pygame.time.get_ticks()

            if self.button_hint_rect.collidepoint(event.pos):
                self.avatar_state = "hint"
                self.message = self.questions[self.current_question]['hint']

        if event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN:
                    try:
                        user_answer = int(self.user_input)
                        correct_answer = self.questions[self.current_question]['answer']
                        if user_answer == correct_answer:
                            self.input_color = pygame.Color('green')
                            self.avatar_state = "correct"
                            self.message = "Bonne réponse !"
                            self.user_input = ""  # Clear the input
                            self.correct_answer_given = True
                            self.avatar_timer = pygame.time.get_ticks()
                        else:
                            self.input_color = pygame.Color('red')
                            self.avatar_state = "incorrect"
                            self.message = "Mauvaise réponse."
                        self.avatar_timer = pygame.time.get_ticks()
                    except ValueError:
                        self.input_color = pygame.Color('red')
                        self.avatar_state = "incorrect"
                        self.message = "Veuillez entrer un nombre valide."
                        self.avatar_timer = pygame.time.get_ticks()
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                else:
                    self.user_input += event.unicode

    def update(self):
        if self.avatar_state in ["correct", "incorrect"]:
            if pygame.time.get_ticks() - self.avatar_timer > 3000:
                if self.correct_answer_given:
                    self.current_question += 1  # Move to the next question
                    self.correct_answer_given = False
                    if self.current_question >= len(self.questions):
                        self.return_callback()  # Return to archipelago if all questions are answered
                self.avatar_state = "normal"
                self.message = ""
        self.draw_screen()
