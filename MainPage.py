import os
import pygame


class MainPage:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.load_images()
        self.scale_images()
        self.set_positions()
        self.avatar_pos = list(self.addition_pos)
        self.avatar_target = None
        self.current_archipelago = None

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

    def scale_images(self):
        self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
        self.addition_island = self.scale_image(self.addition_island, 300, 300)
        self.soustraction_island = self.scale_image(self.soustraction_island, 350, 350)
        self.multiplication_island = self.scale_image(self.multiplication_island, 300, 300)
        self.division_island = self.scale_image(self.division_island, 300, 300)
        self.avatar = self.scale_image(self.avatar, 100, 100)
        self.avatar_moving = self.scale_image(self.avatar_moving, 100, 100)
        self.logo = self.scale_image(self.logo, 250, 250)

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

    def draw_screen(self):
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.addition_island, self.addition_pos)
        self.screen.blit(self.soustraction_island, self.soustraction_pos)
        self.screen.blit(self.multiplication_island, self.multiplication_pos)
        self.screen.blit(self.division_island, self.division_pos)
        self.screen.blit(self.avatar, self.avatar_pos)
        self.screen.blit(self.logo, self.logo_pos)
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

    def update(self):
        self.draw_screen()

