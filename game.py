import random
import json

# goal:
# create a character class where skills/benefits/hp are influenced by their race
# see pygame tut: https://python-forum.io/thread-401.html (9 parts, OOP later)

settings="settings.json"

def load_data_from_json(filepath, date_type):
    """Loads the attacks from the file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}.")
        return {}
    
    return data.get(date_type, {})


class Character():
    def __init__(self, name, hp, mp, power, strength, defense, speed, xp, level=1, **kwargs):
        self._name      = name
        self._hp        = hp
        self._mp        = mp
        self._strength  = strength
        self._power     = power
        self._defense   = defense
        self._speed     = speed
        self._xp        = xp
        self._level     = level
        super().__init__(**kwargs)
    
        all_attacks = load_data_from_json(settings, "attacks")
        player_attacks = all_attacks.get("player", {})
        self.attacks = {name: Attack(name,**data) for name, data in player_attacks.items()}

        #attacks["punch"].damage
        # default attack is the first item in the list
        self.equiped_attack = list(self.attacks.values())[0]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,val):
        self._name = val

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self,val):
        if(val<0):
            self._hp=0
            #print("health clamped at 0")
        else:
            self._hp = val
    
    @property
    def mp(self):
        return self._mp

    @mp.setter
    def mp(self,val):
        self._mp = val
    
    @property
    def power(self):
        return self._power

    @power.setter
    def power(self,val):
        self._power = val

    @property
    def strength(self):
        return self._strength

    @strength.setter
    def strength(self,val):
        self._strength = val
            
    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self,val):
        self._defense = val
    
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self,val):
        self._speed = val

    @property
    def xp(self):
        return self._exp

    @xp.setter
    def xp(self,val):
        self._xp = val

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self,val):
        self._level = val

    def take_damage(self, amount):
        #print(f"  {self.name} has {self.defense} defense")
        damage = amount - self.defense
        # print(f"  {self.name}'s attack of {amount} is reduced to {damage}")
        if damage<=0:
            #print("damange rounded to 0")
            damage=0
        self.hp-=damage
        print(f"    {self.name} takes {damage} damage")

        if(self.hp<=0):
            print(f"  {self.name} has been defeated!")

    def equip_attack(self, attack_name):
        if attack_name in self.attacks:
            self.equipped_attack = self.attacks[attack_name]
            print(f"{self.name} equips {attack_name}")
        else:
            print(f"{self.name} doesn't know how to use {attack_name}")

    # this should use whatever is equiped. if weapon, the use it
    def attack(self, target):
        print(f"{self.name} is attacking {target.name}")
        if self.equiped_attack:
            self.equiped_attack.execute(self, target)
        # add default attack if nothing equipped        



class Attack:
    def __init__(self, name, damage, range, allowed):
        self.name = name
        self.damage = damage #weapon modifies
        self.range = range #speed modifies
        self.allowed = allowed

    def execute(self, attacker, target):
        print(f"  {attacker.name} uses {self.name} on {target.name}")
        
        #calculate the damage to take. att * att / (att + def) 
        damage = (random.randint(0,self.damage) * attacker.strength)
        # add luck modifier to grant killing blow or miss
        #r1 = random.randint(0,20)
        if damage==0:
            print(f"{attacker.name} misses!")
        target.take_damage(damage)

class Enemy(Character):
    def __init__(self, name, hp, mp, power, strength, defense, speed, xp, reward, death_cry, loot, attack, level=1, **kwargs):
        super().__init__(name, hp, mp, power, strength, defense, speed, xp, level, **kwargs)

        self._reward = reward
        self._death_cry = death_cry
        self._loot = loot
        self._level = level

        # equip the default attack.  if there are many attacks, choose the first
        # there is no "attack", then equip punch
        if(attack):
            self.equiped_attack = self.attacks[f"{attack}"]
        elif (len(self.attacks)>0):
             self.equiped_attack = list(self.attacks.values())[0]
        else:
            #add default attack 
            pass

    @property
    def reward(self):
        # returns gold
        # luck modifier. haven't implemented luck yet
        r1 = random.randint(0,20)
        r2 = random.randint(0,20)
        reward_bonus=0
        if(r1==r2):
            reward_bonus = 10 
        return self._reward * self._level + reward_bonus

class Human(Character):
    def __init__(self, name, hp, mp, power, strength, defense, speed, xp, level=1, **kwargs):
        super().__init__(name, hp, mp, power, strength, defense, speed, xp, level, **kwargs)
        
        # do we need a modifier method? add property, hp, then +/- for class
        # modifier: +1 charisma
        #self.equiped_attack = self.attacks[f"{attack}"]

class Elf(Character):
    def __init__(self, name, hp, mp, power, strength, defense, speed, xp, attack="short bow", level=1,**kwargs):
        super().__init__(name, hp, mp, power, strength, defense, speed, xp, level, **kwargs)

        # modifier: +1 speed
        self.speed+=1
        self.equiped_attack = self.attacks[f"{attack}"]
        print(f"************** attack: {self.equiped_attack}")

class Dwarf(Character):
    def __init__(self, name, hp, mp, power, strength, defense, speed, xp, level=1, **kwargs):
        super().__init__(name, hp, mp, power, strength, defense, speed, xp, level, **kwargs)

        # modifier: +1 defense
        self.defense+=1
        
class MagicUserMixin:
    def __init__(self, spell_power, **kwargs):
        super().__init__(**kwargs)
        # spell_power is equiv to strength
        # knowledge controls spell level
        self.spell_power = spell_power


    def cast_spell(self, target):
        # multiply spell power * level
        #level = getattr(self,'level')
        damage =self.level * self.spell_power
        if (self.mp>3):    
            #mp = getattr(self,'mp')
            target.take_damage(damage)
        else:
            print("no MP left. the spell failed")

class PowerAttackMixin:
    def __init__(self, strength_mod, **kwargs):
        super().__init__(**kwargs)
        # adds bonus to attacks
        self.strength_mod = strength_mod

    def power_attack(self, target):
        # strength * 2
        strength = getattr(self,'strength')
        damage = strength + self.strength_mod
        target.take_damage(damage)

# specialties: wizard, warrior, ranger...

class Warrior(PowerAttackMixin, Character):
    def __init__(self, name, hp, mp, strength, defense, speed, xp, level, strength_mod, **kwargs):
        super().__init__(name=name, hp=hp, mp=mp, strength=strength, defense=defense, speed=speed, exp=xp, level=level, strength_mod=strength_mod, **kwargs)

    #they ALL do attack, but the specialty is in the mixin
    def attack(self, target):
        self.power_attack(target)

class Mage(MagicUserMixin, Character):
    def __init__(self, name, hp, mp, strength, defense, speed, xp, level, spell_power, **kwargs):
        super().__init__(name=name, hp=hp, mp=mp, strength=strength, defense=defense, speed=speed, exp=xp, level=level, spell_power=spell_power, **kwargs)
        spell_data = load_data_from_json(settings, "spells") # Load spells
        self.spells = {name: Attack(name, **data) for name, data in spell_data.items()}
        self.equipped_spell = list(self.spells.values())[0] if self.spells else None

    # override equip_attack to make mages use "equip_spell"
    def equip_spell(self,spell_name):
        if spell_name in self.spells:
            self.equipped_spell = self.spells[spell_name]
            print(f"{self.name} prepares the spell {spell_name}")
        else:
            print(f"{self.name} does not know the spell {spell_name}!")

    def cast(self, target):
        if self.equipped_spell:
            self.equipped_spell.execute(self, target)
        else:
            print(f"{self.name} has no spell prepared")

    #they ALL do attack, but the specialty is in the mixin
    def attack(self, target):
        print(f"{self.name} is attacking {target.name}")
        self.cast_spell(target)
        self.mp-=3
        print(f"mp left: {self.mp}")

class Battle():
    # 2 characters battle!
    # make sure player is 1, enemy is 2
    def __init__(self, char1, char2):
        self.char1 = char1
        self.char2 = char2
        self.winner = None # initialize then check if was set
        self.round  = 0

        self.battle_stats(char1,char2)        

        player_won = False #ugly hack
        while char1.hp>0 and char2.hp>0 and self.round<=9:
            

            char1.attack(char2)
            if char2.hp==0:
                self.winner = char1
                player_won = True
                break
            
            char2.attack(char1)
            if char1.hp==0:
                self.winner = char2
                break
            
            self.round+=1
            self.battle_round(self.round)
            self.battle_stats(char1,char2)

        if self.winner!=None:
            print("\n" + "*"*30)
            print(f"          WINNER: {self.winner.name}")
            print(f"*"*30)
            # calculate reward
            if player_won==True:
                reward = self.char2.reward
                print(f"Player gained {reward} experience.")
                print(f"{self.char2.name} {self.char2._death_cry}")


        else: print(f"DRAW (no winner)")
        print("*"*20)

    def battle_round(self, round):
        print(f"*********** Round {round} **********")
        print(f"*"*30)

    def battle_stats(self, char1, char2):
        title="Names"
        print(f"{title:10}{char1.name:>10}{char2.name:>10}")
        title="HP"
        print(f"{title:10}{char1.hp:>10}{char2.hp:>10}")
        print(f"*"*30)
    
if __name__=="__main__":
    '''
    # Enemies              1  2    3   4         5     6     7     8
    #           name,      hp, mp, str,defense, speed, xp, level, reward
    e=Enemy("Goblin",      6,  0,  4,   2,      2,     0,    1,     1)

    # Players
    #           name,      hp, mp, str,defense, speed, xp, level, modifier
    h=Human(    "Bob",     8,  0,  5,   2,      4,     0,    1,     )
    w=Warrior(  "Thor",    10, 0,  6,   3,      3,     0,    1,     2)
    m=Mage(     "Gandolf", 7,  12, 4,   2,      2,     0,    1,     4)
    
    b=Battle(m,e)
    #print(f"MRO: {m.__class__.__mro__}") # inheritance chain
    # show subclasses. usign this we can choose random subclass of Monster.. 
    #print(f"subclasses {Character.__subclasses__()}") 
    '''

    enemies = load_data_from_json(settings, "enemy")
    goblin = enemies["goblin"]
    enemy = Enemy(**goblin)
    print(f"enemy name: {enemy.name}, hp: {enemy.hp}")

    players = load_data_from_json(settings)
    human = players["human"]
    player = Human(**players["human"])
    print(f"player name: {player.name}, hp: {player.hp}")

    b=Battle(player,enemy)