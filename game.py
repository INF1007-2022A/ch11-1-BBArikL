"""
Chapitre 11.1

Classes pour représenter un personnage.
"""

import random
from typing import Union

import utils


class Weapon:
    """
    Une arme dans le jeu.

    :param name: Le nom de l'arme
    :param power: Le niveau d'attaque
    :param min_level: Le niveau minimal pour l'utiliser
    """

    UNARMED_POWER = 20

    def __init__(self, name: str, power: int, min_level: int):
        self.__name = name
        self.power = power
        self.min_level = min_level

    @property
    def name(self):
        return self.__name

    @classmethod
    def make_unarmed(cls):
        return Weapon("Unarmed", Weapon.UNARMED_POWER, 1)


class Character:
    """
    Un personnage dans le jeu

    :param name: Le nom du personnage
    :param max_hp: HP maximum
    :param attack: Le niveau d'attaque du personnage
    :param defense: Le niveau de défense du personnage
    :param level: Le niveau d'expérience du personnage
    """
    CRIT_PROB = 1/16
    RANDOM_MODIFIER_RANGE = 0.15

    def __init__(self, name: str, max_hp: int, attack: int, defense: int, level: int):
        self.__name = name
        self.__hp = self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.level = level
        self.__weapon = Weapon.make_unarmed()

    @property
    def name(self):
        return self.__name

    @property
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, hp: Union[int, float]):
        self.__hp = utils.clamp(hp, 0, self.max_hp)

    @property
    def weapon(self):
        return self.__weapon

    @weapon.setter
    def weapon(self, new_weapon: Weapon):
        if new_weapon is None:
            self.__weapon = Weapon.make_unarmed()
        else:
            if new_weapon.min_level <= self.level:
                self.__weapon = new_weapon
            else:
                raise ValueError(
                    f"Cannot add a weapon of minimum level {new_weapon.min_level} to character of level {self.level}"
                )

    @staticmethod
    def calculate_damage(attacker_level, weapon_power, attack_power, defender_defense, crit_prob, rnd_factor):
        # Modifier
        crit = 2 if random.random() < crit_prob else 1
        random_mod = random.uniform(1-rnd_factor, 1)
        modifier = crit * random_mod

        level_factor = (((2 * attacker_level) / 5) + 2)
        attack_factor = (attack_power / defender_defense)

        dmg = ((((level_factor * weapon_power * attack_factor) / 50) + 2) * modifier)
        return dmg, crit == 2

    def compute_damage(self, target: "Character"):
        return self.calculate_damage(
            self.level,
            self.weapon.power,
            self.attack,
            target.defense,
            self.CRIT_PROB,
            self.RANDOM_MODIFIER_RANGE
        )


def deal_damage(attacker: Character, defender: Character):
    # TODO: Calculer dégâts
    damage, crit = attacker.compute_damage(defender)
    defender.hp -= damage

    print(f"{attacker.name} used {attacker.weapon.name}")
    if crit:
        print("\tCRITICAL HIT!")
    print(f"\t{defender.name} took {damage} dmg")


def run_battle(c1: Character, c2: Character):
    """Plays the game

    Parameters
    ----------
    c1 : Le premier personnage
    c2 : Le deuxième personnage

    Returns
    -------
    Le nombre de tours du jeu
    """
    # TODO: Initialiser attaquant/défendeur, tour, etc.
    tours = 0
    print(f"{c1.name} starts a battle with {c2.name}!")
    while c1.hp > 0 and c2.hp > 0:
        attacker, defender = (c1, c2) if tours % 2 == 0 else (c2, c1)
        deal_damage(attacker, defender)
        tours += 1

    dead_character = c1 if c1.hp <= 0 else c2

    print(f"{dead_character.name} is sleeping with the fishes.")

    return tours
