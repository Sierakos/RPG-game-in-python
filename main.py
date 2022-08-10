from random import *

import os

from player import Player
from enemy import Enemy
from save_system import read_stats, create_file, reset_stats, write_to_file
from items import WEAPONS, USABLE

def line():
    print("xX--------------------Xx")

class GameClass:
    def __init__(self):
        self.player_location = [5,5]
        self.player_icon = 'H'
        self.message = ''
        self.localizations = {
            "Town": {
                "Shop": [[2,3], '$'],
                "Tavern": [[4,3], '@'],
                "Church": [[8,6], '+'],
                "Basement": [[2, 7], 'B']
            },
            "Basement": {
                "Chest": [[8,2], "&"],
                "Town": [[2,7], "T"]
            }
        }
        self.game_location = "Town"
        self.map = None
        self.player = None

    def fight(self): 
        enemy = Enemy(1, 'Szkieletor', 'Wojownik', 1, 0, 15, 80)
        
        while True:
            self.player.print_info()
            enemy.print_info()
            print("Wybierz akcje: ")
            print('*'*20)
            print('1. Zwykły atak')
            print('2. Mocniejsze ataki')
            print('3. Użyj przedmiotu')
            print('*'*20)

            choose = input()
            if choose == '1':
                damage = 0
                for key, value in self.player.weapon.items():
                    weapon_min_atk = self.player.weapon[key]['Atk-min']
                    weapon_max_atk = self.player.weapon[key]['Atk-max']
                min_atk = self.player.level * weapon_min_atk
                max_atk = self.player.level * weapon_max_atk
                dice = randint(1,100)
                if dice < self.player.luck * 10:
                    damage = randint(min_atk*20,max_atk*20)
                    enemy.hp_loss(damage)
                    print(f"KRYTYCZNE UDERZENIE W {enemy.name} ZADAŁEŚ MU {str(damage)} OBRAŻEŃ")

                else:
                    damage = randint(min_atk*10,max_atk*10)
                    enemy.hp_loss(damage)
                    print(f"Zaatakowałeś {enemy.name} zadając mu {str(damage)} obrażeń")

                if enemy.hp <= 0:
                    print(f"Pokonałeś {str(enemy.name)} dostałes {str(enemy.level*2)} exp oraz {str(enemy.level*2)} monet")
                    self.player.exp += enemy.level*2
                    self.player.money += enemy.level*2
                    if self.player.exp >= self.player.level * 5:
                        self.player.level += 1
                        self.player.update_player_stats()
                        self.player.hp = self.player.max_hp
                        self.player.mp = self.player.max_mp
                        self.player.exp = 0
                        print(f"AWANSOWAŁEŚ DO POZIOMU: {self.player.level}")
                    break

                enemy_damage = randint(1*enemy.level, 2*enemy.level)
                self.player.hp_loss(enemy_damage)
                print(f"Przeciwnik zaatakował cię zadając {str(enemy_damage)} obrażeń")

                if self.player.hp <= 0:
                    self.game_over()

            elif choice == "2":
                self.special_attack_page()

    def game(self):
        if os.stat("saves/save_1.txt").st_size == 0:
            name = input("Wpisz nazwę postaci: ")
            for proffesion in ['Wojownik', 'Łucznik', 'Mag']:
                print(proffesion)
            prof = input("Wybierz klase postaci: ")
            
            eq = {}
            weapon = {
                "Gołe pięści": {
                    "Rodzaj": "Bron",
                    "Atk-min": 1,
                    "Atk-max": 2,
                    "Cena": 0,
                    "Ilosc": 1
                }}
            money = 0
            write_to_file(1,name,prof,1,0,10,5,eq,weapon,0)
        else:
            stats = read_stats()
            name = stats[1]
            prof = stats[2]
            eq = {}
            weapon = {stats[7][-1]: WEAPONS[stats[7][-1]]}
            for i in range(len(stats[7])-1):
                print(stats[7][i].split(':')[1])
                if stats[7][i].split(':')[0] == 'Bron':
                    eq[stats[7][i].split(':')[1]] = WEAPONS[stats[7][i].split(':')[1]]
                elif stats[7][i].split(':')[0] == 'Mikstura HP':
                    eq[stats[7][i].split(':')[1]] = USABLE[stats[7][i].split(':')[1]]
                eq[stats[7][i].split(':')[1]]['Ilosc'] = int(stats[7][i].split(':')[2])

            money = int(stats[8])
            

        stats = read_stats()
        
        self.player = Player(
            int(stats[0]),
            name,
            prof,
            int(stats[3]),
            int(stats[4]),
            int(stats[5]),
            int(stats[6]),
            eq,
            weapon,
            money
        )
        
        """
        Move system that detect in which direction
        character will move
        """
        self.draw_board()
        while True:
            move = input("")
            if (move == "w" or move == "W") and self.player_location[1] > 0:
                self.player_location[1] -= 1
                self.draw_board()
            elif (move == "s" or move == "S") and self.player_location[1] < 10:
                self.player_location[1] += 1
                self.draw_board()
            elif (move == "a" or move == "A") and self.player_location[0] > 0:
                self.player_location[0] -= 1
                self.draw_board()
            elif (move == "d" or move == "D") and self.player_location[0] < 10:
                self.player_location[0] += 1
                self.draw_board()
            elif (move == "b" or move == "B"):
                self.player.print_info()
                self.player.print_additional_info()
            elif (move == "h" or move == "H"):
                self.player.heal(5)
            elif (move == "l" or move == "L"):
                self.player.money += 1
            elif (move == "i" or move == "I"):
                self.eq()
                self.draw_board()
            elif (move == "f" or move == "F"):
                self.fight()
            elif (move == "save"):
                self.player.save_char()
            elif (move == "exit"):
                self.player.save_char()
                self.main_menu()
        

    def draw_board(self):
        location = self.game_location
        map = [[0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0]]

        self.map = map

        """
        List of Localization and some places here.
        Also there is function that detect did character
        is on some object (like shop, basement etc.)
        """
        if location == "Town":
            for object in self.localizations["Town"]:
                self.detect_colision(self.player_location, self.localizations[location][object][0], location=location, place=object)
                obj_icon = ''
                for i in [self.localizations["Town"][object][1]]:
                    obj_icon += i
                map[self.localizations["Town"][object][0][1]][self.localizations["Town"][object][0][0]] = obj_icon
                

        if location == "Basement":
            for object in self.localizations["Basement"]:
                self.detect_colision(self.player_location, self.localizations[location][object][0], location=location, place=object)
                obj_icon = ''
                for i in [self.localizations["Basement"][object][1]]:
                    obj_icon += i
                map[self.localizations["Basement"][object][0][1]][self.localizations["Basement"][object][0][0]] = obj_icon
                


        """
        Display player on map
        """
        map[self.player_location[1]][self.player_location[0]] = self.player_icon

        board_str = ""

        for i in map:
            for j in i:
                if j == 0:
                    board_str += ". "
                else:
                    board_str += str(j) + " "
            board_str += ('\n')

        """
        Print out our map
        """
        # os.system('cls')
        print(self.player_location)
        print(self.game_location)
        print(board_str)
        if self.message is not None:
            print(self.message)

        self.message = ''

    def detect_colision(self, player_location, object_place, location, place):
        if player_location == object_place and location == "Town":
            if place == "Shop":
                self.shop_page()

            if place == "Basement":
                self.game_location = "Basement"
                self.player_location[1] += 1
                

        if player_location == object_place and location == "Basement":
            if place == "Town":
                self.game_location = "Town"
                self.player_location[1] += 1

    def shop_page(self):
        os.system('cls')
        while True:
            print("Sklep")
            print("-"*50)
            print("1. Kup")
            print("2. Sprzedaj")
            print("3. Wyjdź")
            print("-"*50)
            choose = input()
            if choose == "1":
                self.shop_buy_page()
            elif choose == "2":
                self.shop_sell_page()
            elif choose == "3":
                self.player_location[0] += 1
                break

    def shop_buy_page(self):
        os.system('cls')
        while True:
            print("Kup")
            print("-"*50)
            i=0
            # Write your item in this order: weapons, HP potions
            items_in_shops = {1: "Patyk", 2: "Drewniana proca", 3: "Mala mikstura HP"}
            print("Bronie: ")
            for item in WEAPONS:
                for item_shop in items_in_shops:
                    if items_in_shops[item_shop] == item:
                        i += 1
                        print(f"{str(i)}. {item} CENA: {WEAPONS[item]['Cena']}")
            print("\nMikstury: ")
            for item in USABLE:
                for item_shop in items_in_shops:
                    if items_in_shops[item_shop] == item:
                        i += 1
                        print(f"{str(i)}. {item} CENA: {USABLE[item]['Cena']}")

            print(f"{str(i+1)}. Wyjdź")
            print("-"*50)

            choose = input()
            try: 
                if int(choose) > 0 and int(choose) <= len(items_in_shops) and WEAPONS[items_in_shops[int(choose)]]['Rodzaj'] == 'Bron':
                    if self.player.money >= WEAPONS[items_in_shops[int(choose)]]['Cena']:
                        print(f"Kupiłeś {items_in_shops[int(choose)]}")
                        if items_in_shops[int(choose)] not in self.player.eq:
                            self.player.eq[items_in_shops[int(choose)]] = WEAPONS[items_in_shops[int(choose)]]
                            self.player.eq[items_in_shops[int(choose)]]['Ilosc'] = 1
                            self.player.money -= WEAPONS[items_in_shops[int(choose)]]['Cena']
                        else:
                            self.player.eq[items_in_shops[int(choose)]]['Ilosc'] += 1
                            self.player.money -= WEAPONS[items_in_shops[int(choose)]]['Cena']
                    else:
                        print("Nie stać cię na to")
                if choose == str(i+1):
                    break
            except KeyError as e:
                pass

            try:
                if int(choose) > 0 and int(choose) <= len(items_in_shops) and USABLE[items_in_shops[int(choose)]]['Rodzaj'] == 'Mikstura HP':
                    if self.player.money >= USABLE[items_in_shops[int(choose)]]['Cena']:
                        print(f"Kupiłeś {items_in_shops[int(choose)]}")
                        if items_in_shops[int(choose)] not in self.player.eq:
                            self.player.eq[items_in_shops[int(choose)]] = USABLE[items_in_shops[int(choose)]]
                            self.player.eq[items_in_shops[int(choose)]]['Ilosc'] = 1
                            self.player.money -= USABLE[items_in_shops[int(choose)]]['Cena']
                        else:
                            self.player.eq[items_in_shops[int(choose)]]['Ilosc'] += 1
                            self.player.money -= USABLE[items_in_shops[int(choose)]]['Cena']
                    else:
                        print("Nie stać cię na to")
                if choose == str(i+1):
                    break
            except KeyError as e:
                pass

    def shop_sell_page(self):
        os.system('cls')
        while True:
            print("Sprzedaj")
            line()
            items_in_eq = {}
            i = 0
            for item in self.player.eq:
                i += 1
                print(f"{str(i)}. {item}")
                items_in_eq[i] = item
            

            print(f"{str(i+1)}. Wyjdź")
            choice = input("> ")

            try:
                self.player.money += self.player.eq[items_in_eq[int(choice)]]['Cena']
                if self.player.eq[items_in_eq[int(choice)]]['Ilosc'] == 1:
                    
                    for key, value in self.player.weapon.items():
                        if self.player.weapon[key] == self.player.eq[items_in_eq[int(choice)]]:
                            self.player.weapon = {}
                            self.player.weapon['Gołe pięści'] = WEAPONS['Gołe pięści']
                    self.player.eq.pop(items_in_eq[int(choice)])
                else:
                    self.player.eq[items_in_eq[int(choice)]]['Ilosc'] -= 1
            except:
                pass

            if choice == str(i+1):
                break

            

    def eq(self):
        while True:
            i = 0
            items_in_eq = {}
            line()
            print("Bronie:")
            for item in self.player.eq:
                if self.player.eq[item]['Rodzaj'] == "Bron":
                    i += 1
                    print(str(i) + ". " + item + " ilość: " + str(self.player.eq[item]['Ilosc']))
                    items_in_eq[i] = item
            
            print("\nMikstury HP:")
            for item in self.player.eq:
                if self.player.eq[item]['Rodzaj'] == "Mikstura HP":
                    i += 1
                    print(str(i) + ". " + item + " ilość: " + str(self.player.eq[item]['Ilosc']))
                    items_in_eq[i] = item


            
            print(f"\n{str(i+1)}. Wyjdź")
            
            print("\nTwoje założone bronie:")
            print(self.player.weapon)
            print(f"Monety: {self.player.money}")
            line()
            choice = input()
            try:
                if self.player.eq[items_in_eq[int(choice)]]['Rodzaj'] == 'Bron':
                    self.player.weapon = {}
                    self.player.weapon[items_in_eq[int(choice)]] = self.player.eq[items_in_eq[int(choice)]]
            except:
                pass


            print(self.player.eq)
            if choice == str(i+1):
                break

    def game_over(self):
        print('Przegrałeś. Powodzenia następnym razem')
        self.main_menu()

    def main_menu(self):
        print("Katakoomby")
        print("-"*50)
        print("1. Nowa gra")
        print("2. Wczytaj grę")
        print("3. Opcje")
        print("4. Wyjdź")
        print("-"*50)
        choose = input()

        if choose == "1":
            create_file()
            reset_stats()
            self.game()
        elif choose =="2":
            if not os.path.exists("saves/save_1.txt"):
                print("Nie masz zapisu gry. Stwórz nową grę")
            self.game()
        elif choose == "3":
            print("Tu będą opcje")
        elif choose == "4":
            exit()

    def run(self):
        self.main_menu()

if __name__ == '__main__':
    game = GameClass()
    game.run()