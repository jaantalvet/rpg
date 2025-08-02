
# example game
# https://github.com/codinggrace/text_based_adventure_game/blob/master/game_02.py

import html
import os
import game

def choose_players():

    print("\n======= Menu =======")
    print("Choose Player type")    

    all_players = game.load_data_from_json("settings.json","player")

    #all_attacks = all_attacks.get("melee", {})
    #self.attacks = {name: Attack(name,**data) for name, data in melee_attacks.items()}

    i = 1
    tmp = []
    for p in all_players:
        print(f"[{i}] {p}")
        tmp.append(p)
        i+=1

    # get choice of player: human, elf or dwarf
    while True:
        try:
            selection = input("> ")
            character_class = tmp[int(selection)-1]         # "Human"
            selected = all_players.get(character_class)     # {'name':'Bob', ...}
            print("You selected: " + selected["name"] + ", the " + character_class)
            # now create the player class instance. selected is dict of attributes
            if hasattr(game, character_class):
                player = getattr(game, character_class)(**selected) 
            else:
                raise ValueError(f"Class {character_class} not found game module")
            break
        except ValueError:
            print("Invalid input. try again\n\n>")


    print(f"Attack equiped: {player.equiped_attack.name} will do {player.equiped_attack.damage} damage" )

    print("\n======= Menu =======")
    print("Choose Enemy character")

    enemies = game.load_data_from_json("settings.json","enemy")
    i=1
    tmp=[]
    for e in enemies:
        print(f"[{i}] {e}")
        tmp.append(e)
        i+=1

    while True:
        try:
            selection = input("> ")
            enemy_type = tmp[int(selection)-1] # goblin
            selected = enemies.get(enemy_type) # {'name':'Troll', ...}
            print("You selected a: " + selected["name"])
            # create the instance
            enemy = getattr(game, "Enemy")(**selected)

            break
        except ValueError:
            print("Invalid input. try again\n\n>")
    
    print(f"player attack: {enemy.equiped_attack.name} will do {enemy.equiped_attack.damage} damage" )


    return player, enemy



def show_menu(players_selected):
    print("\n======= Menu =======")
    print(" [1]: Select Players")
    if(players_selected):
        print(" [2]: Battle")
    print(" Press [q] at any time to quit")
    print("====================")

def battle(player, enemy):

    b = game.Battle(player, enemy)

def start():
    players_selected=False
    show_menu(players_selected)
    while True:
        try:
            #default value. or "blort" . Click,Typer,Rich, for terminal progs
            answer = html.escape(input("> "))
            if answer=="1":
                characters = choose_players()
                players_selected = True
            elif answer=="2":
                print("Starting Battle!.........\n> ")
                battle(characters[0],characters[1])
            elif answer=="q":
                print("Exiting game.")
                break
            else:
                print("Invalid input. Try again\n\n> ")

            #always show the menua
            show_menu(players_selected)

        except ValueError:
            print("Invalid input. try again\n\n>")

if __name__ == '__main__':
    start()