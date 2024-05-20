import os
import pygame

class QuestionPage:
    def __init__(self, screen, background_image, title, text, questions):
        self.screen = screen
        self.background_image_path = background_image
        self.title = title
        self.text = text
        self.questions = questions
        self.current_question = 0
        self.user_input = ""
        self.input_active = False
        self.input_color_inactive = pygame.Color('lightskyblue3')
        self.input_color_active = pygame.Color('dodgerblue2')
        self.input_color = self.input_color_inactive

        self.avatar_state = "normal"
        self.avatar_timer = 0

        self.load_images()
        self.scale_images()
        self.load_font()
        self.create_button()
        self.create_input_box()

    def load_images(self):
        self.background = pygame.image.load(self.background_image_path)
        self.avatar_qst = pygame.image.load('avatar_qst.png')
        self.avatar_true = pygame.image.load('avatar_true.png')
        self.avatar_false = pygame.image.load('avatar_false.png')
        self.avatar_indice = pygame.image.load('avatar_indice.png')

    def scale_images(self):
        self.background = pygame.transform.scale(self.background, (self.screen.get_width(), self.screen.get_height()))
        self.avatar_qst = self.scale_image(self.avatar_qst, 400, 400)
        self.avatar_true = self.scale_image(self.avatar_true, 400, 400)
        self.avatar_false = self.scale_image(self.avatar_false, 400, 400)
        self.avatar_indice = self.scale_image(self.avatar_indice, 400, 400)

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

    def create_button(self):
        self.button_rect = pygame.Rect(800, 500, 150, 50)
        self.button_color = (0, 128, 255)
        self.hint_button_rect = pygame.Rect(800, 560, 150, 50)
        self.hint_button_color = (128, 128, 255)

    def create_input_box(self):
        self.input_box = pygame.Rect(490, 320, 140, 32)

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

    def draw_button(self):
        pygame.draw.rect(self.screen, self.button_color, self.button_rect)
        self.draw_text("Valider", (self.button_rect.x + 40, self.button_rect.y + 10), self.font_text, 250, (255, 255, 255))
        pygame.draw.rect(self.screen, self.hint_button_color, self.hint_button_rect)
        self.draw_text("Indice", (self.hint_button_rect.x + 40, self.hint_button_rect.y + 10), self.font_text, 250, (255, 255, 255))

    def draw_input_box(self):
        txt_surface = self.font_text.render(self.user_input, True, self.input_color)
        width = max(200, txt_surface.get_width() + 10)
        self.input_box.w = width
        self.screen.blit(txt_surface, (self.input_box.x + 5, self.input_box.y + 5))
        pygame.draw.rect(self.screen, self.input_color, self.input_box, 2)

    def draw_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_text(self.title, (520, 70), self.font_title, 350)
        self.draw_text(self.text, (490, 180), self.font_text, 320)
        self.draw_text(self.questions[self.current_question]['question'], (490, 250), self.font_text, 320)
        
        # Draw the appropriate avatar image
        if self.avatar_state == "normal":
            self.screen.blit(self.avatar_qst, (70, 150))
        elif self.avatar_state == "correct":
            self.screen.blit(self.avatar_true, (70, 150))
        elif self.avatar_state == "incorrect":
            self.screen.blit(self.avatar_false, (70, 150))
        elif self.avatar_state == "hint":
            self.screen.blit(self.avatar_indice, (70, 150))

        self.draw_input_box()
        self.draw_button()
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_box.collidepoint(event.pos):
                self.input_active = not self.input_active
            else:
                self.input_active = False

            self.input_color = self.input_color_active if self.input_active else self.input_color_inactive

            if self.button_rect.collidepoint(event.pos):
                try:
                    user_answer = int(self.user_input)
                    correct_answer = self.questions[self.current_question]['answer']
                    if user_answer == correct_answer:
                        self.input_color = pygame.Color('green')
                        self.avatar_state = "correct"
                        self.avatar_timer = pygame.time.get_ticks()
                    else:
                        self.input_color = pygame.Color('red')
                        self.avatar_state = "incorrect"
                        self.avatar_timer = pygame.time.get_ticks()
                except ValueError:
                    self.input_color = pygame.Color('red')
                    self.avatar_state = "incorrect"
                    self.avatar_timer = pygame.time.get_ticks()

            if self.hint_button_rect.collidepoint(event.pos):
                self.avatar_state = "hint"
                self.avatar_image = pygame.image.load("avatar_indice.png")

        if event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN:
                    try:
                        user_answer = int(self.user_input)
                        correct_answer = self.questions[self.current_question]['answer']
                        if user_answer == correct_answer:
                            self.input_color = pygame.Color('green')
                            self.avatar_state = "correct"
                            self.avatar_timer = pygame.time.get_ticks()
                        else:
                            self.input_color = pygame.Color('red')
                            self.avatar_state = "incorrect"
                            self.avatar_timer = pygame.time.get_ticks()
                    except ValueError:
                        self.input_color = pygame.Color('red')
                        self.avatar_state = "incorrect"
                        self.avatar_timer = pygame.time.get_ticks()
                elif event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                else:
                    self.user_input += event.unicode

    def update(self):
        # Check if the avatar state needs to be reset
        if self.avatar_state in ["correct", "incorrect"]:
            if pygame.time.get_ticks() - self.avatar_timer > 5000:
                self.avatar_state = "normal"
        self.draw_screen()
