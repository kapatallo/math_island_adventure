import pygame
from QuestionPage import QuestionPage

class ArchipelagoPage:
    def __init__(self, screen, main_island_image, avatar_image, avatar_moving_image, ilot_done_image, ilot_locked_image, positions, background_image, titles, questions):
        self.screen = screen
        self.main_island_image = main_island_image
        self.avatar_image = avatar_image
        self.avatar_moving_image = avatar_moving_image
        self.ilot_done_image = ilot_done_image
        self.ilot_locked_image = ilot_locked_image
        self.positions = positions
        self.background_image = background_image
        self.titles = titles
        self.questions = questions

        self.avatar_pos = list(positions[0])  # Initial avatar position on the first îlot
        self.current_ilot_index = 0  # Start on the first îlot
        self.ilot_states = ['locked'] * 6  # All îlots start as locked

        self.load_images()
        self.scale_images()
        self.load_font()

    def load_font(self):
        self.font = pygame.font.Font(None, 24)  # Default font and size 24

    def load_images(self):
        self.background = pygame.image.load(self.background_image)
        self.main_island = pygame.image.load(self.main_island_image)
        self.avatar = pygame.image.load(self.avatar_image)
        self.avatar_moving = pygame.image.load(self.avatar_moving_image)
        self.ilot_done = pygame.image.load(self.ilot_done_image)
        self.ilot_locked = pygame.image.load(self.ilot_locked_image)

    def scale_images(self):
        self.background = pygame.transform.scale(self.background, (1000, 600))
        self.main_island = pygame.transform.scale(self.main_island, (400, 400))
        self.avatar = pygame.transform.scale(self.avatar, (100, 100))
        self.avatar_moving = pygame.transform.scale(self.avatar_moving, (100, 100))
        self.ilot_done = pygame.transform.scale(self.ilot_done, (120, 120))
        self.ilot_locked = pygame.transform.scale(self.ilot_locked, (120, 120))

    def draw_text(self, text, position):
        text_surface = self.font.render(text, True, (0, 0, 0))  # Black color
        self.screen.blit(text_surface, position)

    def draw_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.main_island, (300, 30))  # Center the main island


        for i, pos in enumerate(self.positions):
            ilot_image = self.ilot_done if self.ilot_states[i] == 'done' else self.ilot_locked
            self.screen.blit(ilot_image, pos)
            text_position = (pos[0] + ilot_image.get_width() // 2 - self.font.size(self.titles[i])[0] // 2, pos[1] - 20)
            self.draw_text(self.titles[i], text_position)

        self.screen.blit(self.avatar, self.avatar_pos)
        pygame.display.flip()

    def draw_screen_moving(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.main_island, (300, 30))  # Center the main island

        for i, pos in enumerate(self.positions):
            ilot_image = self.ilot_done if self.ilot_states[i] == 'done' else self.ilot_locked
            self.screen.blit(ilot_image, pos)
            text_position = (pos[0] + ilot_image.get_width() // 2 - self.font.size(self.titles[i])[0] // 2, pos[1] - 20)
            self.draw_text(self.titles[i], text_position)

        self.screen.blit(self.avatar_moving, self.avatar_pos)
        pygame.display.flip()

    def move_avatar(self, target_index):
        target_pos = self.positions[target_index]
        steps = 30
        x_step = (target_pos[0] - self.avatar_pos[0]) / steps
        y_step = (target_pos[1] - self.avatar_pos[1]) / steps
        for _ in range(steps):
            self.avatar_pos[0] += x_step
            self.avatar_pos[1] += y_step
            self.draw_screen_moving()
            pygame.time.delay(50)
        self.current_ilot_index = target_index
        self.draw_screen()  # Affiche l'image de l'avatar normal après le déplacement
 # Change to QuestionPage
        title = self.titles[target_index]
        text = self.questions[target_index]['text']
        questions = self.questions[target_index]['questions']
        self.question_page = QuestionPage(self.screen, 'back_qst.png', title, text, questions)

    def handle_event(self, event):
        if hasattr(self, 'question_page'):
            self.question_page.handle_event(event)
        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, pos in enumerate(self.positions):
                    ilot_image = self.ilot_done if self.ilot_states[i] == 'done' else self.ilot_locked
                    if ilot_image.get_rect(topleft=pos).collidepoint(mouse_pos):
                        self.move_avatar(i)
                        break

    def update(self):
        if hasattr(self, 'question_page'):
            self.question_page.update()
        else:
            self.draw_screen()