import json
import numpy as np
from pandas import array
import colorama
from colorama import Fore, Back, Style
colorama.init()


blank = Back.GREEN + Fore.BLUE + ' ' + Style.RESET_ALL
king_color = Fore.RED + 'K' + Style.RESET_ALL


class Building:
    tag = 1

    def __init__(self, x, y, width, height, color, health, village, char, damage):
        self.id = self.tag

        self.type = "building"
        self.height = width
        self.width = height
        self.x = x
        self.y = y
        self.input_array = []
        self.grid = village.grid
        self.village = village
        self.color = color
        self.health = health
        self.max_health = health
        self.char = char
        self.building_list = []
        self.defence_list = []
        self.wall = []
        self.damage = damage
        self.color_reset = Style.RESET_ALL
        Building.tag += 1

    def reduce_health(self, damage):
        self.health -= damage
        self.village.display(self)

    def take_damage(self, village, damage):
        self.health = self.health - damage
        village.display(self)


class TownHall(Building):
    def __init__(self, x, y, village):
        super().__init__(x, y, 4, 3, Fore.WHITE + Back.BLACK, 100, village, "T", 0)


class Huts(Building):
    def __init__(self, x, y, village):
        super().__init__(x, y, 2, 2, Fore.WHITE + Back.BLACK, 100, village, "H", 0)


class Cannons(Building):
    def __init__(self, x, y, village):
        super().__init__(x, y, 2, 2, Fore.WHITE + Back.BLACK, 50, village, "C", 10)

    def cannon_shoot(self, village):
        if(self.health >= 0):
            for i in range(max(self.x-5, 0), min(self.x+6+2, village.length-1)):
                for j in range(max(self.y-5, 0), min(self.y+5, village.width-1)):
                    if village.back_grid[j][i] < 0:
                        trp = village.get_troop(i, j)
                        if trp != None:
                            trp.take_damage(village, self.damage)
                        village.turn_white(self)
                        return
            village.display(self)


class Wizards(Building):
    def __init__(self, x, y, village):
        super().__init__(x, y, 2, 2, Fore.WHITE + Back.BLACK, 50, village, "W", 10)

    def wizard_shoot(self, village):
        if(self.health >= 0):
            for i in range(max(self.x-5, 0), min(self.x+6+2, village.length-1)):
                for j in range(max(self.y-5, 0), min(self.y+5, village.width-1)):
                    if village.back_grid[j][i] < 0:
                        trp = village.get_troop(i, j)
                        if trp != None:
                            self.lattack_wiz(village, trp, self.damage)
                        village.turn_white(self)
                        return
            village.display(self)

    def lattack_wiz(self, village, trp, damage):
        x = trp.x
        y = trp.y
        t = []
        w= []
        print("lattacking")
        for i in range(x-3, x+4):
            for j in range(y-3, y+4):
                if village.back_grid[j][i] < 0:
                    t.append(village.get_troop(i, j))
                unique_troops = set(t)


        for i in unique_troops:
            if i != None:
                print(i)
                i.take_damage(village, damage)


class Walls(Building):
    def __init__(self, x, y, village):
        super().__init__(x, y, 1, 1, Fore.WHITE + Back.RED, 100, village, "#", 0)
