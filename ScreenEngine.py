import pygame
import collections
import Service
import Objects

colors = {
    "black": (42, 52, 44, 255),
    "white": (255, 255, 255, 255),
    "red": (214, 69, 65, 255),
    "green": (77, 175, 124, 255),
    "blue": (68, 108, 179, 255),
    "grey": (191, 191, 191, 255),
    "dark grey": (53, 59, 72, 255),
    "light grey": (189, 195, 199, 255),
    "yellow": (244, 208, 63, 255),
    "lavender": (148, 124, 176, 255)
}


class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["grey"])
        self.game_engine = None

    def connect_engine(self, engine):
        self.game_engine = engine
        if self.successor is not None:
            engine = self.game_engine
            return self.successor.connect_engine(engine)

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)


class GameSurface(ScreenHandle):

    def connect_engine(self, engine):
        self.game_engine = engine
        if self.successor is not None:
            engine = self.game_engine
            return self.successor.connect_engine(engine)

    def min_coord(self):
        size = self.game_engine.sprite_size
        map_size = len(self.game_engine.map)
        sprite_number_x = self.get_size()[0] // size
        sprite_number_y = self.get_size()[1] // size

        if self.game_engine.hero.position[0] < sprite_number_x // 2:
            min_x = 0
        elif self.game_engine.hero.position[0] > map_size - sprite_number_x // 2:
            min_x = map_size - sprite_number_x
        else:
            min_x = self.game_engine.hero.position[0] - sprite_number_x // 2

        if self.game_engine.hero.position[1] < sprite_number_y // 2:
            min_y = 0
        elif self.game_engine.hero.position[1] > map_size - sprite_number_y // 2:
            min_y = map_size - sprite_number_y
        else:
            min_y = self.game_engine.hero.position[1] - sprite_number_y // 2

        return min_x, min_y

    def draw_hero(self):
        self.game_engine.hero.draw(self, self.min_coord(), self.game_engine.sprite_size)

    def draw_map(self):

        min_x, min_y = self.min_coord()

        if self.game_engine.map:
            for i in range(len(self.game_engine.map[0]) - min_x):
                for j in range(len(self.game_engine.map) - min_y):
                    self.blit(self.game_engine.map[min_y + j][min_x + i][0],
                              (i * self.game_engine.sprite_size, j * self.game_engine.sprite_size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        size = self.game_engine.sprite_size

        min_x, min_y = self.min_coord()

        self.blit(sprite, ((coord[0] - min_x) * size,
                           (coord[1] - min_y) * size))

    def draw(self, canvas):
        size = self.game_engine.sprite_size

        min_x, min_y = self.min_coord()

        self.draw_map()
        for obj in self.game_engine.objects:
            self.blit(obj.sprite[0], ((obj.position[0] - min_x) * size,
                                      (obj.position[1] - min_y) * size))
        self.draw_hero()

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["grey"])

    def connect_engine(self, engine):
        self.game_engine = engine
        if self.successor is not None:
            engine = self.game_engine
            return self.successor.connect_engine(engine)

    def draw(self, canvas):
        self.fill(colors["grey"])
        pygame.draw.rect(self, colors["black"], (55, 35, 200, 30), 2)
        pygame.draw.rect(self, colors["black"], (55, 75, 200, 30), 2)

        if self.game_engine.hero.hp <= self.game_engine.hero.max_hp:
            max_xp_rectangle = 200 * self.game_engine.hero.hp / self.game_engine.hero.max_hp
        else:
            max_xp_rectangle = 200

        pygame.draw.rect(self, colors["red"], (55, 35, max_xp_rectangle, 30))
        pygame.draw.rect(self, colors["green"], (55, 75, 200 * self.game_engine.hero.exp /
                                                 (100 * (2**(self.game_engine.hero.level - 1))), 30))

        font = pygame.font.SysFont("gothici", 20)
        self.blit(font.render(f'Hero at {self.game_engine.hero.position}', True, colors["black"]),
                  (250, 3))

        self.blit(font.render(f'{self.game_engine.level} floor', True, colors["black"]),
                  (10, 3))

        self.blit(font.render(f'HP', True, colors["black"]),
                  (4, 40))
        self.blit(font.render(f'Exp', True, colors["black"]),
                  (4, 80))

        self.blit(font.render(f'{self.game_engine.hero.hp}/'
                              f'{self.game_engine.hero.max_hp}', True, colors["black"]),
                  (115, 40))
        self.blit(font.render(f'{self.game_engine.hero.exp}/'
                              f'{(100*(2**(self.game_engine.hero.level-1)))}', True, colors["black"]),
                  (115, 80))

        self.blit(font.render(f'Level', True, colors["black"]),
                  (280, 40))
        self.blit(font.render(f'Gold', True, colors["black"]),
                  (280, 80))

        self.blit(font.render(f'{self.game_engine.hero.level}', True, colors["black"]),
                  (350, 40))
        self.blit(font.render(f'{self.game_engine.hero.gold}', True, colors["black"]),
                  (350, 80))

        self.blit(font.render(f'Str', True, colors["black"]),
                  (390, 40))
        self.blit(font.render(f'Luck', True, colors["black"]),
                  (390, 80))

        self.blit(font.render(f'{self.game_engine.hero.stats["strength"]}', True, colors["black"]),
                  (460, 40))
        self.blit(font.render(f'{self.game_engine.hero.stats["luck"]}', True, colors["black"]),
                  (460, 80))

        self.blit(font.render(f'Score', True, colors["black"]),
                  (520, 40))
        self.blit(font.render(f'{self.game_engine.score:.4f}', True, colors["black"]),
                  (500, 80))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 20
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def connect_engine(self, engine):
        engine.subscribe(self)
        self.game_engine = engine
        if self.successor is not None:
            engine = self.game_engine
            return self.successor.connect_engine(engine)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill(colors["grey"])

        font = pygame.font.SysFont("gothice", 13)
        for i, text in enumerate(self.data):
            self.blit(font.render(text, True, colors["black"]),
                      (5, 20 + 18 * i))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)


class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Up"])
        self.data.append([" ↓ ", "Move Down"])
        self.data.append([" H ", "Show Help"])
        self.data.append([" S ", "Music Off/On"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" R ", "Restart Game"])
        self.data.append(["Esc", "Quit Game"])

    def connect_engine(self, engine):
        self.game_engine = engine
        if self.successor is not None:
            engine = self.game_engine
            return self.successor.connect_engine(engine)

    def draw(self, canvas):
        alpha = 0
        if self.game_engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))

        font1 = pygame.font.SysFont("serif", 20)
        font2 = pygame.font.SysFont("gothici", 20)

        if self.game_engine.show_help:
            pygame.draw.lines(self, colors["red"], True, [
                              (0, 0), (398, 0), (398, 398), (0, 398)], 6)
            for i, text in enumerate(self.data):
                if i <= 3:
                    self.blit(font1.render(text[0], True, colors["white"]),
                              (75, 55 + 30 * i))
                else:
                    self.blit(font2.render(text[0], True, colors["white"]),
                              (60, 55 + 30 * i))
                self.blit(font2.render(text[1], True, colors["white"]),
                          (190, 55 + 30 * i))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)


class MiniMap(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def connect_engine(self, engine):
        self.game_engine = engine
        if self.successor is not None:
            engine = self.game_engine
            return self.successor.connect_engine(engine)

    def draw(self, canvas):
        pygame.draw.rect(self, colors["light grey"], (0, 0, 200, 200))

        wall_sq = pygame.Surface((10, 10))
        wall_sq.fill(colors["dark grey"])
        pygame.draw.lines(wall_sq, colors["black"], True, [
            (0, 0), (9, 0), (9, 9), (0, 9)], 1)

        hero_cl = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(hero_cl, colors["lavender"], (5, 5), 5)

        enemy_cl = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(enemy_cl, colors["red"], (5, 5), 5)

        ally_cl = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(ally_cl, colors["green"], (5, 5), 5)

        stairs_cl = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(stairs_cl, colors["blue"], (5, 5), 5)

        chest_cl = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(chest_cl, colors["yellow"], (5, 5), 5)

        self.blit(hero_cl, (self.game_engine.hero.position[0] * 10,
                            self.game_engine.hero.position[1] * 10))

        if self.game_engine.map:
            for i in range(len(self.game_engine.map[0])):
                for j in range(len(self.game_engine.map)):
                    if self.game_engine.map[i][j] == Service.wall:
                        self.blit(wall_sq, (j * 10, i * 10))

        else:
            self.fill(colors["white"])

        for object_ in self.game_engine.objects:
            if isinstance(object_, Objects.Enemy):
                self.blit(enemy_cl, (object_.position[0] * 10,
                                     object_.position[1] * 10))
            else:
                if object_.name == "stairs":
                    self.blit(stairs_cl, (object_.position[0] * 10,
                                          object_.position[1] * 10))
                elif object_.name == "chest":
                    self.blit(chest_cl, (object_.position[0] * 10,
                                         object_.position[1] * 10))
                elif object_.name == "bless" or "remove" or "heal":
                    self.blit(ally_cl, (object_.position[0] * 10,
                                        object_.position[1] * 10))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)


class GameOverWindow(ScreenHandle):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = []
        self.data.append("GAME OVER")
        self.data.append("Press R to play again")
        self.data.append("or ESC to quit the game")

    def connect_engine(self, engine):
        self.game_engine = engine
        if self.successor is not None:
            engine = self.game_engine
            return self.successor.connect_engine(engine)

    def draw(self, canvas):
        alpha = 0
        font = pygame.font.SysFont("gothici", 24)
        if self.game_engine.game_over:
            alpha = 128
        self.fill((0, 0, 0, alpha))

        if self.game_engine.game_over:
            pygame.draw.lines(self, colors["red"], True, [
                              (0, 0), (498, 0), (498, 298), (0, 298)], 6)
            self.blit(font.render(self.data[0], True, colors["white"]),
                      (150, 60))
            self.blit(font.render(self.data[1], True, colors["white"]),
                      (92, 140))
            self.blit(font.render(self.data[2], True, colors["white"]),
                      (80, 200))

        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)








