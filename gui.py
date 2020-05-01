#!/usr/bin/env python3
# -*- coding: utf_8 -*-

import pygame

from constants import *


class Gui():
    def __init__(self):
        pygame.init()
        pygame.mixer.quit()  # avoid error when pygame CPU usage is 100%
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption(TITLE)


    def draw_screen(self, action, rules, rules2 = None, rules3 = None):
        self.draw_background(DARK_GRAY)
        self.draw_text(self.screen, 100, 100, "Gomoku", 84, LIGHT_SAND)
        self.draw_text(self.screen, 100, 250, rules, 26, LIGHT_SAND)
        self.draw_text(self.screen, 100, 300, rules2, 26, LIGHT_SAND)
        self.draw_text(self.screen, 100, 350, rules3, 26, LIGHT_SAND)
        self.draw_text(self.screen, 100, 700, action, 26, LIGHT_SAND)


    def draw_background(self, color):
        self.screen.fill(color)


    def draw_grid(self):
        """ Rysuje pionowe i poziome linie """
        for c in range(GRID_X_BEGIN, GRID_X_END, GRID_TILESIZE):
            pygame.draw.line(self.screen, SAND, (c, GRID_Y_BEGIN), (c, GRID_Y_END), 2)
        for c in range(GRID_Y_BEGIN, GRID_Y_END, GRID_TILESIZE):
            pygame.draw.line(self.screen, SAND, (GRID_X_BEGIN, c), (GRID_X_END, c), 2)


    def show_actual_player(self):
        rect1 = pygame.draw.rect(self.screen, DARK_SAND, ((50, 25), (125, 40)))
        pygame.display.update(rect1)
        # print("P", self.next_player)  # DEBUG:
        if self.next_player == HUMAN:
            rect2 = self.draw_text(self.screen, 50, 25, "Human", 28, DARK_GRAY)
        elif self.next_player == COMPUTER:
            rect2 = self.draw_text(self.screen, 50, 25, "computer", 28, WHITE)
        pygame.display.update(rect2)


    def show_end_state_of_game(self):
        rect1 = pygame.draw.rect(self.screen, DARK_GRAY, ((0, 0), (800, 75)))
        pygame.display.update(rect1)
        if self.winner == HUMAN:
            rect2 = self.draw_text(self.screen, 50, 15, "Won Human", 36, DARK_GRAY)
        elif self.winner == COMPUTER:
            rect2 = self.draw_text(self.screen, 50, 15, "Won computer", 36, WHITE)
        elif self.winner == PLAYER_DRAW:
            rect2 = self.draw_text(self.screen, 50, 15, "Draw", 36, SAND)
        else:
            rect2 = self.draw_text(self.screen, 50, 15, "Testy", 36, SAND)
        pygame.display.update(rect2)


    def draw_text(self, surface, x, y, text, size, color, font_family = FONT_ICEBERG):
        font = pygame.font.Font(font_family, size)
        rendered_text = font.render(text, True, color)
        rect = rendered_text.get_rect()
        rect.topleft = (x, y)
        surface.blit(rendered_text, rect)
        return rect


    def draw_welcome_screen(self):
        rules = "The winner is first player whose form unbroken line"
        rules2 = "of exactly 5 stones horizontally, vertically or diagonally"
        action = "Click anywhere to start"
        self.draw_screen(action, rules, rules2)


    def draw_gameover_screen(self):
        rules = None
        if self.winner == HUMAN:
            rules = "Won Human"
        elif self.winner == COMPUTER:
            rules = "Won computer"
        elif self.winner == PLAYER_DRAW:
            rules = "Draw. There is no winner"
        else:
            rules = "You are still playing"
        rules2 = "Human    " + str(self.player1_wins)\
        + " : " + str(self.player2_wins) + "    computer"
        action = "Click anywhere to start next game"
        self.draw_screen(action, rules, rules2)



if __name__ == "__main__":
    print("You should run gomoku.py file")
