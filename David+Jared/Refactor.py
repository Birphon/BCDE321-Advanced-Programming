# deck shuffling
import csv
import random
# Output
import cmd
#  Graphs
from sqlite3 import Row
# Timer
import time
#  Directions
from directions import Direction as dir
import pandas as pd
import openpyxl
# MathPlotLib
import matplotlib.pyplot as plt
# JSON
import json
#  Save and load Game
import pickle


class Game:
    def __init__(self, player, time=9, game_map=None, indoor_tiles=None, outdoor_tiles=None, chosen_tile=None,
                 dev_cards=None, state="Starting", current_move_direction=None, can_cower=True):
        if indoor_tiles is None:
            indoor_tiles = []
        if outdoor_tiles is None:
            outdoor_tiles = []
        if dev_cards is None:
            dev_cards = []
        if game_map is None:
            game_map = {}

        self.player = player
        self.time = time
        self.indoor_tiles = indoor_tiles
        self.outdoor_tiles = outdoor_tiles
        self.dev_cards = dev_cards
        self.tiles = game_map
        self.chosen_tile = chosen_tile
        self.state = state
        self.current_move_direction = current_move_direction
        self.current_zombies = 0
        self.can_cower = can_cower
        self.room_item = None

    def start_game(self):
        self.load_tiles()
        self.load_dev_cards()
        print('The dead walk the earth. You must search the house for the Evil Temple, and find the zombie totem. Then '
              'take the totem outside, and bury it in the Graveyard, all before the clock strikes midnight. ')
        for tile in self.indoor_tiles:
            if tile.name == 'Foyer':
                self.chosen_tile = tile
                self.state = "Rotating"
                break

    """Type the 'start' command when the game is in starting state"""

    def get_game(self):
        s = ''
        f = ''
        if self.state == "Moving":
            s = "In this state you can move by typing 'n, e, s, w' "
        if self.state == "Rotating":
            s = "Type 'rotate' until the door of the current tile are aligned with the new tile" \
                " Once you are happy with the door position you can place the tile by typing 'place' "
        if self.state == "Choosing Door":
            s = "Choose where to place a new door by typing 'choose' and a direction 'n, e, s, w' "
        if self.state == "Drawing Dev Card":
            s = "Type 'draw' to draw a random card this may lead to a zombie attack, and item or nothing depending on the time"
        for door in self.chosen_tile.doors:
            f += door.name + ', '
        return print(f' Your current tile is {self.chosen_tile.name}, the available doors in this room are {f}\n '
                     f'The state is {self.state}. {s} \n Special Entrances : {self.chosen_tile.entrance}')

    def get_player_status(self):
        return print(f'It is {self.get_time()} pm \n'
                     f'The player currently has {self.player.get_health()} health \n'
                     f'The player currently has {self.player.get_attack()} attack \n'
                     f'The players items are {self.player.get_items()}\n'
                     f'The game state is {self.state}')

    def get_time(self):
        return self.time

    # Loads tiles from excel file
    def load_tiles(self):  # Needs Error handling in this method
        excel_data = pd.read_excel('Tiles.xlsx')
        tiles = []
        for name in excel_data.iterrows():
            tiles.append(name[1].tolist())
        for tile in tiles:
            doors = self.resolve_doors(tile[3], tile[4], tile[5], tile[6])
            if tile[2] == "Outdoor":
                new_tile = OutdoorTile(tile[0], tile[1], doors)
                if tile[0] == "Patio":
                    new_tile.set_entrance(dir.NORTH)
                self.outdoor_tiles.append(new_tile)
            if tile[2] == "Indoor":
                new_tile = IndoorTile(tile[0], tile[1], doors)
                if tile[0] == "Dining Room":
                    new_tile.set_entrance(dir.NORTH)
                self.indoor_tiles.append(new_tile)

    def draw_tile(self, x, y):
        if self.get_current_tile().type == "Indoor":
            if len(self.indoor_tiles) == 0:
                return print("No more indoor tiles")
            if self.get_current_tile().name == "Dining Room" \
                    and self.current_move_direction == self.get_current_tile().entrance:
                t = [t for t in self.outdoor_tiles if t.name == "Patio"]
                tile = t[0]
                tile.set_x(x)
                tile.set_y(y)
                self.chosen_tile = tile
            else:
                tile = random.choice(self.indoor_tiles)  # Chooses a random indoor tile and places it
                tile.set_x(x)
                tile.set_y(y)
                self.chosen_tile = tile
        elif self.get_current_tile().type == "Outdoor":
            if len(self.outdoor_tiles) == 0:
                return print("No more outdoor tiles")
            tile = random.choice(self.outdoor_tiles)
            tile.set_x(x)
            tile.set_y(y)
            self.chosen_tile = tile

    # Loads development cards from excel file
    def load_dev_cards(self):
        card_data = pd.read_excel('DevCards.xlsx')
        for card in card_data.iterrows():
            item = card[1][0]
            event_one = (card[1][1], card[1][2])
            event_two = (card[1][3], card[1][4])
            event_three = (card[1][5], card[1][6])
            charges = card[1][7]
            dev_card = DevCard(item, charges, event_one, event_two, event_three)
            self.dev_cards.append(dev_card)
        random.shuffle(self.dev_cards)
        self.dev_cards.pop(0)
        self.dev_cards.pop(0)

    def move_player(self, x, y):
        self.player.set_y(y)
        self.player.set_x(x)
        if self.state == "Running":
            self.state = "Moving"
        else:
            self.state = "Drawing Dev Card"

    def get_tile_at(self, x, y):
        return self.tiles[(x, y)]

    def select_move(self, direction):
        x, y = self.get_destination_coords(direction)
        if self.check_for_door(direction):  # If there's a door where the player tried to move
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

    def get_destination_coords(self, direction):  # Gets the x and y value of the proposed move
        if direction == dir.NORTH:
            return self.player.get_x(), self.player.get_y() - 1
        if direction == dir.SOUTH:
            return self.player.get_x(), self.player.get_y() + 1
        if direction == dir.EAST:
            return self.player.get_x() + 1, self.player.get_y()
        if direction == dir.WEST:
            return self.player.get_x() - 1, self.player.get_y()

    def check_for_door(self, direction):  # Takes a direction and checks if the current room has a door there
        if direction in self.get_current_tile().doors:
            return True
        else:
            return False

    def check_for_room(self, x, y):  # Takes a move direction and checks if there is a room there
        if (x, y) not in self.tiles:
            return False
        else:
            self.chosen_tile = self.tiles[(x, y)]
            return True

    def check_doors_align(self, direction):
        if self.chosen_tile.name == "Foyer":
            return True
        if direction == dir.NORTH:
            if dir.SOUTH not in self.chosen_tile.doors:
                return False
        if direction == dir.SOUTH:
            if dir.NORTH not in self.chosen_tile.doors:
                return False
        if direction == dir.WEST:
            if dir.EAST not in self.chosen_tile.doors:
                return False
        elif direction == dir.EAST:
            if dir.WEST not in self.chosen_tile.doors:
                return False
        return True

    def check_entrances_align(self):
        if self.get_current_tile().entrance == dir.NORTH:
            if self.chosen_tile.entrance == dir.SOUTH:
                return True
        if self.get_current_tile().entrance == dir.SOUTH:
            if self.chosen_tile.entrance == dir.NORTH:
                return True
        if self.get_current_tile().entrance == dir.WEST:
            if self.chosen_tile.entrance == dir.EAST:
                return True
        if self.get_current_tile().entrance == dir.EAST:
            if self.chosen_tile.entrance == dir.WEST:
                return True
        return print(" Dining room and Patio entrances dont align")

    def check_dining_room_has_exit(self):
        tile = self.chosen_tile
        if tile.name == "Dining Room":
            if self.current_move_direction == dir.NORTH and tile.entrance == dir.SOUTH:
                return False
            if self.current_move_direction == dir.SOUTH and tile.entrance == dir.NORTH:
                return False
            if self.current_move_direction == dir.EAST and tile.entrance == dir.WEST:
                return False
            if self.current_move_direction == dir.WEST and tile.entrance == dir.EAST:
                return False
        else:
            return True

    def place_tile(self, x, y):
        tile = self.chosen_tile
        self.tiles[(x, y)] = tile
        self.state = "Moving"
        if tile.type == "Outdoor":
            self.outdoor_tiles.pop(self.outdoor_tiles.index(tile))
        elif tile.type == "Indoor":
            self.indoor_tiles.pop(self.indoor_tiles.index(tile))

    def get_current_tile(self):  # returns the current tile that the player is at
        return self.tiles[self.player.get_x(), self.player.get_y()]

    def rotate(self):
        tile = self.chosen_tile
        tile.rotate_tile()
        if tile.name == "Foyer":
            return
        if self.get_current_tile().name == "Dining Room" or "Patio":
            tile.rotate_entrance()

    # Call when player enters a room and draws a dev card
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
        event = dev_card.get_event_at_time(time)  # Gets the event at the current time
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
        elif event[0] == "Health":  # Change health of player
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
        elif event[0] == "Item":  # Add item to player's inventory if there is room
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
                else:  # If player doesn't want to drop item, just move on
                    self.state = "Moving"
                    self.room_item = None
                    self.get_game()
            if self.get_current_tile().name == "Garden" or "Kitchen":
                self.trigger_room_effect(self.get_current_tile().name)
        elif event[0] == "Zombies":  # Add zombies to the game, begin combat
            print(f"There are {event[1]} zombies in this room, prepare to fight!")
            self.current_zombies = int(event[1])
            self.state = "Attacking"  # Create CMD for attacking zombies

    # Call in CMD if state is attacking, *items is a list of items the player is going to use
    def trigger_attack(self, *item):
        player_attack = self.player.get_attack()
        zombies = self.current_zombies
        if len(item) == 2:  # If the player is using two items
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

        # Calculate damage on the player
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

    # DO MOVEMENT INTO ROOM, Call if state is attacking and player wants to run away
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

    def trigger_room_effect(self, room_name):  # Used for the Garden and Kitchen special room effects
        if room_name == "Garden":
            self.player.add_health(1)
            print(f"After ending your turn in the {room_name} you have gained one health")
            self.state = "Moving"
        if room_name == "Kitchen":
            self.player.add_health(1)
            print(f"After ending your turn in the {room_name} you have gained one health")
            self.state = "Moving"

    # If player chooses to cower instead of move to a new room
    def trigger_cower(self):
        if self.can_cower:
            self.player.add_health(3)
            self.dev_cards.pop(0)
            self.state = "Moving"
            print("You cower in fear, gaining 3 health, but lose time with the dev card")
        else:
            return print("Cannot cower during a zombie door attack")

    # Call when player wants to drop an item, and state is dropping item
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

    def choose_door(self, direction):  # used to select where a door will be made during a zombie door attack
        if direction in self.chosen_tile.doors:
            print("Choose a NEW door not an existing one")
            return False
        else:
            self.chosen_tile.doors.append(direction)
            self.current_zombies = 3
            print(f"{self.current_zombies} Zombies have appeared, prepare for battle. Use the attack command to"
                  f" fight or the run command to flee")
            self.state = "Attacking"

    def search_for_totem(self):  # Used to search for a totem in the evil temple, will force the user to draw a dev card
        if self.get_current_tile().name == "Evil Temple":
            if self.player.has_totem:
                print("player already has the totem")
                return
            else:
                self.trigger_dev_card(self.time)
                self.player.found_totem()
        else:
            print("You cannot search for a totem in this room")

    def bury_totem(self):  #
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

    @staticmethod
    def resolve_doors(n, e, s, w):
        doors = []
        if n == 1:
            doors.append(dir.NORTH)
        if e == 1:
            doors.append(dir.EAST)
        if s == 1:
            doors.append(dir.SOUTH)
        if w == 1:
            doors.append(dir.WEST)
        return doors

    def lose_game(self):
        self.state = "Game Over"


class Player:
    def __init__(self, attack=1, health=6, x=16, y=16, has_totem=False):
        self.attack = attack
        self.health = health
        self.x = x  # x Will represent the players position horizontally starts at 16
        self.y = y  # y will represent the players position vertically starts at 16
        self.items = []  # Holds the players items. Can hold 2 items at a time
        self.has_totem = has_totem

    def get_health(self):
        return self.health

    def found_totem(self):
        self.has_totem = True

    def get_attack(self):
        return self.attack

    def set_attack(self, attack):
        self.attack = attack

    def set_health(self, health):
        self.health = health

    def add_health(self, health):
        self.health += health

    def add_attack(self, attack):
        self.attack += attack

    def get_items(self):
        return self.items

    def get_item_charges(self, item):
        for check_item in self.get_items():
            if check_item[0] == item:
                return check_item[1]

    def set_item_charges(self, item, charge):
        for check_item in self.get_items():
            if check_item[0] == item:
                check_item[1] = charge

    def use_item_charge(self, item):
        for check_item in self.get_items():
            if check_item[0] == item:
                check_item[1] -= 1

    def add_item(self, item, charges):
        if len(self.items) < 2:
            self.items.append([item, charges])

    def remove_item(self, item):
        self.items.pop(self.items.index(item))

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


# Development cards for the game. Played when the player moves into the room.
class DevCard:
    def __init__(self, item, charges, event_one, event_two, event_three):
        self.item = item
        self.charges = charges
        self.event_one = event_one
        self.event_two = event_two
        self.event_three = event_three

        if self.charges != "Unlimited":
            int(self.charges)

    def get_event_at_time(self, time):
        if time == 9:
            return self.event_one
        elif time == 10:
            return self.event_two
        elif time == 11:
            return self.event_three

    def get_item(self):
        return self.item

    def get_charges(self):
        return self.charges

    def __str__(self):
        return "Item: {}, Event 1: {}, Event 2: {}, Event 3: {}".format(self.item, self.event_one, self.event_two,
                                                                        self.event_three)


class Tile:
    def __init__(self, name, x=16, y=16, effect=None, doors=None, entrance=None):
        if doors is None:
            doors = []
        self.name = name
        self.x = x  # x will represent the tiles position horizontally
        self.y = y  # y will represent the tiles position vertically
        self.effect = effect
        self.doors = doors
        self.entrance = entrance

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def change_door_position(self, idx, direction):
        self.doors[idx] = direction

    def set_entrance(self, direction):
        self.entrance = direction

    def rotate_entrance(self):
        if self.entrance == dir.NORTH:
            self.set_entrance(dir.EAST)
            return
        if self.entrance == dir.SOUTH:
            self.set_entrance(dir.WEST)
            return
        if self.entrance == dir.EAST:
            self.set_entrance(dir.SOUTH)
            return
        if self.entrance == dir.WEST:
            self.set_entrance(dir.NORTH)
            return

    def rotate_tile(self):  # Will rotate the tile 1 position clockwise
        for door in self.doors:
            if door == dir.NORTH:
                self.change_door_position(self.doors.index(door), dir.EAST)
            if door == dir.EAST:
                self.change_door_position(self.doors.index(door), dir.SOUTH)
            if door == dir.SOUTH:
                self.change_door_position(self.doors.index(door), dir.WEST)
            if door == dir.WEST:
                self.change_door_position(self.doors.index(door), dir.NORTH)


class IndoorTile(Tile):
    def __init__(self, name, effect=None, doors=None, x=16, y=16, entrance=None):
        if doors is None:
            doors = []
        self.type = "Indoor"
        super().__init__(name, x, y, effect, doors, entrance)

    def __repr__(self):
        return f'{self.name}, {self.doors}, {self.type},' \
               f' {self.x}, {self.y}, {self.effect} \n'


class OutdoorTile(Tile):
    def __init__(self, name, effect=None, doors=None, x=16, y=16, entrance=None):
        if doors is None:
            doors = []
        self.type = "Outdoor"
        super().__init__(name, x, y, effect, doors, entrance)

    def __repr__(self):
        return f'{self.name}, {self.doors}, {self.type},' \
               f' {self.x}, {self.y}, {self.effect} \n'


# Possibly working system idk lmao
# class HealthGraph():
#     data = [
#         [Player.get_health, Player.add_turn] # Actually this will break here lmao
#     ]
#
#     def csv_writer(self, data):
#         with open('..\David+Jared\CSV\player_health.csv', 'w', encoding='UTF8', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerows(data)
#
#     def graph_drawing(self):
#         plt.rcParams["figure.figsize"] = [7, 3]
#         plt.rcParams["figure.autolayout"] = True
#         headers = ['Turn', 'Health']
#         df = pd.read_csv('player_health.csv', names=headers)
#         df.set_index('Turn').plot()
#         plt.show()

class Commands(cmd.Cmd):
    intro = 'Welcome to Zombie in My Pocket type "start" to start playing the game, if you need help at any time type ' \
            '"help" or "?". Good Luck '

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.player = Player()
        self.game = Game(self.player)

    # Puts the game into start state
    def do_start(self, line):
        if self.game.state == "Starting":
            self.game.start_game()
            self.game.get_game()
        else:
            print("You are currently playing a game type 'restart' if you want to start again")

    # Add to help file
    @staticmethod
    def help_start():
        print("Type 'start' while seeing the intro")

    # Move to a north tile
    def do_n(self, line):
        if self.game.state == "Moving":
            self.game.select_move(dir.NORTH)
            self.game.get_game()
            self.game.get_player_status()
        else:
            print("You are not currently in Move state")

    # Add to help file
    @staticmethod
    def help_n():
        print("Type 'n' while in the moving state")

    # Move to a south tile
    def do_s(self, line):
        if self.game.state == "Moving":
            self.game.select_move(dir.SOUTH)
            self.game.get_game()
            self.game.get_player_status()
        else:
            print("You are not currently in Move state")

    # Add to help file
    @staticmethod
    def help_s():
        print("Type 's' while in the moving state")

    # Move to a east tile
    def do_e(self, line):
        if self.game.state == "Moving":
            self.game.select_move(dir.EAST)
            self.game.get_game()
            self.game.get_player_status()
        else:
            print("You are not currently in Move state")

    # Add to help file
    @staticmethod
    def help_e():
        print("Type 'e' while in the moving state")

    # Move to a west tile
    def do_w(self, line):
        if self.game.state == "Moving":
            self.game.select_move(dir.WEST)
            self.game.get_game()
            self.game.get_player_status()
        else:
            print("You are not currently in Move state")

    # Add to help file
    @staticmethod
    def help_w():
        print("Type 'w' while in the moving state")

    # Puts player in draw state so player draws a dev card
    def do_draw(self, line):
        if self.game.state == "Drawing Dev Card":
            self.game.trigger_dev_card(self.game.time)
        else:
            print("You are not in the drawing state")

    # Add to help file
    @staticmethod
    def help_draw():
        print("Type 'draw' while in the drawing state")

    # Puts the game into rotate state
    def do_rotate(self, line):
        if self.game.state == "Rotating":
            self.game.rotate()
            self.game.get_game()
        else:
            print("You currently don't have a tile selected to rotate")

    # Add to help file
    @staticmethod
    def help_rotate():
        print("Type 'rotate' while in the rotating state, each time the tile will rotate 90 degrees")

    # Puts the game into place state
    def do_place(self, line):
        if self.game.state == "Rotating":
            if self.game.chosen_tile.name == "Foyer":
                self.game.place_tile(16, 16)
            elif self.game.check_dining_room_has_exit() is False:
                return print("Dining room entrance must face an empty tile")
            else:
                if self.game.get_current_tile().name == "Dining Room" \
                        and self.game.current_move_direction == self.game.get_current_tile().entrance:
                    if self.game.check_entrances_align():
                        self.game.place_tile(self.game.chosen_tile.x, self.game.chosen_tile.y)
                        self.game.move_player(self.game.chosen_tile.x, self.game.chosen_tile.y)
                elif self.game.check_doors_align(self.game.current_move_direction):
                    self.game.place_tile(self.game.chosen_tile.x, self.game.chosen_tile.y)
                    self.game.move_player(self.game.chosen_tile.x, self.game.chosen_tile.y)
                else:
                    print(" Please rotate the tile you are placing until a door lines up with the direction you moved")
            self.game.get_game()
        else:
            print("You currently don't have a tile selected")

    # Add to help file
    @staticmethod
    def help_place():
        print(
            "Type 'place' while in the rotating state, the doors of the new tile must line up with the direction you moved")

    # Select a direction to create a door if tile does not have any
    def do_choose(self, direction):
        dir_choice = ["n", "e", "s", "w"]
        if direction not in dir_choice:
            return print("Invalid input please type 'choose' and one of 'n', 'e', 's', 'w' ")
        if direction == 'n':
            direction = dir.NORTH
        if direction == "e":
            direction = dir.EAST
        if direction == "s":
            direction = dir.SOUTH
        if direction == "w":
            direction = dir.WEST
        if self.game.state == "Choosing Door":
            self.game.can_cower = False
            self.game.choose_door(direction)
        else:
            print("Your cannot create a door in this room")

    # Add to help file
    @staticmethod
    def help_choose():
        print(
            "Type 'choose' and one of 'n', 'e', 's', 'w' while in the Choosing Door state to create a new door in that direction")

    # Calculates players damage taken when attacking zombies
    def do_attack(self, line):
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

    # Add to help file
    @staticmethod
    def help_attack():
        print(
            "Type 'attack' when faced with a group of zombies, the number of zombies minus your attack status will determine how much damage taken")

    # Lets players use items
    def do_use(self, line):
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

    # Add to help file
    @staticmethod
    def help_use():
        print(
            "Type 'use' and the items name when attacking zombies, damage done will be increased and the damage taken will be reduced")

    # Lets players swap items
    def do_swap(self, line):
        if self.game.state == "Swapping Item":
            self.game.drop_item(line)
            self.game.player.add_item(self.game.room_item[0], self.game.room_item[1])
            self.game.room_item = None
            self.game.get_game()

    # Add to help file
    @staticmethod
    def help_swap():
        print(
            "Type 'swap' and the name of the item you want to get rid of when you draw a new item when already carrying two items")

    # Lets players run from zombies
    def do_run(self, direction):
        if self.game.state == "Attacking":
            if direction == 'n':
                self.game.trigger_run(dir.NORTH)
            elif direction == 'e':
                self.game.trigger_run(dir.EAST)
            elif direction == 's':
                self.game.trigger_run(dir.SOUTH)
            elif direction == 'w':
                self.game.trigger_run(dir.WEST)
            else:
                print("Cannot run that direction")
            if len(self.game.get_current_tile().doors) == 1 and self.game.chosen_tile.name != "Foyer":
                self.game.state = "Choosing Door"
                self.game.get_game()
        else:
            print("Cannot run when not being attacked")

    # Add to help file
    @staticmethod
    def help_run():
        print("Type 'run' when faced with a group of zombies, you will return to the room you entered from")

    # Lets players cower from zombies to avoid damage but at the cost of an increase to the time
    def do_cower(self, line):
        if self.game.state == "Moving":
            self.game.trigger_cower()
        else:
            print("You cannot cower if you are not being attacked")

    # Add to help file
    @staticmethod
    def help_cower():
        print(
            "Type 'cower' when faced with a group of zombies, you will hide from the zombies and take not damage but the time of day will increase")

    # Lets players find the totem in the evil temple at the cost of a card
    def do_search(self, line):
        if self.game.state == "Moving":
            self.game.search_for_totem()
        else:
            print("You cannot search for the totem here")

    # Add to help file
    @staticmethod
    def help_search():
        print("Type 'search' when in the Evil Temple, the totem item will be found at the cost of a card")

    # Lets players bury the totem in the graveyard at the cost of a card
    def do_bury(self, line):
        if self.game.state == "Moving":
            self.game.bury_totem()
        else:
            print("You cannot bury for the totem here")

    # Add to help file
    @staticmethod
    def help_bury():
        print("Type 'bury' when in the Graveyard, the totem item will be buried at the cost of a card")

    # Lets player exit the game
    def do_exit(self, line):
        return True

    # Add to help file
    @staticmethod
    def help_exit():
        print("Type 'exit' at any time, the game will close without being saved")

    # Lets player see characters status
    def do_status(self, line):
        if self.game.state != "Game Over":
            self.game.get_player_status()

    # Add to help file
    @staticmethod
    def help_status():
        print(
            "Type 'status' at any time and you will be shown: the time of day, your health points, your attack points, the items you have and the games current state")

    # Not finished yet
    def do_drop(self, item):
        if self.game.state != "Game Over":
            self.game.drop_item(item)
            self.game.get_game()

    # Add to help file
    @staticmethod
    def help_drop():
        print("Type 'drop' and the name of the item, that item will be thrown away")

    #  Restarts the game
    def do_restart(self, line):
        del self.game
        del self.player
        self.player = Player()
        self.game = Game(self.player)

    # Add to help file
    @staticmethod
    def help_restart():
        print("Type 'restart' at any time to start a new game")

    # save game working - Daniel
    def do_save(self, line):
        save_file = line + '.pickle'
        with open(save_file, 'wb') as sg:
            pickle.dump(self.game, sg)
            print("Game Saved")

        if len(self.game.tiles) == 0:
            return print("Please place a tile before saving")

        if not line:
            return print("Please enter a name for the saved game state")

    # Add to help file
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

        if not save:
            return print("Please enter a valid name of a save")

    # Add to help file
    @staticmethod
    def help_load():
        print("Type 'load' and the name of a saved file at any time e.g. 'load sg1', to load your past progress")


if __name__ == "__main__":
    Commands().cmdloop()
