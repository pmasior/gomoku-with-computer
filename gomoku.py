#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import sys
import random
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # ukrycie powitania pygame
import pygame

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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
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
        rules2 = "of five stones horizontally, vertically or diagonally"
        action = "Click anywhere to start"
        self.draw_screen(action, rules, rules2)

    def show_gameover_screen(self):
        rules = None
        if self.winner == 1 or self.winner == 2:
            rules = "Won player " + str(self.winner)
        elif self.winner == PLAYER_DRAW:
            rules = "Draw. There is no winner"
        else:
            rules = "You are still playing"
        rules2 = "Player1    " + str(self.player1_wins)\
        + " : " + str(self.player2_wins) + "    Player 2"
        action = "Click anywhere to start next game"
        self.draw_screen(action, rules, rules2)

    def draw_screen(self, action, rules, rules2 = None):
        self.draw_background()
        self.draw_text(self.screen, 100, 100, "Gomoku", 84, WHITE, FONT_ICEBERG)
        self.draw_text(self.screen, 100, 250, rules, 28, WHITE, FONT_ICEBERG)
        self.draw_text(self.screen, 100, 300, rules2, 28, WHITE, FONT_ICEBERG)
        self.draw_text(self.screen, 100, 650, action, 28, WHITE, FONT_ICEBERG)

    def draw_background(self):
        self.screen.fill(BLACK)

    def draw_text(self, surface, x, y, text, size, color, font_family):
        font = pygame.font.Font(font_family, size)
        rendered_text = font.render(text, True, color)
        rect = rendered_text.get_rect()
        rect.topleft = (x, y)
        surface.blit(rendered_text, rect)


if __name__ == "__main__":
    game = Gomoku()
