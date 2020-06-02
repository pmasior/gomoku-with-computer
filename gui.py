#!/usr/bin/env python3
"""Graficzny interfejs użytkownika"""

import pygame

import constants as c

# Ignore false positive pygame errors
# pylint: disable=E1101

class Gui:
    """Obsługa graficznego interfejsu użytkownika."""
    def __init__(self, screen):
        self.screen = screen


    def draw_screen(self, action, rules, rules2=None, rules3=None):
        """Rysowanie ekranu z tytułem i komunikatem."""
        self.draw_background(c.PROMPT_BACKGROUND_COLOR)
        self.draw_text(self.screen, 100, 100, "Gomoku", 84, c.PROMPT_TEXT_COLOR)
        self.draw_text(self.screen, 100, 250, rules, 26, c.PROMPT_TEXT_COLOR)
        self.draw_text(self.screen, 100, 300, rules2, 26, c.PROMPT_TEXT_COLOR)
        self.draw_text(self.screen, 100, 350, rules3, 26, c.PROMPT_TEXT_COLOR)
        self.draw_text(self.screen, 100, 700, action, 26, c.PROMPT_TEXT_COLOR)


    def draw_background(self, color):
        """Rysowanie tła."""
        self.screen.fill(color)


    def draw_grid(self):
        """Rysuje pionowe i poziome linie."""
        for i in range(c.GRID_X_BEGIN, c.GRID_X_END, c.GRID_TILESIZE):
            pygame.draw.line(self.screen, c.GRID_COLOR,
                             (i, c.GRID_Y_BEGIN), (i, c.GRID_Y_END), 2)
        for i in range(c.GRID_Y_BEGIN, c.GRID_Y_END, c.GRID_TILESIZE):
            pygame.draw.line(self.screen, c.GRID_COLOR,
                             (c.GRID_X_BEGIN, i), (c.GRID_X_END, i), 2)


    def show_actual_player(self):
        """Pokazywanie aktualnego gracza w rogu ekranu podczas rozgrywki."""
        rect1 = pygame.draw.rect(self.screen, c.GAME_BACKGROUND_COLOR,
                                 ((50, 25), (125, 40)))
        pygame.display.update(rect1)
        if self.next_player == c.HUMAN:
            rect2 = self.draw_text(self.screen, 50, 25, "Human", 28,
                                   c.HUMAN_STONES_COLOR)
        elif self.next_player == c.COMPUTER:
            rect2 = self.draw_text(self.screen, 50, 25, "Computer", 28,
                                   c.COMPUTER_STONES_COLOR)
        pygame.display.update(rect2)


    def show_end_state_of_game(self):
        """Pokazywanie paska z informacją o zakończeniu gry."""
        rect1 = pygame.draw.rect(self.screen, c.PROMPT_BACKGROUND_COLOR,
                                 ((0, 0), (800, 75)))
        pygame.display.update(rect1)
        if self.winner == c.HUMAN:
            rect2 = self.draw_text(self.screen, 50, 15, "Human won", 36,
                                   c.GRID_COLOR)
        elif self.winner == c.COMPUTER:
            rect2 = self.draw_text(self.screen, 50, 15, "Computer won", 36,
                                   c.GRID_COLOR)
        elif self.winner == c.PLAYER_DRAW:
            rect2 = self.draw_text(self.screen, 50, 15, "Draw", 36,
                                   c.GRID_COLOR)
        pygame.display.update(rect2)


    def draw_text(self, surface, x_position, y_position, text, size, color,
                  font_family=c.FONT_ICEBERG):
        """Rysowanie tekstu na ekranie."""
        font = pygame.font.Font(font_family, size)
        rendered_text = font.render(text, True, color)
        rect = rendered_text.get_rect()
        rect.topleft = (x_position, y_position)
        surface.blit(rendered_text, rect)
        return rect


    def draw_welcome_screen(self):
        """Pokazywanie ekranu powitalnego po uruchomieniu aplikacji."""
        rules = "The winner is the first player whose form an unbroken line"
        rules2 = "of exactly 5 stones horizontally, vertically or diagonally"
        action = "Click anywhere to start"
        self.draw_screen(action, rules, rules2)


    def draw_gameover_screen(self):
        """Pokazywanie ekranu informującego o zakończeniu gry."""
        rules = None
        if self.winner == c.HUMAN:
            rules = "Human won"
        elif self.winner == c.COMPUTER:
            rules = "Computer won"
        elif self.winner == c.PLAYER_DRAW:
            rules = "Draw. There is no winner"
        else:
            rules = "You are still playing"
        rules2 = f'Human    {str(self.human_wins)} : {str(self.computer_wins)}    Computer'
        action = "Click anywhere to start next game"
        self.draw_screen(action, rules, rules2)



if __name__ == "__main__":
    print("You should run gomoku.py file")
