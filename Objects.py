from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class AbstractObject(ABC):
    @abstractmethod
    def __init__(self, icon, position):
        self.sprite = icon
        self.position = position

    def draw(self, display, min_coord, sprite_size):
        display.blit(self.sprite,
                     ((self.position[0] - min_coord[0]) * sprite_size,
                      (self.position[1] - min_coord[1]) * sprite_size))


class Ally(AbstractObject, Interactive):

    def __init__(self, name, icon, action, position):
        self.name = name
        self.sprite = icon
        self.action = action
        self.position = position

    def interact(self, engine, hero):
        self.action(engine, hero)


class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.stats = stats
        self.position = position
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2


class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, xp, position):
        super().__init__(icon, stats, position)
        self.xp = xp

# FIXME
    def interact(self, engine, hero):
        if random.randint(0, 50) <= hero.stats["luck"]:
            engine.notify("The enemy is asleep")
        else:
            hero.hp = int(hero.hp - self.stats["strength"] * 5)
            engine.score += 0.1
        if hero.hp <= 0:
            hero.hp = 0
            engine.game_over = True
        else:
            hero.exp = int(hero.exp + self.xp)
            hero.level_up()
            engine.notify("Level up!")


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = (0, 0)
        super().__init__(icon, stats, pos)
        self.level = 1
        self.exp = 0
        self.gold = 0

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):
    def apply_effect(self):
        self.hp += 50
        self.stats["strength"] += 7
        self.stats["endurance"] += 7
        self.stats["intelligence"] -= 3
        self.stats["luck"] += 7


class Blessing(Effect):
    def apply_effect(self):
        self.stats["strength"] += 2
        self.stats["endurance"] += 2
        self.stats["intelligence"] += 2
        self.stats["luck"] += 2


class Weakness(Effect):
    def apply_effect(self):
        self.stats["strength"] -= 4
        self.stats["endurance"] -= 4


class CatPower(Effect):
    def apply_effect(self):
        self.stats["intelligence"] -= 5
        self.stats["luck"] += 10
