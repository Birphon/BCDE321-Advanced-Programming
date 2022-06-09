import random
import pickle
from Directions import Direction
from Loader import Loader
# from Action import Action
from Tile import Tile


class Game:
    # indoor_tiles=None, outdoor_tiles=None, dev_cards=None,  chosen_tile=None,(Moved to Loader.py)
    def __init__(self, player, time=9, game_map=None,
                 state="Starting", current_move_direction=None,
                 can_cower=True):
        if game_map is None:
            game_map = {}
        #        if indoor_tiles is None:
        #            indoor_tiles = []
        #        if outdoor_tiles is None:
        #            outdoor_tiles = []
        #       if dev_cards is None:
        #            dev_cards = []

        self.player = player
        self.time = time
        self.tiles = game_map
        # self.load.chosen_tile = chosen_tile
        self.state = state
        self.current_move_direction = current_move_direction
        self.current_zombies = 0
        self.can_cower = can_cower
        self.room_item = None
        self.load = Loader()

        #   self.indoor_tiles = indoor_tiles
        #   self.outdoor_tiles = outdoor_tiles
        #   self.dev_cards = dev_cards

    #  Puts the game into starting state using users input of the start command
    def start_game(self):
        """ Pre-condition: tiles and card not loaded in game in state of none
            Post-condition: tiles and card loaded in game in state of starting """
        # load = Loader()
        self.load.load_tiles()
        self.load.load_dev_cards()
        print('The dead walk the earth. You must search the house for the Evil Temple, and find the zombie totem. Then '
              'take the totem outside, and bury it in the Graveyard, all before the clock strikes midnight. ')
        for tile in self.load.indoor_tiles:
            if tile.name == 'Foyer':
                self.load.chosen_tile = tile
                self.state = "Rotating"
                break

    #  Loads the games different states and assigns command line text to them
    def get_game(self):
        """ Pre-condition: User has typed start command game is in starting state
            Post-condition: The assigned text is shown to the player depending on the state and command used """
        try:
            s = ''
            f = ''
            if self.state == "Moving":
                s = "In this state you can move by typing 'n, e, s, w' "
            if self.state == "Rotating":
                s = "Type 'rotate' until the door of the current tile are aligned with the new tile" \
                    " Once you are happy with the door position you can place the tile by typing 'place' "
            if self.state == "Choosing Door":
                s = "There are no doors you can go through in this room, you will have to make your-own" \
                    "Choose where to place a new door by typing 'choose' and a direction 'n, e, s, w' "
            if self.state == "Drawing Dev Card":
                s = "Type 'draw' to draw a random card this may lead to a zombie attack, and item or nothing " \
                    "depending on the time "
            for door in self.load.chosen_tile.doors:
                f += door.name + ', '
            return print(f' Your current tile is {self.load.chosen_tile.name}, the available doors in this room are {f}\n '
                         f'The state is {self.state}. {s} \n Special Entrances : {self.load.chosen_tile.entrance}')

        except AttributeError as e:
            print("ERROR: Unable to load game states, please try again", e)

    #  Shows player there current stats
    def get_player_status(self):
        """ Pre-condition: Player types status command and Game is in one of the active states Moving, Rotating,
        Choosing or Drawing Post-condition: Player is shown current stats and can continue the game """
        return print(f'It is {self.get_time()} pm \n'
                     f'The player currently has {self.player.get_health()} health \n'
                     f'The player currently has {self.player.get_attack()} attack \n'
                     f'The players items are {self.player.get_items()}\n'
                     f'The game state is {self.state}')

    def get_time(self):
        return self.time

    # Lets player draw tiles as the move- Daniel

    def draw_tile(self, x, y):
        """ Pre-condition: Game has loaded file containing tiles, player has typed a move command
            Post-condition: Games draws a random tile that player sees the name of and can be placed """
        if self.get_current_tile().type == "Indoor":
            if len(self.indoor_tiles) == 0:
                return print("No more indoor tiles")
            if self.get_current_tile().name == "Dining Room" \
                    and self.current_move_direction == self.get_current_tile().entrance:
                t = [t for t in self.outdoor_tiles if t.name == "Patio"]
                tile = t[0]
                tile.set_x(x)
                tile.set_y(y)
                self.load.chosen_tile = tile
            else:
                # Chooses a random indoor tile and places it
                tile = random.choice(self.indoor_tiles)
                tile.set_x(x)
                tile.set_y(y)
                self.load.chosen_tile = tile
        elif self.get_current_tile().type == "Outdoor":
            if len(self.outdoor_tiles) == 0:
                return print("No more outdoor tiles")
            tile = random.choice(self.outdoor_tiles)
            tile.set_x(x)
            tile.set_y(y)
            self.load.chosen_tile = tile

    def get_tile_at(self, x, y):
        return self.tiles[(x, y)]

    #  Lets player select a direction to move using tile doors
    def select_move(self, direction):
        """ Pre-condition: Game is in moving or running away state tile has doors player can use
            Post-condition: player is able to select a door using a direction command"""
        x, y = self.get_destination_coords(direction)
        if self.check_for_door(direction):
            self.current_move_direction = direction
            if self.check_for_room(x, y) is False:
                if self.state == "Running":
                    return print("Can only run into a discovered room")
                else:
                    self.draw_tile(x, y)
                    self.state = "Rotating"
            if self.check_for_room(x, y):
                if self.check_indoor_outdoor_move(self.get_current_tile().type, self.get_tile_at(x, y).type):
                    return print("Cannot Move this way")
                else:
                    self.move_player(x, y)

    def check_indoor_outdoor_move(self, current_type, move_type):
        if current_type != move_type and self.get_current_tile().name != "Patio" or "Dining Room":
            return False

    def get_destination_coords(self, direction):
        if direction == Direction.NORTH:
            return self.player.get_x(), self.player.get_y() - 1
        if direction == Direction.SOUTH:
            return self.player.get_x(), self.player.get_y() + 1
        if direction == Direction.EAST:
            return self.player.get_x() + 1, self.player.get_y()
        if direction == Direction.WEST:
            return self.player.get_x() - 1, self.player.get_y()

    def check_for_door(self, direction):
        if direction in self.get_current_tile().doors:
            return True
        else:
            return False

    def check_for_room(self, x, y):
        if (x, y) not in self.tiles:
            return False
        else:
            self.load.chosen_tile = self.tiles[(x, y)]
            return True

    def check_doors_align(self, direction):
        if self.load.chosen_tile.name == "Foyer":
            return True
        if direction == Direction.NORTH:
            if Direction.SOUTH not in self.load.chosen_tile.doors:
                return False
        if direction == Direction.SOUTH:
            if Direction.NORTH not in self.load.chosen_tile.doors:
                return False
        if direction == Direction.WEST:
            if Direction.EAST not in self.load.chosen_tile.doors:
                return False
        elif direction == Direction.EAST:
            if Direction.WEST not in self.load.chosen_tile.doors:
                return False
        return True

    def check_entrances_align(self):
        if self.get_current_tile().entrance == Direction.NORTH:
            if self.load.chosen_tile.entrance == Direction.SOUTH:
                return True
        if self.get_current_tile().entrance == Direction.SOUTH:
            if self.load.chosen_tile.entrance == Direction.NORTH:
                return True
        if self.get_current_tile().entrance == Direction.WEST:
            if self.load.chosen_tile.entrance == Direction.EAST:
                return True
        if self.get_current_tile().entrance == Direction.EAST:
            if self.load.chosen_tile.entrance == Direction.WEST:
                return True
        return print(" Dining room and Patio entrances dont align")

    def check_dining_room_has_exit(self):
        tile = self.load.chosen_tile
        if tile.name == "Dining Room":
            if self.current_move_direction == Direction.NORTH and tile.entrance == Direction.SOUTH:
                return False
            if self.current_move_direction == Direction.SOUTH and tile.entrance == Direction.NORTH:
                return False
            if self.current_move_direction == Direction.EAST and tile.entrance == Direction.WEST:
                return False
            if self.current_move_direction == Direction.WEST and tile.entrance == Direction.EAST:
                return False
        else:
            return True

    def place_tile(self, x, y):
        tile = self.load.chosen_tile
        self.tiles[(x, y)] = tile
        self.state = "Moving"
        if tile.type == "Outdoor":
            self.outdoor_tiles.pop(self.outdoor_tiles.index(tile))
        elif tile.type == "Indoor":
            self.indoor_tiles.pop(self.indoor_tiles.index(tile))

    def get_current_tile(self):
        return self.tiles[self.player.get_x(), self.player.get_y()]

    def lose_game(self):
        self.state = "Game Over"

    # -- Moved to Loader.py --

    # Load tiles from the Excel file, added error checking - Daniel
    #    def load_tiles(self):
    #        """ Pre-condition: Game has not started and the file containing the tiles can be loaded
    #            Post-condition: Games starts and tiles are loaded in """
    #        try:
    #            excel_data = pd.read_excel('Tiles.xlsx')
    #            tiles = []
    #            for name in excel_data.iterrows():
    #                tiles.append(name[1].tolist())
    #            for tile in tiles:
    #                doors = self.resolve_doors(tile[3], tile[4], tile[5], tile[6])
    #                if tile[2] == "Outdoor":
    #                    new_tile = OutdoorTile(tile[0], tile[1], doors)
    #                    if tile[0] == "Patio":
    #                        new_tile.set_entrance(Direction.NORTH)
    #                    self.outdoor_tiles.append(new_tile)
    #                if tile[2] == "Indoor":
    #                    new_tile = IndoorTile(tile[0], tile[1], doors)
    #                    if tile[0] == "Dining Room":
    #                        new_tile.set_entrance(Direction.NORTH)
    #                    self.indoor_tiles.append(new_tile)
    #
    #        except FileNotFoundError as e:
    #            print("ERROR: File not found please check Excel file name", e)
    #        except OSError as e:
    #            print("ERROR: Unable to access file please check file location", e)

    # -- Moved to Loader.py --

    # Load cards from Excel file, added error checking - Daniel
    #    def load_dev_cards(self):
    #        """ Pre-condition: Game has not started and the file containing the card can be loaded
    #            Post-condition: Games starts and cards are loaded in """
    #        try:
    #            card_data = pd.read_excel('DevCards.xlsx')
    #            for card in card_data.iterrows():
    #                item = card[1][0]
    #                event_one = (card[1][1], card[1][2])
    #                event_two = (card[1][3], card[1][4])
    #                event_three = (card[1][5], card[1][6])
    #                charges = card[1][7]
    #                dev_card = DevCard(item, charges, event_one, event_two, event_three)
    #                self.dev_cards.append(dev_card)
    #            random.shuffle(self.dev_cards)
    #            self.dev_cards.pop(0)
    #            self.dev_cards.pop(0)
    #
    #        except FileNotFoundError as e:
    #            print("ERROR: File not found please check Excel file name", e)
    #        except OSError as e:
    #            print("ERROR: Unable to access file please check file location", e)

    #  Moves the player to a new location when in the right state

    def move_player(self, x, y):
        """ Pre-condition: Game is in moving or running away state and there is a tile for player to move to
        Post-condition: player is moved to new tile """
        self.player.set_y(y)
        self.player.set_x(x)
        if self.state == "Running":
            self.state = "Moving"
        else:
            self.state = "Drawing Dev Card"

    def rotate(self):
        tile = self.load.chosen_tile
        tile.rotate_tile()
        if tile.name == "Foyer":
            return
        if self.get_current_tile().name == "Dining Room" or "Patio":
            tile.rotate_entrance()

    def trigger_dev_card(self, time):
        if len(self.dev_cards) == 0:
            if self.get_time == 11:
                print("You have run out of time")
                self.lose_game()
                return
            else:
                print("Reshuffling The Deck")
                self.load_dev_cards()
                self.time += 1

        dev_card = self.dev_cards[0]
        self.dev_cards.pop(0)
        event = dev_card.get_event_at_time(time)
        if event[0] == "Nothing":
            print("There is nothing in this room")
            if len(self.chosen_tile.doors) == 1 and self.chosen_tile.name != "Foyer":
                self.state = "Choosing Door"
                self.get_game()
                return
            else:
                self.state = "Moving"
                self.get_game()
            return
        elif event[0] == "Health":
            print("There might be something in this room")
            self.player.add_health(event[1])

            if event[1] > 0:
                print(f"You gained {event[1]} health")
                self.state = "Moving"
            elif event[1] < 0:
                print(f"You lost {event[1]} health")
                self.state = "Moving"
                if self.player.get_health() <= 0:
                    self.lose_game()
                    return
            elif event[1] == 0:
                print("You didn't gain or lose any health")
            if len(self.chosen_tile.doors) == 1 and self.chosen_tile.name != "Foyer":
                self.state = "Choosing Door"
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
            else:
                self.state = "Moving"
                self.get_game()
        elif event[0] == "Item":
            if len(self.dev_cards) == 0:
                if self.get_time == 11:
                    print("You have run out of time")
                    self.lose_game()
                    return
                else:
                    print("Reshuffling The Deck")
                    self.load_dev_cards()
                    self.time += 1
            next_card = self.dev_cards[0]
            print(f"There is an item in this room: {next_card.get_item()}")
            if len(self.player.get_items()) < 2:
                self.dev_cards.pop(0)
                self.player.add_item(next_card.get_item(), next_card.charges)
                print(f"You picked up the {next_card.get_item()}")
                if len(self.chosen_tile.doors) == 1 and self.chosen_tile.name != "Foyer":
                    self.state = "Choosing Door"
                    self.get_game()
                else:
                    self.state = "Moving"
                    self.get_game()
            else:
                self.room_item = [next_card.get_item(), next_card.charges]
                response = input("You already have two items, do you want to drop one of them? (Y/N) ")
                if response == "Y" or response == "y":
                    self.state = "Swapping Item"
                else:
                    self.state = "Moving"
                    self.room_item = None
                    self.get_game()
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
        elif event[0] == "Zombies":
            print(f"There are {event[1]} zombies in this room, prepare to fight!")
            self.current_zombies = int(event[1])
            self.state = "Attacking"

    def trigger_attack(self, *item):
        player_attack = self.player.get_attack()
        zombies = self.current_zombies
        if len(item) == 2:
            if "Oil" in item and "Candle" in item:
                print("You used the oil and the candle to attack the zombies, it kills all of them")
                self.drop_item("Oil")
                self.state = "Moving"
                return
            elif "Gasoline" in item and "Candle" in item:
                print("You used the gasoline and the candle to attack the zombies, it kills all of them")
                self.drop_item("Gasoline")
                self.state = "Moving"
                return
            elif "Gasoline" in item and "Chainsaw" in item:
                chainsaw_charge = self.player.get_item_charges("Chainsaw")
                self.player.set_item_charges("Chainsaw", chainsaw_charge + 2)
                player_attack += 3
                self.drop_item("Gasoline")
                self.player.use_item_charge("Chainsaw")
            else:
                print("These items cannot be used together, try again")
                return
        elif len(item) == 1:
            if "Machete" in item:
                player_attack += 2
            elif "Chainsaw" in item:
                if self.player.get_item_charges("Chainsaw") > 0:
                    player_attack += 3
                    self.player.use_item_charge("Chainsaw")
                else:
                    print("This item has no charges left")
            elif "Golf Club" in item or "Grisly Femur" in item or "Board With Nails" in item:
                player_attack += 1
            elif "Can of Soda" in item:
                self.player.add_health(2)
                self.drop_item("Can of Soda")
                print("Used Can of Soda, gained 2 health")
                return
            elif "Oil" in item:
                self.trigger_run(0)
                return
            else:
                print("You cannot use this item right now, try again")
                return

        damage = zombies - player_attack
        if damage < 0:
            damage = 0
        print(f"You attacked the zombies, you lost {damage} health")
        self.can_cower = True
        self.player.add_health(-damage)
        if self.player.get_health() <= 0:
            self.lose_game()
            return
        else:
            self.current_zombies = 0
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
            self.state = "Moving"

    def trigger_run(self, direction, health_lost=-1):
        self.state = "Running"
        self.select_move(direction)
        if self.state == "Moving":
            self.player.add_health(health_lost)
            print(f"You run away from the zombies, and lose {health_lost} health")
            self.can_cower = True
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
        else:
            self.state = "Attacking"

    def trigger_room_effect(self, room_name):
        if room_name == "Garden":
            self.player.add_health(1)
            print(f"After ending your turn in the {room_name} you have gained one health")
            self.state = "Moving"
        if room_name == "Kitchen":
            self.player.add_health(1)
            print(f"After ending your turn in the {room_name} you have gained one health")
            self.state = "Moving"

    def trigger_cower(self):
        if self.can_cower:
            self.player.add_health(3)
            self.dev_cards.pop(0)
            self.state = "Moving"
            print("You cower in fear, gaining 3 health, but lose time with the dev card")
        else:
            return print("Cannot cower during a zombie door attack")

    def drop_item(self, old_item):
        for item in self.player.get_items():
            if item[0] == old_item:
                self.player.remove_item(item)
                print(f"You dropped the {old_item}")
                self.state = "Moving"
                return
        print("That item is not in your inventory")

    def use_item(self, *item):
        if "Can of Soda" in item:
            self.player.add_health(2)
            self.drop_item("Can of Soda")
            print("Used Can of Soda, gained 2 health")
        elif "Gasoline" in item and "Chainsaw" in item:
            chainsaw_charge = self.player.get_item_charges("Chainsaw")
            self.player.set_item_charges("Chainsaw", chainsaw_charge + 2)
            self.drop_item("Gasoline")
        else:
            print("These items cannot be used right now")
            return

    def choose_door(self, direction):
        if direction in self.chosen_tile.doors:
            print("Choose a NEW door not an existing one")
            return False
        else:
            self.chosen_tile.doors.append(direction)
            self.current_zombies = 3
            print(f"{self.current_zombies} Zombies have appeared, prepare for battle. Use the attack command to"
                  f" fight or the run command to flee")
            self.state = "Attacking"

    def search_for_totem(self):
        if self.get_current_tile().name == "Evil Temple":
            if self.player.has_totem:
                print("player already has the totem")
                return
            else:
                self.trigger_dev_card(self.time)
                self.player.found_totem()
        else:
            print("You cannot search for a totem in this room")

    def bury_totem(self):
        if self.get_current_tile().name == "Graveyard":
            if self.player.has_totem:
                self.trigger_dev_card(self.time)
                if self.player.health != 0:
                    print("You Won")
                    self.state = "Game Over"
        else:
            print("Cannot bury totem here")

    def check_for_dead_player(self):
        if self.player.health <= 0:
            return True
        else:
            return False
