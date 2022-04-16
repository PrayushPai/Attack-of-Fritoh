import json
import time
import os
import numpy as np
from pandas import array
import colorama
from src.buildings import *
from colorama import Fore, Back, Style
from src.game import *
from src.king import *
from src.input import *
colorama.init()

input_array = []
os.system('stty echo')
level = input("Enter Level you wish to play (1-3): ")
input_array.append(level)
if (level== '2'):
    

    village = Village(100, 45)
    village.init_grid()
    village.make_border(village.grid)

    townhall1 = TownHall(60, 25, village)

    hut1 = Huts(40, 17, village)
    hut2 = Huts(80, 20, village)
    hut3 = Huts(75, 35, village)

    cannon1 = Cannons(60, 15, village)
    cannon2 = Cannons(45, 35, village)

    wiz1 = Wizards(60, 20 , village)
    wiz2 = Wizards(45, 15, village)
    cannons_array = [(59, 15), (44, 35)]

    village.add_building(townhall1)
    village.add_building(hut1)
    village.add_building(hut2)
    village.add_building(hut3)
    village.add_building(cannon1)
    village.add_building(cannon2)
    village.add_building(wiz1)
    village.add_building(wiz2)


    Wall = []
    count = 0
    for i in range(30, 90):
        Wall.append(Walls(i, 10, village))
        village.add_building(Wall[count])
        count += 1
    for i in range(30, 91):
        Wall.append(Walls(i, 40, village))
        village.add_building(Wall[count])
        count += 1

    for i in range(10, 40):
        Wall.append(Walls(30, i, village))
        village.add_building(Wall[count])
        count += 1

    for i in range(10, 40):
        Wall.append(Walls(90, i, village))
        village.add_building(Wall[count])
        count += 1

    non_wall_array = [(39, 17), (5, 18), (15, -20), (0, 10), (20, -5), (-5, 15)]
    build_y = [39, 79, 74, 59, 44]
    build_x = [17, 20, 35, 15, 35]

    os.system('stty echo')
    choice = input("Press K for King and Q for Queen: ")
    input_array.append(choice)
    if choice == 'K':
        king1 = king(10, 25, village)
    else:
        king1 = queen(10,25,village)



    # t_end = time.time() + 60 * 15
    barb_count = 0
    arch_count = 0
    Barbarians = []
    Archers = []
    inty =1
    os.system('stty -echo')
    while (1):

        start = time.time()
        
        king1.king_health_bar()
        dire = input_to(Get(), 0.1)
        input_array.append(dire)
        if dire == 'w':
            king1.move('w',village)
        elif dire == 's':
            king1.move('s',village)
        elif dire == 'a':
            king1.move('a',village)
        elif dire == 'd':
            king1.move('d',village)
        elif dire == ' ':
            if (king1.axe%2 == 0):
                king1.attack_normal(village)
            if (king1.axe%2 == 1):
                king1.attack_normal(village)

    
            
        elif dire == '1':
            if barb_count == 10:
                continue
            Barbarians.append(Barbarian(5,20,village))
            barb_count += 1
        elif dire == '2':
            if barb_count == 10:
                continue
            Barbarians.append(Barbarian(5, 40,village))
            barb_count += 1
        elif dire == '3':
            if barb_count == 10:
                continue
            Barbarians.append(Barbarian(75,5,village))
            barb_count += 1
        elif dire == '4':
            if arch_count == 10:
                continue
            Archers.append(Archer(8,20,village))
            arch_count += 1
        elif dire == '5':
            if arch_count == 10:
                continue
            Archers.append(Archer(8, 40,village))
            arch_count += 1
        elif dire == '6':
            if arch_count == 10:
                continue
            Archers.append(Archer(80,8,village))
            arch_count += 1
        elif dire == 'l':
            king1.axe = king1.axe + 1
        # elif dire == 't':
        #     king1.move_up_2()
        # elif dire == 'g':
        #     king1.move_down_2()
        # elif dire == 'f':
        #     king1.move_left_2()
        # elif dire == 'h':
        #     king1.move_right_2()
        elif dire == 'm':
            king1.health_inc()
        elif dire == 'r':
            king1.rage()

        elif dire == 'x':
            input_file = input('Save game as: ')
            with open(input_file + '.json', 'w') as outfile:
                json.dump(input_array, outfile)
            exit()




        for barbarian in Barbarians:
            barbarian.move(village)
            if(barbarian.health <= 0):
                Barbarians.remove(barbarian)
                village.remove_troop(barbarian)

        for archer in Archers:
            if (inty%2==0):
                archer.move(village)
            if(archer.health <= 0):
                Archers.remove(archer)
                village.remove_troop(archer)

        if(cannon1.health >= 0):
            cannon1.cannon_shoot(village)
        if(cannon2.health >= 0):
            cannon2.cannon_shoot(village)
        if(wiz1.health >= 0):
            wiz1.wizard_shoot(village)
        if(wiz2.health >= 0):
            wiz2.wizard_shoot(village)

        if(king1.health <= 0):
            village.remove_troop(king1)

        inty = inty + 1

        village.print_grid()
        print(king1.x,"King", king1.y)
        print(hut1.health)
        king1.king_dies(input_array)
        if(king1.health <= 0):
            if(barb_count == 10 and arch_count == 10):
                for i in village.troops:
                    if (i.health<= 0):
                        print("YAAAAY You WIN !!!!!")
                        input_file = input('Save game as: ')
                        with open(input_file + '.json', 'w') as outfile:
                            json.dump(input_array, outfile)
                        exit()
        
        for i in village.buildings:
            if(i.health <= 0):
                print("YAAAAY You LOSE !!!!!")
                input_file = input('Save game as: ')
                with open(input_file + '.json', 'w') as outfile:
                    json.dump(input_array, outfile)
                exit()

        if dire == 'q':
            break
    
elif(level == '1'):

    village = Village(100, 45)
    village.init_grid()
    village.make_border(village.grid)

    townhall1 = TownHall(60, 25, village)

    hut1 = Huts(40, 17, village)
    hut2 = Huts(80, 20, village)
    hut3 = Huts(75, 35, village)

    cannon1 = Cannons(60, 15, village)


    wiz1 = Wizards(60, 20 , village)

    cannons_array = [(59, 15), (44, 35)]

    village.add_building(townhall1)
    village.add_building(hut1)
    village.add_building(hut2)
    village.add_building(hut3)
    village.add_building(cannon1)
    village.add_building(wiz1)



    Wall = []
    count = 0
    for i in range(30, 90):
        Wall.append(Walls(i, 10, village))
        village.add_building(Wall[count])
        count += 1
    for i in range(30, 91):
        Wall.append(Walls(i, 40, village))
        village.add_building(Wall[count])
        count += 1

    for i in range(10, 40):
        Wall.append(Walls(30, i, village))
        village.add_building(Wall[count])
        count += 1

    for i in range(10, 40):
        Wall.append(Walls(90, i, village))
        village.add_building(Wall[count])
        count += 1

    non_wall_array = [(39, 17), (5, 18), (15, -20), (0, 10), (20, -5), (-5, 15)]
    build_y = [39, 79, 74, 59, 44]
    build_x = [17, 20, 35, 15, 35]

    os.system('stty echo')
    choice = input("Press K for King and Q for Queen: ")
    input_array.append(choice)
    if choice == 'K':
        king1 = king(10, 25, village)
    else:
        king1 = queen(10,25,village)



    # t_end = time.time() + 60 * 15
    barb_count = 0
    arch_count = 0
    Barbarians = []
    Archers = []
    inty =1
    os.system('stty -echo')
    while (1):

        start = time.time()
        
        king1.king_health_bar()
        dire = input_to(Get(), 0.1)
        input_array.append(dire)
        if dire == 'w':
            king1.move('w',village)
        elif dire == 's':
            king1.move('s',village)
        elif dire == 'a':
            king1.move('a',village)
        elif dire == 'd':
            king1.move('d',village)
        elif dire == ' ':
            if (king1.axe%2 == 0):
                king1.attack_normal(village)
            if (king1.axe%2 == 1):
                king1.attack_normal(village)

    
            
        elif dire == '1':
            if barb_count == 5:
                continue
            Barbarians.append(Barbarian(5,20,village))
            barb_count += 1
        elif dire == '2':
            if barb_count == 5:
                continue
            Barbarians.append(Barbarian(5, 40,village))
            barb_count += 1
        elif dire == '3':
            if barb_count == 5:
                continue
            Barbarians.append(Barbarian(75,5,village))
            barb_count += 1
        elif dire == '4':
            if arch_count == 5:
                continue
            Archers.append(Archer(8,20,village))
            arch_count += 1
        elif dire == '5':
            if arch_count == 5:
                continue
            Archers.append(Archer(8, 40,village))
            arch_count += 1
        elif dire == '6':
            if arch_count == 5:
                continue
            Archers.append(Archer(80,8,village))
            arch_count += 1
        elif dire == 'l':
            king1.axe = king1.axe + 1
        # elif dire == 't':
        #     king1.move_up_2()
        # elif dire == 'g':
        #     king1.move_down_2()
        # elif dire == 'f':
        #     king1.move_left_2()
        # elif dire == 'h':
        #     king1.move_right_2()
        elif dire == 'm':
            king1.health_inc()
        elif dire == 'r':
            king1.rage()

        elif dire == 'x':
            input_file = input('Save game as: ')
            with open(input_file + '.json', 'w') as outfile:
                json.dump(input_array, outfile)
            exit()




        for barbarian in Barbarians:
            barbarian.move(village)
            if(barbarian.health <= 0):
                Barbarians.remove(barbarian)
                village.remove_troop(barbarian)

        for archer in Archers:
            if (inty%2==0):
                archer.move(village)
            if(archer.health <= 0):
                Archers.remove(archer)
                village.remove_troop(archer)

        if(cannon1.health >= 0):
            cannon1.cannon_shoot(village)

        if(wiz1.health >= 0):
            wiz1.wizard_shoot(village)


        if(king1.health <= 0):
            village.remove_troop(king1)

        inty = inty + 1

        village.print_grid()
        print(king1.x,"King", king1.y)
        print(hut1.health)
        king1.king_dies(input_array)

        if(king1.health <= 0):
            if(barb_count == 5 and arch_count == 5):
                for i in village.troops:
                    if (i.health<= 0):
                        print("YAAAAY You WIN !!!!!")
                        input_file = input('Save game as: ')
                        with open(input_file + '.json', 'w') as outfile:
                            json.dump(input_array, outfile)
                        exit()
        
        for i in village.buildings:
            if(i.health <= 0):
                print("YAAAAY You LOSE !!!!!")
                input_file = input('Save game as: ')
                with open(input_file + '.json', 'w') as outfile:
                    json.dump(input_array, outfile)
                exit()

        if dire == 'q':
            break

elif(level == '3'):
    

    village = Village(100, 45)
    village.init_grid()
    village.make_border(village.grid)

    townhall1 = TownHall(60, 25, village)

    hut1 = Huts(40, 17, village)
    hut2 = Huts(80, 20, village)
    hut3 = Huts(75, 35, village)

    cannon1 = Cannons(60, 15, village)
    cannon2 = Cannons(45, 35, village)
    cannon3 = Cannons(15, 35, village)

    wiz1 = Wizards(60, 20 , village)
    wiz2 = Wizards(45, 15, village)
    wiz3 = Wizards(15, 15, village)
    cannons_array = [(59, 15), (44, 35)]

    village.add_building(townhall1)
    village.add_building(hut1)
    village.add_building(hut2)
    village.add_building(hut3)
    village.add_building(cannon1)
    village.add_building(cannon2)
    village.add_building(wiz1)
    village.add_building(wiz2)


    Wall = []
    count = 0
    for i in range(30, 90):
        Wall.append(Walls(i, 10, village))
        village.add_building(Wall[count])
        count += 1
    for i in range(30, 91):
        Wall.append(Walls(i, 40, village))
        village.add_building(Wall[count])
        count += 1

    for i in range(10, 40):
        Wall.append(Walls(30, i, village))
        village.add_building(Wall[count])
        count += 1

    for i in range(10, 40):
        Wall.append(Walls(90, i, village))
        village.add_building(Wall[count])
        count += 1

    non_wall_array = [(39, 17), (5, 18), (15, -20), (0, 10), (20, -5), (-5, 15)]
    build_y = [39, 79, 74, 59, 44]
    build_x = [17, 20, 35, 15, 35]

    os.system('stty echo')
    choice = input("Press K for King and Q for Queen: ")
    input_array.append(choice)
    if choice == 'K':
        king1 = king(10, 25, village)
    else:
        king1 = queen(10,25,village)



    # t_end = time.time() + 60 * 15
    barb_count = 0
    arch_count = 0
    Barbarians = []
    Archers = []
    inty =1
    os.system('stty -echo')
    while (1):

        start = time.time()
        
        king1.king_health_bar()
        dire = input_to(Get(), 0.1)
        input_array.append(dire)
        if dire == 'w':
            king1.move('w',village)
        elif dire == 's':
            king1.move('s',village)
        elif dire == 'a':
            king1.move('a',village)
        elif dire == 'd':
            king1.move('d',village)
        elif dire == ' ':
            if (king1.axe%2 == 0):
                king1.attack_normal(village)
            if (king1.axe%2 == 1):
                king1.attack_normal(village)


            
        elif dire == '1':
            if barb_count == 15:
                continue
            Barbarians.append(Barbarian(5,20,village))
            barb_count += 1
        elif dire == '2':
            if barb_count == 15:
                continue
            Barbarians.append(Barbarian(5, 40,village))
            barb_count += 1
        elif dire == '3':
            if barb_count == 15:
                continue
            Barbarians.append(Barbarian(75,5,village))
            barb_count += 1
        elif dire == '4':
            if arch_count == 15:
                continue
            Archers.append(Archer(8,20,village))
            arch_count += 1
        elif dire == '5':
            if arch_count == 15:
                continue
            Archers.append(Archer(8, 40,village))
            arch_count += 1
        elif dire == '6':
            if arch_count == 15:
                continue
            Archers.append(Archer(80,8,village))
            arch_count += 1
        elif dire == 'l':
            king1.axe = king1.axe + 1
        # elif dire == 't':
        #     king1.move_up_2()
        # elif dire == 'g':
        #     king1.move_down_2()
        # elif dire == 'f':
        #     king1.move_left_2()
        # elif dire == 'h':
        #     king1.move_right_2()
        elif dire == 'm':
            king1.health_inc()
        elif dire == 'r':
            king1.rage()
        
        elif dire == 'x':
            input_file = input('Save game as: ')
            with open(input_file + '.json', 'w') as outfile:
                json.dump(input_array, outfile)
            exit()

        


        for barbarian in Barbarians:
            barbarian.move(village)
            if(barbarian.health <= 0):
                Barbarians.remove(barbarian)
                village.remove_troop(barbarian)

        for archer in Archers:
            if (inty%2==0):
                archer.move(village)
            if(archer.health <= 0):
                Archers.remove(archer)
                village.remove_troop(archer)

        if(cannon1.health >= 0):
            cannon1.cannon_shoot(village)
        if(cannon2.health >= 0):
            cannon2.cannon_shoot(village)
        if(wiz1.health >= 0):
            wiz1.wizard_shoot(village)
        if(wiz2.health >= 0):
            wiz2.wizard_shoot(village)
        if(cannon3.health >= 0):
            cannon3.cannon_shoot(village)
        if(wiz3.health >= 0):
            wiz3.wizard_shoot(village)

        if(king1.health <= 0):
            village.remove_troop(king1)
        

        inty = inty + 1

        village.print_grid()
        print(king1.x,"King", king1.y)
        print(hut1.health)
        king1.king_dies(input_array)

        if(king1.health <= 0):
            if(barb_count == 15 and arch_count == 15):
                for i in village.troops:
                    if (i.health<= 0):
                        print("YAAAAY You WIN !!!!!")
                        input_file = input('Save game as: ')
                        with open(input_file + '.json', 'w') as outfile:
                            json.dump(input_array, outfile)
                        exit()
        
        for i in village.buildings:
            if(i.health <= 0):
                print("YAAAAY You LOSE !!!!!")
                input_file = input('Save game as: ')
                with open(input_file + '.json', 'w') as outfile:
                    json.dump(input_array, outfile)
                exit()


        if dire == 'q':
            break