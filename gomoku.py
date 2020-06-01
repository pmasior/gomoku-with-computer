#!/usr/bin/env python3

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
from gui import *


class Gomoku(Gui):
    def __init__(self):
        super().__init__()
        self.clock = pygame.time.Clock()
        self.human_wins = 0
        self.computer_wins = 0
        self.player_draw = 0
        self.last_winner = 0
        self.draw_welcome_screen()
        self.run()


    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(FRAMES_PER_SECOND)
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
        self.draw_gameover_screen()


    def save_last_game_status(self):
        self.winner = self.tie.winner
        if self.winner == HUMAN:
            self.human_wins += 1
        elif self.winner == COMPUTER:
            self.computer_wins += 1
        elif self.winner == PLAYER_DRAW:
            self.player_draw += 1



if __name__ == "__main__":
    game = Gomoku()
