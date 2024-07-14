import numpy as np  # type: ignore
from tcod.console import Console

import tile_types

from creature import Creature
from item import Item

from misc import all_of_type

class GameMap:
    def __init__(self, width: int, height: int, tiles=[], creatures=[], items=[]):
        self.width, self.height = width, height
        self.tiles = tiles

        self.visible = np.full((width, height), fill_value=False, order="F")  # Tiles the player can currently see
        self.explored = np.full((width, height), fill_value=False, order="F")  # Tiles the player has seen before

        entities = creatures + items

        self.entities = entities

    def in_bounds(self, x: int, y: int) -> bool:
        """Return True if x and y are inside of the bounds of this map."""
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = np.select(
            condlist=[self.visible, self.explored],
            choicelist=[self.tiles["light"], self.tiles["dark"]],
            default=tile_types.SHROUD
        )
        for entity in all_of_type(Creature, self.entities) + all_of_type(Item, self.entities):
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, entity.color)

    def get_creature_at(self, x, y):
        for creature in all_of_type(Creature, self.entities):
            if (creature.x, creature.y) == (x,y):
                return creature
        return None

    def get_item_at(self, x, y):
        for item in all_of_type(Item, self.entities):
            if (item.x, item.y) == (x,y):
                return item
        return None