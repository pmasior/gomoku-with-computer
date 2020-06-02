#!/usr/bin/env python3
"""Główny moduł"""

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # ukrycie powitania pygame
import sys

try:
    import pygame
except ModuleNotFoundError:
    print("Module Pygame not found, so you should install it using command:")
    print("python3 -m pip install pygame")
    sys.exit()

# pylint: disable=wrong-import-position
import constants as c
import gui
import tie

# Ignore false positive pygame errors
# pylint: disable=E1101

class Gomoku(gui.Gui):
    """Główna klasa uruchamiająca aplikację."""
    def __init__(self, screen):
        super().__init__(screen)
        self.clock = pygame.time.Clock()
        self.human_wins = 0
        self.computer_wins = 0
        self.player_draw = 0
        self.running = True
        self.winner = None
        self.actual_tie = None


    def start(self):
        """Uruchamia główną pętlę"""
        self.draw_welcome_screen()
        self.run()


    def run(self):
        """Główna pętla programu."""
        self.running = True
        while self.running:
            self.clock.tick(c.FRAMES_PER_SECOND)
            self.events()
            self.update()
            self.draw()


    def events(self):
        """Obsługiwane zdarzenia podczas każdej pętli w run()."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if event.type == pygame.MOUSEBUTTONUP:
                self.new_game()


    def update(self):
        """Aktualizacja obiektów podczas każdej pętli w run()."""


    def draw(self):
        """Rysowanie obiektów na ekranie podczas każdej pętli w run()."""
        pygame.display.flip()


    def new_game(self):
        """Rozpoczyna nową turę."""
        self.winner = None
        self.actual_tie = tie.Tie(self.screen, self.clock)
        self.actual_tie.start()
        self.game_over()


    def game_over(self):
        """Kończy turę."""
        self.save_last_game_status()
        self.draw_gameover_screen()


    def save_last_game_status(self):
        """Zapisuje, który gracz wygrał podczas ostatniej tury."""
        self.winner = self.actual_tie.winner
        if self.winner == c.HUMAN:
            self.human_wins += 1
        elif self.winner == c.COMPUTER:
            self.computer_wins += 1
        elif self.winner == c.PLAYER_DRAW:
            self.player_draw += 1



def main():
    """Funkcja inicjująca biblioteki zewnętrzne i tworząca obiekt klasy Gui."""
    pygame.init()
    pygame.mixer.quit()  # avoid error when pygame CPU usage is 100%
    pygame.display.set_caption(c.TITLE)
    screen = pygame.display.set_mode((c.WIDTH, c.HEIGHT), pygame.RESIZABLE)

    game = Gomoku(screen)

    game.start()



if __name__ == "__main__":
    main()
