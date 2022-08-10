class Enemy:
    def __init__(self, id, name, prof, level, exp, hp, mp):
        self.id = id
        self.name = name
        self.prof = prof
        self.level = level
        self.exp = exp
        self.hp = hp
        self.mp = mp

    def hp_loss(self, ammount):
        self.hp -= ammount

    def print_info(self):
        print(f'nazwa: {self.name}')
        print("*"*20)
        print(f'profesja: {self.prof}')
        print(f'poziom: {str(self.level)}')
        print(f'HP: {self.hp}')
        print(f'MP: {self.mp}')
        print('*'*20)