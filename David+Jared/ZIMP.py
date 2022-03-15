class Player:
    def __init__(self, name, health=6, attack_score=1, items=[], inventory=[], current_tile=None, previous_tile=None,
                 has_totem=False, time=2100):
        self.inventory = inventory
        self.name = name
        self.hp = health
        self.attack_score = attack_score
        self.items = items
        self.current_tile = current_tile
        self.previous_tile = previous_tile
        self.has_totem = has_totem
        self.game_time = time

    def get_name(self):
        return self.name

    def get_health(self):
        return self.hp

    def get_attack_score(self):
        return self.attack_score

    def get_items(self):
        return self.items

    def get_inventory(self):
        return self.inventory

    def get_current_tile(self):
        return self.current_tile

    def get_previous_tile(self):
        return self.previous_tile

    def get_has_totem(self):
        return self.has_totem

    def get_current_time(self):
        return self.game_time


class Game:
    def __init__(self, dev_cards=[], tile_cards=[]):
        self.dev_cards = dev_cards
        self.tile_cards = tile_cards

    def add_card(self, card):
        if type(card) is TileCard:
            self.tile_cards.append(card)
        elif type(card) is DevCard:
            self.dev_cards.append(card)


the_game = Game()


class Card:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect
        the_game.add_card(self)

    def get_desc(self):
        return self.name + "\nEffect: " + self.effect


class TileCard(Card):
    def __init__(self, x=0, y=0, name="", effect="", doors=[]):
        Card.__init__(self, name, effect)
        self.x = x
        self.y = y
        self.doors = doors

    def get_name(self):
        return self.name

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_door(self, direction):
        door_ref = {"n": 0, "e": 1, "s": 2, "w": 3}.get(direction)
        return self.doors[door_ref]

    def get_doors_string(self):
        return "North = " + str(self.doors[0]) + ", East = " + str(self.doors[1]) + ", South = " + str(
            self.doors[2]) + ", and West = " + str(self.doors[3])

    def set_crds(self, x, y):
        self.x = x
        self.y = y

    def get_desc(self):
        return self.name + " at (" + str(self.x) + ", " + str(self.y) + ")"


class DevCard(Card):
    def __init__(self, identity=0, item="", nine_effect="", ten_effect="", eleven_effect="", num_zombies=0):
        self.id = identity
        self.num_zombies = num_zombies
        self.eleven_effect = eleven_effect
        self.ten_effect = ten_effect
        self.nine_effect = nine_effect
        self.item = item

    def get_desc(self):
        return self.name + "\nItem: " + self.item.get_desc()

    def get_nine_effect(self):
        # the effect that happens at 9pm
        return self.nine_effect

    def get_ten_effect(self):
        # the effect that happens at 10pm
        return self.ten_effect

    def get_eleven_effect(self):
        # the effect that happens at 11pm
        return self.eleven_effect

    def add_item(self, item):
        self.item = item

    def add_zombies(self):
        return self.num_zombies


class Items:
    def __init__(self, name, attack, weapon: bool):
        self.name = name
        self.attack = attack
        self.weapon = weapon
        DevCard.add_item(self)


class GameRules:  # Win / Loss conditions
    def __init__(self, end, win):
        self.loss = end
        self.win = win

    def has_lost(self):
        return self.loss

    def lose_game_hp(self):
        if Player.get_health() == 0:
            print("Player has Lost")
        return self.has_lost()

    def lose_game_time(self):
        if Player.get_current_time() == 2300: # and Shuffled_DevCards == 0
            print("Player has Lost")
        return  self.has_lost()

    def win_game(self):
        if Player.get_current_tile() == TileCard.get_name() and Player.get_has_totem() == True:
            pass
        pass


class Action:
    def __init__(self, fight, run, cower, end_turn):
        self.fight = fight
        self.run = run
        self.cower = cower
        self.end = end_turn

    def fight(self):
        # DevCard.num_zombies - Player.get_attack_score() = Player.get_health()
        pass

    def run(self):
        # Go back to previous location, Player.get_health() - 1
        pass

    def cower(self):
        Player.get_health() + 3
        # Discard Top Dev Card
        return self.cower

    def end_turn(self):
        return self.end

class GameStart:
    pass


class Help:  # for the help command
    pass

def add_tile_cards(args): #X-location, Y-location, Name, Effect, doors[North, East, South, West]
    TileCard(0,0,"Foyer","Nothing",[True,False,False,False]) # add an item somehow for the likes of the Totem
    TileCard(0,0,"Bedroom","Nothing",[True,False,False,True])
    TileCard(0,0,"Dining Room","Ability to go in and out of the house - North side only",[True,True,True,True])
    TileCard(0,0,"Family Room","Nothing",[True,True,False,True])
    TileCard(0,0,"Evil Temple","Has Totem - Use a Development Card to get the Item",[False,True,False,True])
    TileCard(0,0,"Storage","May draw a new Development Card to find an item",[True,False,False,False])
    TileCard(0,0,"Kitchen","+1 Health if ending turn here",[True,True,False,True])
    TileCard(0,0,"Bathroom","Nothing",[True,False,False,False])
    TileCard(0,0,"Yard - 2 White Chairs","Nothing",[False,True,True,True])
    TileCard(0,0,"Yard - Swing set","Nothing",[False,True,True,True])
    TileCard(0,0,"Patio","Ability to go in and out of the house - North side only",[True,True,True,False])
    TileCard(0,0,"Garage","Nothing",[False,False,True,True])
    TileCard(0,0,"Graveyard","Use a new development card to bury totem",[False,True,True,False])
    TileCard(0,0,"Yard - Tree","Nothing",[False,True,True,True])
    TileCard(0,0,"Sitting Area","Nothing",[False,True,True,True])
    TileCard(0,0,"Garden","+1 Health if ending turn here",[False,True,True,True])

def add_dev_card():# name, item, nine_effect, ten_effect, 11_effect, num_zombies
    DevCard(1,"Oil","You try hard not to wet yourself","Item","6 Zombies",num_zombies=6)

def add_items():
    items = {
        'Oil': 'Throw as you run away to avoid taking damage. Combine with candle to kill all zombies on one tile without taking damage. One time use',
        'Gasoline': 'Combine with Candle to kill all zombies without taking damage. Combine with Chainsaw to give two more Chainsaw uses. One time use',
        'Board w/ Nails': 'Add 1 to Attack Score',
        'Can of Soda': 'Add 2 to Health Points',
        'Grisly Femur': 'Add 1 to Attack Score',
        'Golf Club': 'Add 1 to Attack Score',
        'Candle': 'Combine with Oil or Gas to kill all zombies on one tile without taking damage',
        'Chainsaw': 'Add 3 to attack score. Only has enough fuel for two battles',
        # So this means you get +3 for 2 turns unless you give it more gas which means +3 for a total of 4 turns
        'Machete': 'Add 2 to Attack Score'
    }
    Player.get_items(items)


def get_totem(self, use_card):
    if Player.get_current_tile() == TileCard.get_name("Evil Temple"):
        self.use_card = input("You may draw a Development Card. If the Hour you are on has 'ITEM' you may you may pick up the totem" +\
              "\nNote: This will use the development card which loses it. Do you wish to proceed? Y/N:" )
        if self.use_card == "Y":
            pass # Draw Card
        else:
            pass
