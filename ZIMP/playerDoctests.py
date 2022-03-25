class Player:
    def __init__(self, attack=1, health=6, x=16, y=16, has_totem=False):
        self.attack = attack
        self.health = health
        self.x = x
        self.y = y
        self.items = []
        self.has_totem = has_totem

    def get_health(self) -> int:
        """Get player's health
        >>> player = Player("Player")
        >>> player.get_health()
        6
        """
        return self.health

    def set_health_increase(self, total_health: int) -> None:
        """Test increasing player's health
        >>> player = Player("Player")
        >>> player.set_health(7)
        >>> player.get_health()
        7
        """
        self.health = total_health

    def set_health(self, lost_health: int) -> None:
        """Test decreasing player's health
        >>> player = Player("Player")
        >>> player.set_health(1)
        >>> player.get_health()
        1
        """
        self.health = lost_health

    def get_attack(self) -> int:
        """Get player's attack
        >>> player = Player("Player")
        >>> player.get_attack()
        1
        """
        self.attack = 1
        return self.attack

    def set_attack(self, total_attack: int) -> None:
        """Test increasing player's atttack
        >>> player = Player("Player")
        >>> player.set_attack(2)
        >>> player.get_attack()
        2
        """
        self.attack = total_attack

    def get_player_x(self):
        """Check player's x position
        >>> player = Player("Player")
        >>> player.x
        16"""
        return self.x

    def set_x(self, new_x: int) -> None:
        """Test decreasing player's health
        >>> player = Player("Player")
        >>> player.set_x(17)
        >>> player.get_player_x()
        17
        """
        self.x = new_x

    def get_player_y(self):
        """Check player's x position
        >>> player = Player("Player")
        >>> player.y
        16"""
        return self.y

    def set_y(self, new_y: int) -> None:
        """Test decreasing player's health
        >>> player = Player("Player")
        >>> player.set_y(17)
        >>> player.get_player_y()
        17
        """
        self.y = new_y

    def get_has_totem(self) -> bool:
        """Boolean that holds true or false if player has totem
        >>> player = Player("Test")
        >>> player.has_totem
        False
        """
        return self.has_totem

    def found_totem(self) -> bool:
        """Player has the totem
        >>> player = Player("Test")
        >>> player.found_totem()
        True
        """
        self.has_totem = True
        return self.has_totem

    def get_items(self) -> []:
        """Array that holds list of player's items
        >>> player = Player("Test")
        >>> player.get_items()
        []
        """
        return self.items

    def add_item(self) -> []:
        """Add an item to inventory
        >>> player = Player("Test")
        >>> player.add_item()
        [] """
        return self.items

    def remove_item(self) -> None:
        """Test remove an item from inventory
        >>> player = Player("Test")
        >>> player.remove_item()
        [] """
        return self.items
