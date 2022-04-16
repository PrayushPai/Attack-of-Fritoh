import json
from torch import grid_sampler
import numpy as np
from pandas import array
import colorama
from colorama import Fore, Back, Style
from src.buildings import *
colorama.init()

wally = Fore.BLACK + Back.RED + '#' + Style.RESET_ALL
blank = Back.GREEN + Fore.BLUE + ' ' + Style.RESET_ALL


class Troop:
    value_trp = -1

    def __init__(self, x, y, health, village, char, damage):
        self.type = "characters"
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.id = self.value_trp
        self.village = village
        self.char = char
        self.last_move = 'w'
        self.damage = damage
        self.color_reset = Style.RESET_ALL
        Troop.value_trp -= 1

        self.color = Back.RED + Fore.WHITE

    def attack(self, x_attack, y_attack, damage, village):
        building = village.get_building(y_attack, x_attack)
        wall = village.get_wall(y_attack, x_attack)
        print(building)
        if building != None:
            building.take_damage(village, damage)
        else:
            if wall != None:
                wall.take_damage(village, damage)

    

        

    def attack_king(self, x_attack, y_attack, damage, village):
        building = village.get_building(x_attack, y_attack)
        print(building)
        if building != None:
            building.take_damage(village, damage)

    def take_damage(self, village, damage):
        self.health -= damage
        self.village.add_troop(self)


class king(Troop):
    def __init__(self, x, y, village1):
        super().__init__(x, y, 100, village1, 'K', 10)
        self.axe = 0

    def move(self, move, village):
        village.remove_troop(self)
        self.last_move = move
        if move == 'a':
            if self.x > 0:
                # check if there is a building in the way
                if village.back_grid[self.y][self.x-1] == 0:
                    self.x -= 1

        elif move == 'd':
            if self.x < village.length - 1:
                # check if there is a building in the way
                if village.back_grid[self.y][self.x+1] == 0:
                    self.x += 1

        elif move == 'w':
            if self.y > 0:
                # check if there is a building in the way
                if village.back_grid[self.y-1][self.x] == 0:
                    self.y -= 1

        elif move == 's':
            if self.x < village.width - 1:
                # check if there is a building in the way
                if village.back_grid[self.y+1][self.x] == 0:
                    self.y += 1

        if self.axe % 2 == 1:
            self.char = 'A'
        else:
            self.char = 'K'

        village.add_troop(self)

    def attack_normal(self, village):
        if (self.char == 'A'):
            self.lattack(self.village)
        else:
            x_attack = self.x
            y_attack = self.y
            if self.last_move == 'w':
                if self.x > 0:
                    x_attack = self.x
                    y_attack = self.y - 1
            elif self.last_move == 's':
                if self.x < village.width - 1:
                    x_attack = self.x
                    y_attack = self.y + 1
            elif self.last_move == 'a':
                if self.y > 0:
                    x_attack = self.x - 1
                    y_attack = self.y
            elif self.last_move == 'd':
                if self.y < village.length - 1:
                    x_attack = self.x + 1
                    y_attack = self.y

            self.attack_king(x_attack, y_attack, self.damage, village)

    # def move_down_2(self):
    #     x1 = self.x
    #     y1 = self.y
    #     if self.grid[self.y+1][self.x] == wally:
    #         self.y += 2
    #         self.grid[y1][x1] = blank
    #         self.grid[self.y][self.x] = self.color+'K'+Style.RESET_ALL
    #     return self.grid

    # def move_up_2(self):
    #     x1 = self.x
    #     y1 = self.y
    #     if self.grid[self.y-1][self.x] == wally:
    #         self.y -= 2
    #         self.grid[y1][x1] = blank
    #         self.grid[self.y][self.x] = self.color+'K'+Style.RESET_ALL
    #     return self.grid

    # def move_right_2(self):
    #     x1 = self.x
    #     y1 = self.y
    #     if self.grid[self.y][self.x+1] == wally:
    #         self.x += 2
    #         self.grid[y1][x1] = blank
    #         self.grid[self.y][self.x] = self.color+'K'+Style.RESET_ALL
    #     return self.grid

    # def move_left_2(self):
    #     x1 = self.x
    #     y1 = self.y
    #     if self.grid[self.y][self.x-1] == wally:
    #         self.x -= 2
    #         self.grid[y1][x1] = blank
    #         self.grid[self.y][self.x] = self.color+'K'+Style.RESET_ALL
    #     return self.grid

    def king_health_bar(self):
        print("King's health: ", self.health)
        status = ""
        for i in range(int(self.health/10)):
            if i < 2:
                status += Fore.RED + '██'
            elif i < 5:
                status += Fore.LIGHTYELLOW_EX + '██'
            else:
                status += Fore.GREEN + '██'
        print(status)
        print("King's Damage: ", self.damage)

    def get_damage(self):
        return self.damage

    def reduce_health(self, damage):
        self.health -= damage
        return self.king_health_bar()

    def king_dies(self, input_array):
        if self.health <= 0:
            # self.grid[self.y][self.x] = 'DEATH'
            print("King's health: 0")
            print("Game over")
            # input_file = input('Save game as: ')
            # with open(input_file + '.json', 'w') as outfile:
            #     json.dump(input_array, outfile)
            # exit()

    def lattack(self, village):
        b = []
        w= []
        print("lattacking")
        for i in range(self.x-4, self.x+5):
            for j in range(self.y-4, self.y+5):
                if village.back_grid[j][i] > 0:
                    b.append(village.get_building(i, j))
                    w.append(village.get_wall(i,j))
                unique_building = set(b)
                unique_walls = set(w)

        for i in unique_building:
            if i != None:
                i.take_damage(village, self.damage)
        for i in unique_walls:
            if i != None:
                i.take_damage(village, self.damage)

    def health_inc(self):
        self.health = 1.5 * self.health
        return self.king_health_bar()

    def rage(self):
        self.damage = 2 * self.damage
        return self.king_health_bar()


class Barbarian(Troop):
    def __init__(self, x, y, village1):
        super().__init__(x, y, 100, village1, 'B', 10)

    def move(self, village):
        village.remove_troop(self)
        x_dir = village.direction[self.y][self.x][0]
        y_dir = village.direction[self.y][self.x][1]
        x_change = 0
        y_change = 0
        if x_dir == 0:
            if(y_dir > 0):
                y_change = 1
            else:
                y_change = -1
        elif y_dir == 0:
            if(x_dir > 0):
                x_change = 1
            else:
                x_change = -1
        else:
            if(x_dir > 0):
                x_change = 1
            else:
                x_change = -1
        self.final_x = self.x + x_change
        self.final_y = self.y + y_change
        if village.back_grid[self.y+y_change][self.x+x_change] == 0:
            self.x += x_change
            self.y += y_change
        else:
            self.attack(self.y+y_change, self.x+x_change, self.damage, village)
        village.add_troop(self)


class Archer(Troop):
    def __init__(self, x, y, village1):
        super().__init__(x, y, 100, village1, '/', 10)

    def move(self, village):
        village.remove_troop(self)
        x_dir = village.direction[self.y][self.x][0]
        y_dir = village.direction[self.y][self.x][1]
        x_change = 0
        y_change = 0
        y_attack= 0
        x_attack=0
        if x_dir == 0:
            if(y_dir > 0):
                y_change = 1
                y_attack = 5
            else:
                y_change = -1
                y_attack = -5
        elif y_dir == 0:
            if(x_dir > 0):
                x_change = 1
                x_attack = 5
            else:
                x_change = -1
                x_attack = -5
        else:
            if(x_dir > 0):
                x_change = 1
                x_attack = 5
            else:
                x_change = -1
                x_attack = -5
        self.final_x = self.x + x_change
        self.final_y = self.y + y_change
    
        tag = self.searching(village)
        if(tag == 0):
            if village.back_grid[self.y+y_change][self.x+x_change] == 0:
                self.x += x_change
                self.y += y_change
        else:
            self.lattack_archer(village)
            tag = 0
        village.add_troop(self)

    def searching(self, village):
        print("searching")
        tag = 0
        for i in range(self.x-3, self.x+3):
            for j in range(self.y-3, self.x+3):
                if village.back_grid[j][i] > 0 :
                    tag =1
        return tag
                


    def lattack_archer(self, village):
        b = []
        w = []
        print("lattacking")
        for i in range(self.x-4, self.x+5):
            for j in range(self.y-4, self.y+5):
                if village.back_grid[j][i] > 0:
                    b.append(village.get_building(i, j))
        
        for i in range(self.x-4, self.x+4):
            for j in range(self.y-4, self.y+4):
                if village.back_grid[j][i] >0:
                    w.append(village.get_wall(i,j))

        
        build_dam = self.min_dist_build(village, b)
        wall_dam  = self.min_dist_build(village, w)
        print(build_dam)
        print(wall_dam)
        if build_dam != None:
            build_dam.take_damage(village, self.damage)
        elif wall_dam != None:
            wall_dam.take_damage(village, self.damage)
        


    def min_dist_build(self, village, b):
        min_dist = 100
        close_b = None
        for i in b:
            if i != None:
                dist = abs(self.x - i.x) + abs(self.y - i.y)
                if dist < min_dist:
                    min_dist = dist
                    close_b = i                
        return close_b

    def dist_building(self, village, b):
        min_dist = 100
        for i in b:
            if i != None:
                dist = abs(self.x - i.x) + abs(self.y - i.y)
                if dist < min_dist:
                    min_dist = dist
        return min_dist


class queen(Troop):
    def __init__(self, x, y, village1):
        super().__init__(x, y, 100, village1, 'K', 5)
        self.axe = 0

    def move(self, move, village):
        village.remove_troop(self)
        self.last_move = move
        if move == 'a':
            if self.x > 0:
                # check if there is a building in the way
                if village.back_grid[self.y][self.x-1] == 0:
                    self.x -= 1

        elif move == 'd':
            if self.x < village.length - 1:
                # check if there is a building in the way
                if village.back_grid[self.y][self.x+1] == 0:
                    self.x += 1

        elif move == 'w':
            if self.y > 0:
                # check if there is a building in the way
                if village.back_grid[self.y-1][self.x] == 0:
                    self.y -= 1

        elif move == 's':
            if self.x < village.width - 1:
                # check if there is a building in the way
                if village.back_grid[self.y+1][self.x] == 0:
                    self.y += 1

        if self.axe % 2 == 1:
            self.char = 'P'
        else:
            self.char = 'Q'

        village.add_troop(self)

    def attack_normal(self, village):
        x_attack = self.x
        y_attack = self.y
        if self.last_move == 'w':
            if self.x > 0:
                x_attack = self.x
                y_attack = self.y - 5
        elif self.last_move == 's':
            if self.x < village.width - 5:
                x_attack = self.x
                y_attack = self.y + 5
        elif self.last_move == 'a':
            if self.y > 0:
                x_attack = self.x - 5
                y_attack = self.y
        elif self.last_move == 'd':
            if self.y < village.length - 5:
                x_attack = self.x + 5
                y_attack = self.y
        if (self.char == "Q"):
            self.lattack_queen(x_attack, y_attack, village)
        else:
            self.lattack(x_attack, y_attack, village)

    def king_health_bar(self):
        print("Queens's health: ", self.health/2)
        status = ""
        for i in range(int(self.health/10)):
            if i < 2:
                status += Fore.RED + '██'
            elif i < 5:
                status += Fore.LIGHTYELLOW_EX + '██'
            else:
                status += Fore.GREEN + '██'
        print(status)
        print("Queen's Damage: ", self.damage)

    def get_damage(self):
        return self.damage

    def reduce_health(self, damage):
        self.health -= damage
        return self.king_health_bar()

    def king_dies(self, input_array):
        if self.health <= 0:
            # self.grid[self.y][self.x] = 'DEATH'
            print("King's health: 0")
            print("Game over")
            # input_file = input('Save game as: ')
            # with open(input_file + '.json', 'w') as outfile:
            #     json.dump(input_array, outfile)
            # exit()

    def lattack_queen(self,x,y, village):

        b = []
        w= []
        print("lattacking")
        for i in range(x-4, x+5):
            for j in range(y-4, y+5):
                if village.back_grid[j][i] > 0:
                    b.append(village.get_building(i, j))
                    w.append(village.get_wall(i,j))
                unique_building = set(b)
                unique_walls = set(w)

        for i in unique_building:
            if i != None:
                print(i)
                i.take_damage(village, self.damage)
        for i in unique_walls:
            if i != None:
                print(i)
                i.take_damage(village, self.damage)

    def lattack(self,x,y, village):
        
        b = []
        w= []
        print("lattacking")
        for i in range(x-7, x+8):
            for j in range(y-7, y+8):
                if village.back_grid[j][i] > 0:
                    b.append(village.get_building(i, j))
                    w.append(village.get_wall(i,j))
                unique_building = set(b)
                unique_walls = set(w)

        for i in unique_building:
            if i != None:
                print(i)
                i.take_damage(village, self.damage)
        for i in unique_walls:
            if i != None:
                print(i)
                i.take_damage(village, self.damage)

    def health_inc(self):
        self.health = 1.5 * self.health
        return self.king_health_bar()

    def rage(self):
        self.damage = 2 * self.damage
        return self.king_health_bar()


class Barbarian(Troop):
    def __init__(self, x, y, village1):
        super().__init__(x, y, 100, village1, 'B', 10)

    def move(self, village):
        village.remove_troop(self)
        x_dir = village.direction[self.y][self.x][0]
        y_dir = village.direction[self.y][self.x][1]
        x_change = 0
        y_change = 0
        if x_dir == 0:
            if(y_dir > 0):
                y_change = 1
            else:
                y_change = -1
        elif y_dir == 0:
            if(x_dir > 0):
                x_change = 1
            else:
                x_change = -1
        else:
            if(x_dir > 0):
                x_change = 1
            else:
                x_change = -1
        self.final_x = self.x + x_change
        self.final_y = self.y + y_change
        if village.back_grid[self.y+y_change][self.x+x_change] == 0:
            self.x += x_change
            self.y += y_change
        else:
            self.attack(self.y+y_change, self.x+x_change, self.damage, village)
        village.add_troop(self)
