import pygame
from settings import Settings
import os
import sys
import random

GREEN = (47, 249, 36)
GREY = (192, 192, 192)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class RpsGame:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.settings = Settings.Settings()
        self.display = pygame.display
        self.screen = self.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.display.set_caption('Rock-Paper-Scissor')
        self.events = dict()
        self.clock = pygame.time.Clock()
        self.assets = dict()
        self.game_data = dict()
        self.mouse = pygame.mouse
        self.computer_choices = []
        self.computer_choice_t = 0
        self.font = pygame.font.Font('RPS_assets//font.otf', 30)

    def run_game(self):
        self.load_assets()
        sound_counter = True
        round_counter = 0
        countdown_start = 0
        self.game_data['player_score'] = 0
        self.events['MOUSEBUTTONUP'] = False
        self.events['MOUSEBUTTONDOWN'] = False
        self.events['Clock_sound_ON'] = False
        while True:
            self.clock.tick(self.settings.fps)
            self.events['Timer_ON'] = False
            self.events['Countdown_ON'] = False
            if self.events['MOUSEBUTTONUP']:
                self.events['MOUSEBUTTONDOWN'] = False
            self.events['MOUSEBUTTONUP'] = False
            self.events['Clicked'] = False
            self.check_events()

            if round_counter == 0:
                pygame.time.set_timer(pygame.USEREVENT + 1, 300, loops=10)
                self.computer_choices = self.round_generator()
                self.computer_choice_t = self.computer_choices[round_counter][1]
                round_counter += 1
            elif round_counter > 0 and self.events['Timer_ON']:
                self.computer_choice_t = self.computer_choices[round_counter][1]
                self.game_data['computer_choice'] = self.computer_choices[round_counter][0]
                round_counter += 1
            if round_counter == 9:
                self.events['Clock_sound_ON'] = True
                countdown_start = pygame.time.get_ticks()
                round_counter = -1
                pygame.time.set_timer(pygame.USEREVENT + 1, 0, loops=10)
            if self.events['Clock_sound_ON']:
                self.assets['Clock-sound'].play()
                self.events['Clock_sound_ON'] = False
            if round_counter == -1 and pygame.time.get_ticks() < countdown_start + 2000:
                countdown_offset = pygame.time.get_ticks() - countdown_start
                percent = 1 - (countdown_offset / 2000)
                self.events['Countdown_ON'] = True
                self.game_data['percent'] = percent
                if percent > 0.3:
                    self.game_data['bar_color'] = GREEN
                else:
                    self.game_data['bar_color'] = RED
                if self.events['Clicked'] and any(self.cursor_onhold().values()):
                    for button_state in self.cursor_onhold():
                        if self.cursor_onhold()[button_state]:
                            self.game_data['player_choice'] = button_state
                    if self.outcome():
                        self.game_data['player_score'] += int(self.game_data['percent'] * 10)
                        self.assets['correct_sound'].play()
                    else:
                        self.game_data['player_score'] = 0
                        self.assets['wrong_sound'].play()
                    round_counter = 0
                    self.assets['Clock-sound'].stop()
            elif round_counter == -1 and pygame.time.get_ticks() > countdown_start + 2000:
                self.assets['wrong_sound'].play()
                round_counter = 0
                self.game_data['player_score'] = 0
                self.assets['Clock-sound'].stop()
            if sound_counter and any(self.cursor_onhold().values()):
                self.assets['button_sound'].play()
                sound_counter = False
            elif not any((self.cursor_onhold().values())):
                sound_counter = True
            self.update_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass
            if event.type == pygame.USEREVENT + 1:
                self.events['Timer_ON'] = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.events['MOUSEBUTTONDOWN'] = True
            if event.type == pygame.MOUSEBUTTONUP:
                self.events['MOUSEBUTTONUP'] = True
            if self.events['MOUSEBUTTONUP'] and self.events['MOUSEBUTTONDOWN']:
                self.events['MOUSEBUTTONDOWN'] = False
                self.events['MOUSEBUTTONUP'] = False
                self.events['Clicked'] = True
            if event.type == pygame.QUIT:
                sys.exit()

    def update_screen(self):
        pygame.mouse.set_visible(False)
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.assets['background'], (0, 0))
        self.button_drawer()
        if self.events['Countdown_ON']:
            self.time_bar(self.game_data['percent'])
        self.screen.blit(self.computer_choice_t, (350, 50))
        self.screen.blit(self.assets['cursor'], self.mouse.get_pos())
        self.screen.blit(self.score_display(), (700, 40))
        self.display.update()

    def load_assets(self):
        rock_image = pygame.image.load(os.path.join('RPS_assets', 'rock.png'))
        scissor_image = pygame.image.load(os.path.join('RPS_assets', 'scissor.png'))
        paper_image = pygame.image.load(os.path.join('RPS_assets', 'paper.png'))
        button_sound = pygame.mixer.Sound(os.path.join('RPS_assets', 'button_sound.mp3'))
        cursor_image = pygame.transform.smoothscale(pygame.image.load(os.path.join('RPS_assets', 'cursor.cur')),
                                                    (30, 30))
        correct_sound = pygame.mixer.Sound(os.path.join('RPS_assets', 'correct_sound_2.mp3'))
        wrong_sound = pygame.mixer.Sound(os.path.join('RPS_assets', 'wrong_sound_2.mp3'))
        clock_sound = pygame.mixer.Sound(os.path.join('RPS_assets', 'clock-ticking_f.mp3'))
        background = pygame.transform.smoothscale(pygame.image.load(os.path.join('RPS_assets', 'background4.png')),
                                                  (self.settings.screen_width, self.settings.screen_height))
        self.assets['rock'] = rock_image
        self.assets['scissor'] = scissor_image
        self.assets['paper'] = paper_image
        self.assets['cursor'] = cursor_image
        self.assets['button_sound'] = button_sound
        self.assets['correct_sound'] = correct_sound
        self.assets['wrong_sound'] = wrong_sound
        self.assets['Clock-sound'] = clock_sound
        self.assets['background'] = background

    def time_bar(self, percent=1):
        pygame.draw.rect(self.screen, (192, 192, 192), pygame.Rect(348, 270, 204, 12), 2, 4, 4, 4, 4)
        pygame.draw.rect(self.screen, self.game_data['bar_color'], pygame.Rect(350, 272, int(200 * percent), 8), 0, 2,
                         2, 2, 2)

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

    def round_generator(self):
        number_of_sets = 10
        keys = ['rock', 'paper', 'scissor']
        round_list = []
        for i in range(number_of_sets):
            random_pick = random.randint(0, 2)
            key_picked = keys[random_pick]
            value_picked = pygame.transform.smoothscale(self.assets[key_picked], (200, 200))
            round_list.append((key_picked, value_picked))
        return round_list

    def outcome(self):
        computer_choice = self.game_data['computer_choice']
        player_choice = self.game_data['player_choice']
        if (computer_choice == 'rock' and player_choice == 'paper') or (
                computer_choice == 'paper' and player_choice == 'scissor') or (
                computer_choice == 'scissor' and player_choice == 'rock'):
            return True
        else:
            return False

    def score_display(self, color=WHITE):
        score_num = self.game_data['player_score']
        score = self.font.render(f'Score: {score_num}', 1, color)
        return score


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
