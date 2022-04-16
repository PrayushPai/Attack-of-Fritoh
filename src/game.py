import os
import numpy as np
from pandas import array
import colorama
from colorama import Fore, Back, Style
colorama.init()


class Village():
    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.buildings = []
        self.defence = []
        self.walls = []
        self.min_dist = []
        self.direction = []
        self.troops = []
        self.level = 1
        self.main_troops = 4 + self.level*2

    def place_troop(self, troop):
        self.troops.append(troop)
        for i in range(troop.height):
            for j in range(troop.width):
                self.grid[troop.y+i][troop.x+j] = Back.BLACK + \
                    Fore.WHITE + troop.char + Style.RESET_ALL
                self.back_grid[troop.y+i][troop.x+j] = troop.id

    def init_grid(self):
        self.grid = [[" " for x in range(self.length)]
                     for y in range(self.width)]
        self.back_grid = [[0 for x in range(self.length)]
                          for y in range(self.width)]

    def make_border(self, grid):
        for i in range(self.length):
            for j in range(self.width):
                self.grid[j][i] = Back.GREEN + Fore.BLUE + ' '+Style.RESET_ALL
        for i in range(self.length):
            self.grid[0][i] = Fore.BLUE+'█'+Style.RESET_ALL
            self.grid[self.width-1][i] = Fore.BLUE+'█'+Style.RESET_ALL
        for i in range(self.width):
            self.grid[i][0] = Fore.BLUE+'██'+Style.RESET_ALL
            self.grid[i][self.length-1] = Fore.BLUE + '██'+Style.RESET_ALL

    def print_grid(self):
        # print('\033[1;1H', end="")
        os.system('clear')
        for i in range(self.width):
            for j in range(self.length):
                print(self.grid[i][j], end='')
            print("")

    def add_building(self, building):
        for i in range(building.height):
            for j in range(building.width):
                self.grid[building.y+i][building.x+j] = Back.BLACK + \
                    Fore.WHITE + building.char + Style.RESET_ALL
                self.back_grid[building.y+i][building.x+j] = building.id
        if(building.char != '#'):
            self.buildings.append(building)
        if(building.char == 'M' or building.char == 'C'):
            self.defence.append(building)
        if(building.char == '#'):
            self.walls.append(building)
        self.min_dist = self.make_grid()

    def display(self, building):
        if(building.health >= 0.5 * building.max_health):
            for i in range(building.height):
                for j in range(building.width):
                    self.grid[building.y+i][building.x+j] = Back.BLACK + Fore.WHITE + \
                        building.char + Style.RESET_ALL
                    self.back_grid[building.y+i][building.x+j] = building.id

        elif(building.health >= 0.2*building.max_health and building.health < 0.5*building.max_health):
            for i in range(building.height):
                for j in range(building.width):
                    self.grid[building.y+i][building.x+j] = Back.LIGHTYELLOW_EX + Fore.WHITE + \
                        building.char + Style.RESET_ALL
                    self.back_grid[building.y+i][building.x+j] = building.id

        elif(building.health >= 0.1*building.max_health and building.health < 0.2*building.max_health):
            for i in range(building.height):
                for j in range(building.width):
                    self.grid[building.y+i][building.x+j] = Back.RED + Fore.WHITE + \
                        building.char + Style.RESET_ALL
                    self.back_grid[building.y+i][building.x+j] = building.id

        elif(building.health <= 0.1*building.max_health and building.health > 0):
            for i in range(building.height):
                for j in range(building.width):
                    self.grid[building.y+i][building.x+j] = Back.WHITE + Fore.BLUE + \
                        building.char + Style.RESET_ALL
                    self.back_grid[building.y+i][building.x+j] = building.id

        elif(building.health <= 0):
            self.remove_building(building)
            

        self.min_dist = self.make_grid()

    def remove_building(self, building):
        for i in range(building.height):
                for j in range(building.width):
                    self.grid[building.y + i][building.x +
                                              j] = Back.GREEN + Fore.BLUE + " " + Style.RESET_ALL
                    self.back_grid[building.y + i][building.x+j] = 0

        for i in range(len(self.buildings)):
            if self.buildings[i].id == building.id:
                self.buildings.pop(i)
                break

    def make_grid(self):
        grid = []
        self.direction = []
        for i in range(self.width):
            grid.append([])
            self.direction.append([])
            for j in range(self.length):
                grid[i].append(5000)
                self.direction[i].append((0, 0))
        for x in range(self.width):
            for y in range(self.length):
                if self.back_grid[x][y] <= 0:
                    continue
                if self.back_grid[x][y] > 8:
                    continue
                for i in range(self.width):
                    for j in range(self.length):
                        if grid[i][j] > abs(x-i)+abs(y-j):
                            grid[i][j] = abs(x-i)+abs(y-j)
                            self.direction[i][j] = ((y-j, x-i))
        return grid

    def add_troop(self, troop):
            self.troops.append(troop)

            self.grid[troop.y][troop.x] = Back.BLACK + \
                Fore.WHITE + troop.char + Style.RESET_ALL
            self.back_grid[troop.y][troop.x] = troop.id

    def remove_troop(self, troop):

        self.grid[troop.y][troop.x] = Back.GREEN + \
            Fore.BLUE + ' '+Style.RESET_ALL
        self.back_grid[troop.y][troop.x] = 0
        for i in range(len(self.troops)):
            if self.troops[i].id == troop.id:
                self.troops.pop(i)
                break

    # funtinon to get building by building id
    def get_building(self, x, y):
        id = self.back_grid[y][x]
        for i in range(len(self.buildings)):
            if self.buildings[i].id == id:
                return self.buildings[i]
        return None

    def get_wall(self, x,y):
        id = self.back_grid[y][x]
        for i in range(len(self.walls)):
            if self.walls[i].id == id:
                return self.walls[i]
        return None

    # function to get troop by troop id
    def get_troop(self, x, y):
        id = self.back_grid[y][x]
        for i in range(len(self.troops)):
            if self.troops[i].id == id:
                return self.troops[i]
        return None

    def turn_white(self, building):
        for i in range(building.height):
            for j in range(building.width):
                self.grid[building.y+i][building.x+j] = Back.WHITE + Fore.BLUE + \
                    building.char + Style.RESET_ALL
                self.back_grid[building.y+i][building.x+j] = building.id
