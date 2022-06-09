import cmd
from Player import Player
from Game import Game
from Directions import Direction
import pickle
from Loader import Loader


class Commands(cmd.Cmd):
    intro = 'Welcome to Zombie in My Pocket type "start" to start playing the game, if you need help at any time type ' \
            '"help" Good Luck '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.player = Player()
        self.game = Game(self.player)
        self.load = Loader()

    # Overwrites default command line error message for better error handing - Daniel
    def default(self, line):
        self.stdout.write(
            'Unknown command used: %s\n please use all lowercase letters (type "help" for more info)\n' % (line,))

    # Puts the game into start state
    def do_start(self, line):
        try:
            if self.game.state == "Starting":
                self.game.start_game()
                self.game.get_game()
            else:
                print(
                    "You are currently playing a game type 'restart' if you want to start again")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_start():
        print("Type 'start' while seeing the intro")

    # Move to a north tile
    def do_n(self, line):
        try:
            if self.game.state == "Moving":
                self.game.select_move(Direction.NORTH)
                self.game.get_game()
                self.game.get_player_status()
            else:
                print("You are not currently in Move state")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_n():
        print("Type 'n' while in the moving state")

    # Move to a south tile
    def do_s(self, line):
        try:
            if self.game.state == "Moving":
                self.game.select_move(Direction.SOUTH)
                self.game.get_game()
                self.game.get_player_status()
            else:
                print("You are not currently in Move state")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_s():
        print("Type 's' while in the moving state")

    # Move to a east tile
    def do_e(self, line):
        try:
            if self.game.state == "Moving":
                self.game.select_move(Direction.EAST)
                self.game.get_game()
                self.game.get_player_status()
            else:
                print("You are not currently in Move state")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_e():
        print("Type 'e' while in the moving state")

    # Move to a west tile
    def do_w(self, line):
        try:
            if self.game.state == "Moving":
                self.game.select_move(Direction.WEST)
                self.game.get_game()
                self.game.get_player_status()
            else:
                print("You are not currently in Move state")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_w():
        print("Type 'w' while in the moving state")

    # Puts player in draw state so player draws a dev card
    def do_draw(self, line):
        try:
            if self.game.state == "Drawing Dev Card":
                self.game.trigger_dev_card(self.game.time)
            else:
                print("You are not in the drawing state")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_draw():
        print("Type 'draw' while in the drawing state")

    # Puts the game into rotate state
    def do_rotate(self, line):
        try:
            if self.game.state == "Rotating":
                self.game.rotate()
                self.game.get_game()
            else:
                print("You currently don't have a tile selected to rotate")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_rotate():
        print("Type 'rotate' while in the rotating state, each time the tile will rotate 90 degrees")

    # Puts the game into place state
    def do_place(self, line):
        try:
            if self.game.state == "Rotating":
                if self.load.chosen_tile.name == "Foyer":
                    self.game.place_tile(16, 16)
                elif self.game.check_dining_room_has_exit() is False:
                    return print("Dining room entrance must face an empty tile")
                else:
                    if self.game.get_current_tile().name == "Dining Room" \
                            and self.game.current_move_direction == self.game.get_current_tile().entrance:
                        if self.game.check_entrances_align():
                            self.game.place_tile(
                                self.game.chosen_tile.x, self.game.chosen_tile.y)
                            self.game.move_player(
                                self.game.chosen_tile.x, self.game.chosen_tile.y)
                    elif self.game.check_doors_align(self.game.current_move_direction):
                        self.game.place_tile(
                            self.game.chosen_tile.x, self.game.chosen_tile.y)
                        self.game.move_player(
                            self.game.chosen_tile.x, self.game.chosen_tile.y)
                    else:
                        print(
                            " Please rotate the tile you are placing until a door lines up with the direction you moved")
                self.game.get_game()
            else:
                print("You currently don't have a tile selected")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_place():
        print(
            "Type 'place' while in the rotating state, the doors of the new tile must line up with the direction you moved")

    # Select a direction to create a door if tile does not have any
    def do_choose(self, direction):
        try:
            dir_choice = ["n", "e", "s", "w"]
            if direction not in dir_choice:
                return print("Invalid input please type 'choose' and one of 'n', 'e', 's', 'w' ")
            if direction == 'n':
                direction = Direction.NORTH
            if direction == "e":
                direction = Direction.EAST
            if direction == "s":
                direction = Direction.SOUTH
            if direction == "w":
                direction = Direction.WEST
            if self.game.state == "Choosing Door":
                self.game.can_cower = False
                self.game.choose_door(direction)
            else:
                print("Your cannot create a door in this room")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_choose():
        print(
            "Type 'choose' and one of 'n', 'e', 's', 'w' while in the Choosing Door state to create a new door in that direction")

    # Calculates players damage taken when attacking zombies
    def do_attack(self, line):
        try:
            item1 = ''
            item2 = 0
            if "," in line:
                item1, item2 = [item for item in line.split(", ")]
            else:
                item1 = line

            if self.game.state == "Attacking":
                if item1 == '':
                    self.game.trigger_attack()
                elif item2 == 0:
                    self.game.trigger_attack(item1)
                elif item1 != '' and item2 != 0:
                    self.game.trigger_attack(item1, item2)

                if len(self.game.chosen_tile.doors) == 1 and self.game.chosen_tile.name != "Foyer":
                    self.game.state = "Choosing Door"
                    self.game.get_game()
                if self.game.state == "Game Over":
                    print("Sorry you lose, game over")
                    print("Type 'restart' to play again")
                else:
                    self.game.get_game()
            else:
                print("There is nothing to attack")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_attack():
        print(
            "Type 'attack' when faced with a group of zombies, the number of zombies minus your attack status will determine how much damage taken")

    # Lets players use items
    def do_use(self, line):
        try:
            item1 = ''
            item2 = 0
            if "," in line:
                item1, item2 = [item for item in line.split(", ")]
            else:
                item1 = line

            if self.game.state == "Moving":
                if item1 == '':
                    return
                if item2 == 0:
                    self.game.use_item(item1)
                elif item1 != '' and item2 != 0:
                    self.game.use_item(item1, item2)
            else:
                print("You cannot do that right now")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_use():
        print(
            "Type 'use' and the items name when attacking zombies, damage done will be increased and the damage taken will be reduced")

    # Lets players swap items
    def do_swap(self, line):
        try:
            if self.game.state == "Swapping Item":
                self.game.drop_item(line)
                self.game.player.add_item(
                    self.game.room_item[0], self.game.room_item[1])
                self.game.room_item = None
                self.game.get_game()
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_swap():
        print(
            "Type 'swap' and the name of the item you want to get rid of when you draw a new item when already carrying two items")

    # Lets players run from zombies
    def do_run(self, direction):
        try:
            if self.game.state == "Attacking":
                if direction == 'n':
                    self.game.trigger_run(Direction.NORTH)
                elif direction == 'e':
                    self.game.trigger_run(Direction.EAST)
                elif direction == 's':
                    self.game.trigger_run(Direction.SOUTH)
                elif direction == 'w':
                    self.game.trigger_run(Direction.WEST)
                else:
                    print("Cannot run that direction")
                if len(self.game.get_current_tile().doors) == 1 and self.game.chosen_tile.name != "Foyer":
                    self.game.state = "Choosing Door"
                    self.game.get_game()
            else:
                print("Cannot run when not being attacked")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_run():
        print("Type 'run' when faced with a group of zombies, you will return to the room you entered from")

    # Lets players cower from zombies to avoid damage but at the cost of an increase to the time
    def do_cower(self, line):
        try:
            if self.game.state == "Moving":
                self.game.trigger_cower()
            else:
                print("You cannot cower if you are not being attacked")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_cower():
        print(
            "Type 'cower' when faced with a group of zombies, you will hide from the zombies and take not damage but the time of day will increase")

    # Lets players find the totem in the evil temple at the cost of a card
    def do_search(self, line):
        try:
            if self.game.state == "Moving":
                self.game.search_for_totem()
            else:
                print("You cannot search for the totem here")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_search():
        print("Type 'search' when in the Evil Temple, the totem item will be found at the cost of a card")

    # Lets players bury the totem in the graveyard at the cost of a card
    def do_bury(self, line):
        try:
            if self.game.state == "Moving":
                self.game.bury_totem()
            else:
                print("You cannot bury for the totem here")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_bury():
        print("Type 'bury' when in the Graveyard, the totem item will be buried at the cost of a card")

    # Lets player exit the game
    def do_exit(self, line):
        try:
            return True

        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_exit():

        print("Type 'exit' at any time, the game will close without being saved")

    # Lets player see characters status
    def do_status(self, line):
        try:
            if self.game.state != "Game Over":
                self.game.get_player_status()
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_status():
        print(
            "Type 'status' at any time and you will be shown: the time of day, your health points, your attack points, the items you have and the games current state")

    def do_drop(self, item):
        try:
            if self.game.state != "Game Over":
                self.game.drop_item(item)
                self.game.get_game()
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_drop():
        print("Type 'drop' and the name of the item, that item will be thrown away")

    #  Restarts the game
    def do_restart(self, line):
        try:
            del self.game
            del self.player
            self.player = Player()
            self.game = Game(self.player)
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_restart():
        print("Type 'restart' at any time to start a new game")

    # save game working - Daniel
    def do_save(self, line):
        try:
            save_file = line + '.pickle'
            with open(save_file, 'wb') as sg:
                pickle.dump(self.game, sg)
                print("Game Saved")

            if len(self.game.tiles) == 0:
                return print("Please place a tile before saving")

            if not line:
                return print("Please enter a name for the saved game state")
        except SyntaxError:
            print(Commands.default)

    # Add to help file - Daniel
    @staticmethod
    def help_save():
        print("Type 'save' and a name for the save file at any time e.g. 'save sg1', to save your current progress")

    # load game working - Daniel
    def do_load(self, save):
        try:
            load = save + '.pickle'
            print("Game Loaded")
            with open(load, 'rb') as lg:
                self.game = pickle.load(lg)
                self.game.get_game()
        except FileNotFoundError:
            print("File not found please check name of save")
        except SyntaxError:
            print(Commands.default)

        if not save:
            return print("Please enter a valid name of a save")

    # Add to help file - Daniel
    @staticmethod
    def help_load():
        print("Type 'load' and the name of a saved file at any time e.g. 'load sg1', to load your past progress")
