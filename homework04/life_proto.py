"""
Qulick prototype for the game of life
"""

import random
import typing as tp

import pygame
from pygame.locals import *

CellCord = tp.Tuple[int, int]
Creatures = tp.List[int]
Grid = tp.List[Creatures]


class GameOfLife:
    """Main GameOfLife class"""

    def __init__(self, w: int = 640, h: int = 480, s: int = 10, speed: int = 10) -> None:
        self.width = w
        self.height = h
        self.cell_size = s

        # Устанавливаем размер окна
        self.screen_size = w, h
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """Создание списка клеток"""
        if randomize:
            return [[random.choice((0, 1)) for _ in range(self.cell_width)] for _ in range(self.cell_height)]

        return [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y, line in enumerate(self.grid):
            for x, creature in enumerate(line):
                color = "green" if creature else "white"
                s = self.cell_size
                pygame.draw.rect(self.screen, pygame.Color(color), (x * s, self.height - y * s - s, s, s))

    def get_neighbours(self, cell: CellCord) -> Creatures:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток, в котором каждая позиция – 0 или 1.
        """
        x, y = cell
        assumed_neighbors = [
            # Linter will break my beautiful code:
            # (x-1, y+1), (x, y+1), (x+1, y+1),
            # (x-1, y),             (x+1, y),
            # (x-1, y-1), (x, y-1), (x+1, y-1)
            (x - 1, y + 1),
            (x, y + 1),
            (x + 1, y + 1),
            (x - 1, y),
            (x + 1, y),
            (x - 1, y - 1),
            (x, y - 1),
            (x + 1, y - 1),
        ]
        neighbors_creatures = []
        for assumed_neighbor in assumed_neighbors:
            # NOTE tests have incorrect cords ordering, reversing
            y_n, x_n = assumed_neighbor
            if x_n >= 0 and y_n >= 0:
                try:
                    neighbors_creatures.append(self.grid[y_n][x_n])
                except IndexError:
                    continue

        return neighbors_creatures

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        """
        new_grid = self.create_grid()
        for y, line in enumerate(self.grid):
            for x, creature in enumerate(line):
                if creature:
                    # NOTE tests have incorrect cords ordering, reversing
                    if sum(self.get_neighbours((y, x))) in (2, 3):
                        new_grid[y][x] = creature
                elif sum(self.get_neighbours((y, x))) == 3:
                    new_grid[y][x] = 1

        return new_grid


if __name__ == "__main__":
    game = GameOfLife(320, 240, 20)
    game.run()
