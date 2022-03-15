import random
# deck shuffling
import cmd
# Output
import time
# Timer

# Todo add functionality to the Help Command - Use CMD
# Todo - add more DevCards
# Todo add a game loader
# Todo add a game saver
# Todo add a json reader - for Game Saver most likely
# Todo add play space
# Todo add Dev Card shuffling
# Todo add Dev Card drawing/pulling/using
# Todo add combat

class Player:
    def __init__(self, name, health=6, attack_score=1, items=[], inventory=[], current_tile=None, previous_tile=None, has_totem=False, time=2100, loaded=False, saved=False ,turns=0):
        self.inventory = inventory
        self.name = name
        self.hp = health
        self.attack_score = attack_score
        self.items = items
        self.current_tile = current_tile
        self.previous_tile = previous_tile
        self.has_totem = has_totem
        self.game_time = time
        self.loaded = loaded
        self.saved = saved
        self.turns = turns

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

    def has_loaded(self):
        return self.loaded

    def has_saved(self):
        return self.saved

    def add_turn(self):
        return self.turns+1


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
    def __init__(self, fight, run, cower, end_turn, start_turn, move, use_items):
        self.fight = fight
        self.run = run
        self.cower = cower
        self.end = end_turn
        self.start = start_turn
        self.move = move
        self.use_items = use_items

    def start(self): # Starting turn
        print("Action List: \nM: Move\nC: Cower")
        if input("Which action would you like to perform? [M/C]") == "M":
            return self.move
        else:
            return self.cower
    
    def move(self):
        print("Possible movement locations for " + Player.get_current_tile + " tile: ") # Todo Display Doors here
        input("What direction would you like to move"+ {} +": ") # Valid movement points
        # if moved direction has zombies - Action Text for Fight, Run, Cower, UseItems
        return self.move

    def fight(self):
        # DevCard.num_zombies - Player.get_attack_score() = Player.get_health()
        pass

    def run(self):
        Player.get_current_tile = Player.get_previous_tile
        Player.get_health - 1
        return self.end

    def cower(self):
        Player.get_health() + 3
        # Discard Top Dev Card
        return self.cower

    def use_items(self):
        pass

    def end(self):
        Player.add_turn
        return self.end

class GameStart:
    if Player.get_current_time != 2100 and Player.has_loaded == False: # setting the game to 9pm when the player starts a new game
        Player.get_current_time = 2100

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
    DevCard(1,"Oil","You try hard not to wet yourself","Item","6 Zombies",6)
    DevCard(2,"Gasoline","4 Zombies","You sense your impending doom. -1hp","ITEM",4) #-1 HP
    DevCard(3,"Board with Nails","ITEM","4 Zombies","Something icky in your mouth. -1hp",4)
    DevCard(4,"Machete","4 zombies","A bat pooped in your eye. -1hp","6 zombies") # If statement needed for the zombies here
    DevCard(5,"Grisly Femus","ITEM","5 Zombies","Your soul isn't wanted here. -1hp",5)
    DevCard(6,"Golf Club","Slip on nasty goo. -1hp","4 Zombies","The smell of blood is in the air",4)
    DevCard(7,"Chainsaw", "3 Zombies","You hear terrible screams", "5 Zombies") # If statement needed for the zombies here
    DevCard(8,"Can of Soda","Candybar in your pocket. +1hp","ITEM","4 zombies",4)
    DevCard(9,"Candle","Your whole body shivers involuntarily","You feel a spark of Hope. +1hp","4 Zombies",4)

def add_items(): # name, attack score, weapon(T/F), desc, usable(t/f), use_count
    Items("Oil", 0, False, "Throw as you run away to avoid taking damage. COMBIE with candle to kill all zombies on one tile without taking damage. One time use", True, 1)
    Items("Gasoline",0,False,"COMBIE with Candle to kill all zombies without taking damage. COMBIE with Chainsaw to give two more Chainsaw uses. One time use",True,1)
    Items("Board with Nails", 1, True,"+1 Attack Score")
    Items("Can of Soda", 0,False,"Add 2 to Health Points",True, 1)
    Items("Grisly Femur",1,True,"+1 to Attack Score")
    Items("Golf Club",1,True,"+1 to Attack Score")
    Items("Candle",0,False,"COMBIE with Oil or Gasoline to kill all zombies on ONE tile without taking Damage")
    Items("Chainsaw",3,True,"+3 to Attack Score - Only has enough Fuel for 2 battles -- COMBIE with Gasoline for two more uses")
    Items("Machete",2,True,"+2 Attack Score")


def get_totem(self, use_card):
    if Player.get_current_tile() == TileCard.get_name("Evil Temple"):
        self.use_card = input("You may draw a Development Card. If the Hour you are on has 'ITEM' you may you may pick up the totem" +\
              "\nNote: This will use the development card which loses it. Do you wish to proceed? Y/N:" )
        if self.use_card == "Y":
            pass # Draw Card
        else:
            pass

def load_game():
    Player.has_loaded == True

def save_game():
    if Player.has_saved == False:
        t = 120
        while t:
            mins, secs = divmod(t, 120)
            timer = '{:02d}:{:02d}'.format(mins,secs)
            timer
            time.sleep(1)
            t -= 1
        if t == 0:
            print("You have not saved in a 2 minutes. Please do save :)")
    pass

def json_reader():
    pass