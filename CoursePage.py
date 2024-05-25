import pygame

class CoursePage:
    def __init__(self, screen, images, return_callback):
        self.screen = screen
        self.images_paths = images
        self.current_image_index = 0
        self.return_callback = return_callback

        self.back_button = None
        self.back_button_rect = None

        self.load_images()
        self.scale_images()
        self.create_buttons()

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
        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button_rect.collidepoint(event.pos):
                self.return_callback()

            if self.current_image_index > 0 and self.button_prev_rect.collidepoint(event.pos):
                self.current_image_index -= 1
            elif self.current_image_index < len(self.images) - 1 and self.button_next_rect.collidepoint(event.pos):
                self.current_image_index += 1
            elif self.current_image_index == len(self.images) - 1 and self.button_finish_rect.collidepoint(event.pos):
                self.return_callback()

    def update(self):
        self.draw_screen()
