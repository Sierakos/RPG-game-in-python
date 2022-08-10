from genericpath import isfile
import os

def create_file():
    if not os.path.exists("saves/save_1.txt"):
        f = open('saves/save_1.txt', 'w')
    
def write_to_file(id,name,prof,lvl,exp,hp,mp,eq,weapon,money):
    f = open('saves/save_1.txt', 'w')
    f.write('')
    f.write(f'{id},{name},{prof},{lvl},{exp},{hp},{mp}|')
    for item in eq:
        f.write(f"{eq[item]['Rodzaj']}:{item}:{eq[item]['Ilosc']}<>")
    for item in weapon:
        f.write(f"{item}")
    f.write(f"|{str(money)}")

def read_stats():
    f = open('saves/save_1.txt', 'r')
    lines = []
    stats = []
    for line in f:
        lines += line.split('|')

    stats = lines[0].split(',')
    stats.append(lines[1].split('<>'))
    stats.append(str(lines[2]))
    return stats

def reset_stats():
    f = open('saves/save_1.txt', 'w')
    f.write('')

print(read_stats())