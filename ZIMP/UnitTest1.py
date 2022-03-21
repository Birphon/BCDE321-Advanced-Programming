import unittest
from main import Game
from main import Commands


class TestGame(unittest.TestCase):
    def test_game_attributes(self):
        commands = Commands
        game = Game
        commands.do_n(game.state == "Moving")
        self.assertEqual(game.state == "Moving")


if __name__ == '__main__':
    unittest.main()
