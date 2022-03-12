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

    def rotate(self, num_quarter_turns=1):
        pass

    def get_desc(self):
        return self.name + " at (" + str(self.x) + ", " + str(self.y) + ")"


class DevCard(Card):
    def __init__(self, name, effect, item, nine_effect, ten_effect, eleven_effect, num_zombies):
        # key for effects is Z = Zombies, D = take 1 dmg, I = Get Item
        Card.__init__(self, name, effect)
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
