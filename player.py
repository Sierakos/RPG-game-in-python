from save_system import write_to_file

class Player:
    def __init__(self, id, name, prof, level, exp, hp, mp, eq, weapon, money):
        self.id = id
        self.name = name
        self.prof = prof
        self.level = level
        self.exp = exp
        self.hp = hp
        self.max_hp = 0
        self.max_mp = 0
        self.mp = 0
        self.atk = 0
        self.magic_atk = 0
        self.defence = 0
        self.luck = 0
        self.weapon = weapon
        self.armor = {}
        self.potions = {}
        self.eq = eq
        self.money = money
        self.max_exp = 0

        if self.prof == "Wojownik":
            self.atk = 4
            self.magic_atk = 2
            self.defence = 4
            self.luck = 2
            self.max_hp = self.level * 20
            self.max_mp = self.level * 5
        elif self.prof == "Łucznik":
            self.atk = 4
            self.magic_atk = 2
            self.defence = 2
            self.luck = 4
            self.max_mp = self.level * 7
            self.max_hp = self.level * 17
        elif self.prof == "Mag":
            self.atk = 2
            self.magic_atk = 6
            self.defence = 2
            self.luck = 1
            self.max_hp = self.level * 15
            self.max_mp = self.level * 12


    def hp_loss(self, ammount):
        self.hp -= ammount

    def heal(self, ammount):
        if (self.hp + ammount >= self.max_hp):
            self.hp = self.max_hp
        else:
            self.hp += ammount

    def update_player_stats(self):
        self.max_hp = self.level * 20
        self.max_mp = self.level * (self.magic_atk*2)

    def print_info(self):
        print(f'nazwa: {self.name}')
        print("*"*20)
        print(f'profesja: {self.prof}')
        print(f'poziom: {str(self.level)}')
        print(f'HP: {self.hp} / {self.max_hp}')
        print(f'MP: {self.mp} / {self.max_mp}')
        print('*'*20)

    

    def print_additional_info(self):
        print(f'Współczynnik ataku: {str(self.atk)}')
        print(f'Współczynnik magicznego ataku: {str(self.magic_atk)}')
        print(f'Współczynnik obrony: {str(self.defence)}')

    def print_eq(self):
        print("Ekwipunek: ")
        print("*"*20)
        for i in self.eq:
            print(i + ": " + str(self.eq[i]))
        print('*'*20)

    def save_char(self):
        write_to_file(self.id,self.name,self.prof,self.level,self.exp,self.hp,self.mp,self.eq,self.weapon,self.money)
