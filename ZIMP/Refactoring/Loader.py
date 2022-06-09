# Split Game.py Loader stuff into here
import random
import pandas as pd
from Directions import Direction
from OutdoorTile import OutdoorTile
from IndoorTile import IndoorTile
from DevCard import DevCard


class Loader:
    def __init__(self, indoor_tiles=None, outdoor_tiles=None, dev_cards=None, chosen_tile=None):
        if indoor_tiles is None:
            indoor_tiles = []
        if outdoor_tiles is None:
            outdoor_tiles = []
        if dev_cards is None:
            dev_cards = []

        self.chosen_tile = chosen_tile
        self.indoor_tiles = indoor_tiles
        self.outdoor_tiles = outdoor_tiles
        self.dev_cards = dev_cards

        # Load tiles from the Excel file, added error checking - Daniel

    def load_tiles(self):
        """ Pre-condition: Game has not started and the file containing the tiles can be loaded
            Post-condition: Games starts and tiles are loaded in """
        try:
            excel_data = pd.read_excel('Tiles.xlsx')
            tiles = []
            for name in excel_data.iterrows():
                tiles.append(name[1].tolist())
            for tile in tiles:
                doors = self.resolve_doors(tile[3], tile[4], tile[5], tile[6])
                if tile[2] == "Outdoor":
                    new_tile = OutdoorTile(tile[0], tile[1], doors)
                    if tile[0] == "Patio":
                        new_tile.set_entrance(Direction.NORTH)
                    self.outdoor_tiles.append(new_tile)
                if tile[2] == "Indoor":
                    new_tile = IndoorTile(tile[0], tile[1], doors)
                    if tile[0] == "Dining Room":
                        new_tile.set_entrance(Direction.NORTH)
                    self.indoor_tiles.append(new_tile)

        except FileNotFoundError as e:
            print("ERROR: File not found please check Excel file name", e)
        except OSError as e:
            print("ERROR: Unable to access file please check file location", e)

        # Load cards from Excel file, added error checking - Daniel

    def load_dev_cards(self):
        """ Pre-condition: Game has not started and the file containing the card can be loaded
            Post-condition: Games starts and cards are loaded in """
        try:
            card_data = pd.read_excel('DevCards.xlsx')
            for card in card_data.iterrows():
                item = card[1][0]
                event_one = (card[1][1], card[1][2])
                event_two = (card[1][3], card[1][4])
                event_three = (card[1][5], card[1][6])
                charges = card[1][7]
                dev_card = DevCard(item, charges, event_one,
                                   event_two, event_three)
                self.dev_cards.append(dev_card)
            random.shuffle(self.dev_cards)
            self.dev_cards.pop(0)
            self.dev_cards.pop(0)

        except FileNotFoundError as e:
            print("ERROR: File not found please check Excel file name", e)
        except OSError as e:
            print("ERROR: Unable to access file please check file location", e)

    @staticmethod
    def resolve_doors(n, e, s, w):
        doors = []
        if n == 1:
            doors.append(Direction.NORTH)
        if e == 1:
            doors.append(Direction.EAST)
        if s == 1:
            doors.append(Direction.SOUTH)
        if w == 1:
            doors.append(Direction.WEST)
        return doors
