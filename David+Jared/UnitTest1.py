import unittest

import main
from main import Game
from main import Player
from main import Tile
from directions import Direction as dir


class TestDevCards(unittest.TestCase):

    def test_dev_card_load(self):
        game = Game
        actual = self.game.load_dev_cards
        expected = self.game.load_dev_cards
        self.assertEqual(expected, actual)

    def test_dev_card_shuffle(self):
        game = Game
        actual = self.dev_cards[0]
        self.game.trigger_dev_card
        expected = self.dev_cards[0]
        self.assertNotEqual(expected, actual)


class TestGameTime(unittest.TestCase):
    def test_starting_time_should_equal_9(self):
        game = Game
        expected = game.time = 9
        actual = self.game.get_time()
        self.assertEqual(expected, actual)

    def test_time_after_no_shuffle_should_equal_9(self):
        game = Game
        expected = game.time = 9
        self.game.trigger_dev_card
        actual = self.game.get_time()
        self.assertNotEqual(expected, actual)

    def test_time_after_1_shuffle_should_equal_10(self):
        game = Game
        expected = game.time = 10
        self.game.trigger_dev_card
        actual = self.game.get_time()
        self.assertEqual(expected, actual)

    def test_time_after_2_shuffle_should_equal_11(self):
        game = Game
        expected = game.time = 11
        self.game.trigger_dev_card
        actual = self.game.get_time()
        self.game.state != "Game Over"
        self.assertEqual(expected, actual)

    def test_time_after_3_shuffle_should_equal_game_over(self):
        game = Game
        expected = game.time = 11
        actual = self.game.state = "Game Over"
        self.assertTrue(expected, actual)


if __name__ == '__main__':
    unittest.main()
