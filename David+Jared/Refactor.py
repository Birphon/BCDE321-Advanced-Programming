class Game:
    def __init__(self, player, time=2100, indoor_tiles=None, outdoor_tiles=None, dev_cards=None, game_map=None, chosen_tile=None,state="Start",current_move_direction=None,can_cower=True):
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
        
        # The below makes empty arrays if there is no usable's for the specific name -- Taken from Alec and Cameron's code, had something similar but wasn't working
        
        if indoor_tiles is None:
            indoor_tiles = []
        if outdoor_tiles is None:
            outdoor_tiles = []
        if dev_cards is None:
            dev_cards = []
        if game_map is None:
            game_map = []
    
    # Alec and Cameron's code
    def starting_game(self):
        self.load_tiles()
        self.load_dev_cards()
        for tile in self.indoor_tiles:
            if tile.name == 'Foyer':
                self.chosen_tile = tile
                self.state = "Rotating"
                break
    
    # Alec and Cameron's code
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
                    new_tile.set_entrance(d.NORTH)
                self.outdoor_tiles.append(new_tile)
            if tile[2] == "Indoor":
                new_tile = IndoorTile(tile[0], tile[1], doors)
                if tile[0] == "Dining Room":
                    new_tile.set_entrance(d.NORTH)
                self.indoor_tiles.append(new_tile)
    
    def player_info(self):
        pass
    
    def get_time(self):
        return self.time
    
    