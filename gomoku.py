#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import sys
import random
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # ukrycie powitania pygame
try:
    import pygame
except ModuleNotFoundError:
    print("Module Pygame not found, so you should install it using command:")
    print("python3 -m pip install pygame")
    sys.exit()

from tie import *
from player import *
from constants import *


class Gomoku():
    def __init__(self):
        pygame.init()
        pygame.mixer.quit()  # avoid error when pygame CPU usage is 100%
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.player1_wins = 0
        self.player2_wins = 0
        self.player_draw = 0
        self.last_winner = 0
        self.show_welcome_screen()
        self.run()

    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                # print("END")  # DEBUG:

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    # print("END")  # DEBUG:
            if event.type == pygame.MOUSEBUTTONUP:
                self.new_game()

    def update(self):
        pass

    def draw(self):
        pygame.display.flip()

    def new_game(self):
        self.winner = None
        self.tie = Tie(self.screen, self.clock)
        self.game_over()

    def game_over(self):
        self.save_last_game_status()
        self.show_gameover_screen()

    def save_last_game_status(self):
        self.winner = self.tie.winner
        if self.winner == PLAYER_1:
            self.player1_wins += 1
        elif self.winner == PLAYER_2:
            self.player2_wins += 1
        elif self.winner == PLAYER_DRAW:
            self.player_draw += 1

    def show_welcome_screen(self):
        rules = "The winner is first player whose form unbroken line"
        rules2 = "of exactly 5 stones horizontally, vertically or diagonally"
        action = "Click anywhere to start"
        self.draw_screen(action, rules, rules2)

    def show_gameover_screen(self):
        rules = None
        if self.winner == PLAYER_1:
            rules = "Won Human"
        elif self.winner == PLAYER_2:
            rules = "Won computer"
        elif self.winner == PLAYER_DRAW:
            rules = "Draw. There is no winner"
        else:
            rules = "You are still playing"
        rules2 = "Human    " + str(self.player1_wins)\
        + " : " + str(self.player2_wins) + "    computer"
        action = "Click anywhere to start next game"
        self.draw_screen(action, rules, rules2)

    def draw_screen(self, action, rules, rules2 = None):
        self.draw_background()
        self.draw_text(self.screen, 100, 100, "Gomoku", 84, LIGHT_SAND, FONT_ICEBERG)
        self.draw_text(self.screen, 100, 250, rules, 28, LIGHT_SAND, FONT_ICEBERG)
        self.draw_text(self.screen, 100, 300, rules2, 28, LIGHT_SAND, FONT_ICEBERG)
        self.draw_text(self.screen, 100, 650, action, 28, LIGHT_SAND, FONT_ICEBERG)

    def draw_background(self):
        self.screen.fill(DARK_GRAY)

    def draw_text(self, surface, x, y, text, size, color, font_family):
        font = pygame.font.Font(font_family, size)
        rendered_text = font.render(text, True, color)
        rect = rendered_text.get_rect()
        rect.topleft = (x, y)
        surface.blit(rendered_text, rect)



if __name__ == "__main__":
    game = Gomoku()
