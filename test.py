#!/usr/bin/env python3
"Testy modułu tie"

import unittest
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1' # ukrycie powitania pygame

# pylint: disable=wrong-import-position
import numpy as np

import constants as c
import tie

class TestWinningDiagonally1(unittest.TestCase):
    """Sprawdzanie wygranej po przekątnej \ ."""  # pylint: disable=anomalous-backslash-in-string
    def setUp(self):
        self.actual_tie = tie.Tie(None, None)
        self.board = [[None for n in range(c.FIELDS)] for m in range(c.FIELDS)]
        self.board[0][0] = c.HUMAN
        self.board[1][1] = c.HUMAN
        self.board[2][2] = c.HUMAN
        self.board[3][3] = c.HUMAN
        self.board[4][4] = c.HUMAN

    def test_check_winning_diagonally1(self):
        """Test wykrywania wygranej w check_winning_diagonally1()."""
        self.assertTrue(self.actual_tie.check_winning_diagonally1(2, 2, 0, self.board,
                                                           c.HUMAN))

    def test_check_winning(self):
        """Test wykrywania wygranej w check_winning()."""
        self.assertTrue(self.actual_tie.check_winning(2, 2, self.board, c.HUMAN))



class TestWinningDiagonally2(unittest.TestCase):
    """Sprawdzanie wygranej po przekątnej / ."""
    def setUp(self):
        self.actual_tie = tie.Tie(None, None)
        self.board = [[None for n in range(c.FIELDS)] for m in range(c.FIELDS)]
        self.board[0][14] = c.HUMAN
        self.board[1][13] = c.HUMAN
        self.board[2][12] = c.HUMAN
        self.board[3][11] = c.HUMAN
        self.board[4][10] = c.HUMAN

    def test_check_winning_diagonally2(self):
        """Test wykrywania wygranej w check_winning_diagonally2()."""
        self.assertTrue(
            self.actual_tie.check_winning_diagonally2(2, 12, 0, self.board, c.HUMAN))

    def test_check_winning(self):
        """Test wykrywania wygranej w check_winning()."""
        self.assertTrue(self.actual_tie.check_winning(2, 12, self.board, c.HUMAN))



class TestWinningHorizontally(unittest.TestCase):
    """Sprawdzanie braku wygranej w poziomie."""
    def setUp(self):
        self.actual_tie = tie.Tie(None, None)
        self.board = [[None for n in range(c.FIELDS)] for m in range(c.FIELDS)]
        self.board[0][0] = c.COMPUTER
        self.board[1][0] = c.COMPUTER
        self.board[2][0] = c.COMPUTER
        self.board[3][0] = c.COMPUTER
        self.board[4][0] = c.COMPUTER
        self.board[5][0] = c.COMPUTER

    def test_check_winning_horizontally(self):
        """Test braku wygranej w check_winning_horizontally() przy 6 kamieniach."""
        self.assertFalse(self.actual_tie.check_winning_horizontally(2, 0, 0, self.board,
                                                             c.COMPUTER))

    def test_check_winning(self):
        """Test wykrywania braku wygranej w check_winning() przy 6 kamieniach."""
        self.assertIsNone(self.actual_tie.check_winning(2, 0, self.board, c.HUMAN))

    def test_end_if_gameover(self):
        """Test wykrywania braku końca gry w end_if_gameover()."""
        self.actual_tie.end_if_gameover(2, 0, self.board)
        self.assertIsNone(self.actual_tie.winner)



class TestWinningVertically(unittest.TestCase):
    """Sprawdzanie braku wygranej w pionie."""
    def setUp(self):
        self.actual_tie = tie.Tie(None, None)
        self.board = [[None for n in range(c.FIELDS)] for m in range(c.FIELDS)]
        self.board[10][0] = c.COMPUTER
        self.board[10][1] = c.COMPUTER
        self.board[10][2] = c.COMPUTER
        self.board[10][3] = c.COMPUTER
        self.board[10][4] = c.COMPUTER
        self.board[10][5] = c.COMPUTER

    def test_check_winning_vertically(self):
        """Test braku wygranej w check_winning_vertically() przy 6 kamieniach."""
        self.assertFalse(self.actual_tie.check_winning_vertically(10, 2, 0, self.board,
                                                           c.COMPUTER))

    def test_check_winning(self):
        """Test braku wygranej w check_winning() przy 6 kamieniach w linii."""
        self.assertIsNone(self.actual_tie.check_winning(10, 2, self.board, c.HUMAN))

    def test_end_if_gameover(self):
        """Test wykrywania braku końca gry w end_if_gameover()."""
        self.actual_tie.end_if_gameover(10, 2, self.board)
        self.assertIsNone(self.actual_tie.winner)



class TestCheckDraw(unittest.TestCase):
    """Sprawdzanie remisu."""
    def setUp(self):
        self.actual_tie = tie.Tie(None, None)
        self.board = [[None for n in range(c.FIELDS)] for m in range(c.FIELDS)]
        self.board = np.array(self.board)
        self.board[::2] = c.HUMAN
        self.board[1::2] = c.COMPUTER
        self.board = self.board.tolist()

    def test_check_winning(self):
        """Test wykrywania braku wygranej w check_winning przy remisie."""
        self.assertIsNone(self.actual_tie.check_winning(2, 12, self.board, c.HUMAN))

    def test_check_draw(self):
        """Test wykrywania remisu."""
        self.assertTrue(self.actual_tie.check_draw(self.board))



class TestChangePlayer(unittest.TestCase):
    """Sprawdzanie remisu."""
    def setUp(self):
        self.actual_tie = tie.Tie(None, None)
        self.actual_tie.next_player = c.COMPUTER

    def test_cange_player(self):
        """Test zmiany gracza."""
        self.assertIsNone(self.actual_tie.change_player())
        self.assertEqual(self.actual_tie.next_player, c.HUMAN)



if __name__ == '__main__':
    unittest.main()
