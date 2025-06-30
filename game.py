import random
import json

# goal:
# create a character class where skills/benefits/hp are influenced by their race
# see pygame tut: https://python-forum.io/thread-401.html (9 parts, OOP later)

settings="settings.json"

def load_enemies_from_json(filepath):
    """Loads character data from a JSON file.""" 
    # later we could just load a single dict with players & enemies
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}.")
        return {}

    enemies = {}
    for category,enemy in data.items():
        if category=="enemy":
            enemies=enemy
    return enemies

def load_players_from_json(filepath):
    """Loads character data from a JSON file.""" 
    # later we could just load a single dict with players & enemies
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filepath}.")
        return {}

    players = {}
    for category,player in data.items():
        if category=="player":
            players=player
    return players
 
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
            print("health clamped at 0")
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

        pass
            
    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self,val):

        pass
    
    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self,val):

        pass

    @property
    def xp(self):
        return self._exp

    @xp.setter
    def xp(self,val):

        pass

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self,val):

        pass

    def take_damage(self, amount):
        #print(f"  {self.name} has {self.defense} defense")
        damage = amount - self.defense
        # print(f"  {self.name}'s attack of {amount} is reduced to {damage}")
        if damage<=0:
            #print("damange rounded to 0")
            damage=0
        self.hp-=damage
        print(f"  {self.name} takes {damage} damage")

        if(self.hp<=0):
            print(f"  {self.name} has been defeated!")

    def attack(self, target):
        print(f"{self.name} is attacking {target.name}")
        damage = random.randint(0,self.strength)
        target.take_damage(damage)

class Enemy(Character):
    def __init__(self, name, hp, mp, power, strength, defense, speed, xp, reward, death_cry, loot, level=1, **kwargs):
        super().__init__(name, hp, mp, power, strength, defense, speed, xp, level, **kwargs)

    #def __init__(self, name, hp, mp, strength, defense, speed, xp, level, **kwargs):

        self._reward = reward

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

class Elf(Character):
    def __init__(self, name, hp, mp, power, strength, defense, speed, xp, level=1,**kwargs):
        super().__init__(name, hp, mp, power, strength, defense, speed, xp, level, **kwargs)

    # modifier: +1 speed

class Dwarf(Character):
    def __init__(self, name, hp, mp, power, strength, defense, speed, xp, level=1, **kwargs):
        super().__init__(name, hp, mp, power, strength, defense, speed, xp, level, **kwargs)

        self.defense+=1
    # modifier: +1 defense

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

        while char1.hp>0 and char2.hp>0 and self.round<=9:
            
            char1.attack(char2)
            if char2.hp==0:
                self.winner = char1
                break
            
            char2.attack(char1)
            if char1.hp==0:
                self.winner = char2
                break
            
            self.round+=1
            self.battle_round(self.round)
            self.battle_stats(char1,char2)

        print("\n"+ "*"*20)
        if self.winner!=None:
            print(f"WINNER: {self.winner.name}")
            # calculate reward
            reward = self.char2.reward
            print(f"reward: {reward}")

        else: print(f"DRAW (no winner)")
        print("*"*20)

    def battle_round(self, round):
        print("\n" + "*"*30)
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

    enemies = load_enemies_from_json(settings)
    goblin = enemies["zmoch"]
    g = Enemy(**goblin)
    print(f"enemy name: {g.name}, hp: {g.hp}")

    enemies = load_enemies_from_json(settings)
    zmoch = enemies["goblin"]
    e = Enemy(**zmoch)
    print(f"enemy name: {e.name}, hp: {e.hp}")

    # players = load_players_from_json(settings)
    # #human = players["elf"]
    # elf = Enemy(**enemies["goblin"])
    # print(f"player name: {elf.name}, hp: {elf.hp}")

    b=Battle(g,e)