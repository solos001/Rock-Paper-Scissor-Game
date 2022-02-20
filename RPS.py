import pygame
from settings import Settings
import os
import sys


class Block:
    def __init__(self, image, width, height, pos_x, pos_y):
        self.surface = pygame.transform.smoothscale(image, (width, height))
        self.rect = image.get_rect()
        self.width = width
        self.height = height

    def move(self, x, y):
        self.rect = self.rect.move(x, y)

    def expanded(self):
        expanded = pygame.transform.smoothscale(self.surface, (self.width * 1.3, self.height * 1.3))
        return expanded


class RpsGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings.Settings()
        self.display = pygame.display
        self.screen = self.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.display.set_caption('Rock-Paper-Scissor')
        self.events = pygame.event
        self.clock = pygame.time.Clock()
        self.assets = dict()
        self.game_data = dict()
        self.mouse = pygame.mouse

    def run_game(self):
        self.load_assets()
        sound_counter = True
        while True:
            self.clock.tick(self.settings.fps)
            self.check_events()
            if sound_counter and any(self.cursor_onhold().values()):
                self.assets['button_sound'].play()
                sound_counter = False
            elif not any((self.cursor_onhold().values())):
                sound_counter = True
            self.update_screen()

    def check_events(self):
        for event in self.events.get():
            if event.type == pygame.KEYDOWN:
                print(event.key)
            if event.type == pygame.QUIT:
                sys.exit()

    def update_screen(self):
        pygame.mouse.set_visible(False)
        self.screen.fill(self.settings.bg_color)
        self.button_drawer()
        self.time_bar()
        self.screen.blit(self.assets['cursor'], self.mouse.get_pos())
        self.display.update()

    def load_assets(self):
        rock_image = pygame.image.load(os.path.join('RPS_assets', 'rock.png'))
        scissor_image = pygame.image.load(os.path.join('RPS_assets', 'scissor.png'))
        paper_image = pygame.image.load(os.path.join('RPS_assets', 'paper.png'))
        button_sound = pygame.mixer.Sound(os.path.join('RPS_assets', 'button_sound.mp3'))
        cursor_image = pygame.transform.smoothscale(pygame.image.load(os.path.join('RPS_assets', 'cursor.cur')),
                                                    (30, 30))
        self.assets['rock'] = rock_image
        self.assets['scissor'] = scissor_image
        self.assets['paper'] = paper_image
        self.assets['cursor'] = cursor_image
        self.assets['button_sound'] = button_sound

    def time_bar(self, percent=1):
        pygame.draw.rect(self.screen, (192, 192, 192), pygame.Rect(348, 270, 204, 12), 2, 4, 4, 4, 4)
        pygame.draw.rect(self.screen, (47, 249, 36), pygame.Rect(350, 272, 200 * percent, 8), 0, 2, 2, 2, 2)

    def cursor_onhold(self):
        rock_rect = pygame.Rect(160, 360, 80, 80)
        paper_rect = pygame.Rect(410, 360, 80, 80)
        scissor_rect = pygame.Rect(660, 360, 80, 80)
        cursor_pos = self.mouse.get_pos()
        button_state = {'rock': rock_rect.collidepoint(cursor_pos), 'paper': paper_rect.collidepoint(cursor_pos),
                        'scissor': scissor_rect.collidepoint(cursor_pos)}
        return button_state

    def button_drawer(self):
        width, height = 100, 100
        if self.cursor_onhold()['rock']:
            rock = pygame.transform.smoothscale(self.assets['rock'], (width * 1.3, height * 1.3))
            self.screen.blit(rock, (135, 335))
        else:
            rock = pygame.transform.smoothscale(self.assets['rock'], (width, height))
            self.screen.blit(rock, (150, 350))

        if self.cursor_onhold()['paper']:
            paper = pygame.transform.smoothscale(self.assets['paper'], (width * 1.3, height * 1.3))
            self.screen.blit(paper, (385, 335))
        else:
            paper = pygame.transform.smoothscale(self.assets['paper'], (width, height))
            self.screen.blit(paper, (400, 350))

        if self.cursor_onhold()['scissor']:
            scissor = pygame.transform.smoothscale(self.assets['scissor'], (width * 1.3, height * 1.3))
            self.screen.blit(scissor, (635, 335))
        else:
            scissor = pygame.transform.smoothscale(self.assets['scissor'], (width, height))
            self.screen.blit(scissor, (650, 350))


class Player:
    def __init__(self):
        self.id = 1
        self.name = 'Player'
        self.score = 0

    def update_score(self, score):
        self.score = score

    def update_name(self, name):
        self.name = name


if __name__ == '__main__':
    game = RpsGame()
    game.run_game()

