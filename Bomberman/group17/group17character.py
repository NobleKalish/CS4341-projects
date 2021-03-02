# This is necessary to find the main code
import sys

sys.path.insert(0, '../bomberman')
# Import necessary stuff
from Bomberman.bomberman.entity import CharacterEntity
from colorama import Fore, Back


class Group17Character(CharacterEntity):
    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, avatar, x, y, variant):
        super().__init__(name, avatar, x, y)
        # Max search depth
        self.variant = variant
        self.variant_solutions = {
            1: self.variant1,
            2: self.variant2,
            3: self.variant3,
            4: self.variant4,
            5: self.variant5
        }

    def do(self, wrld):
        func = self.variant_solutions.get(self.variant)
        func()

    def variant1(self):
        print("HI")
        pass

    def variant2(self):
        pass

    def variant3(self):
        pass

    def variant4(self):
        pass

    def variant5(self):
        pass
