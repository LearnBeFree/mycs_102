import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        self.rows, self.cols = size
        self.prev_generation = self.create_grid()
        self.curr_generation = self.create_grid(randomize=randomize)
        self.max_generations = max_generations
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        if randomize:
            return [[random.choice((0, 1)) for _ in range(self.cols)] for _ in range(self.rows)]
        else:
            return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def get_neighbours(self, cell: Cell) -> Cells:
        x, y = cell
        assumed_neighbors = [
            # Linter will want to break my beautiful code:
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
                    neighbors_creatures.append(self.curr_generation[y_n][x_n])
                except IndexError:
                    continue

        return neighbors_creatures

    def get_next_generation(self) -> Grid:
        new_grid = self.create_grid()
        for y, line in enumerate(self.curr_generation):
            for x, creature in enumerate(line):
                if creature:
                    # NOTE tests have incorrect cords ordering, reversing
                    if sum(self.get_neighbours((y, x))) in (2, 3):
                        new_grid[y][x] = creature
                elif sum(self.get_neighbours((y, x))) == 3:
                    new_grid[y][x] = 1

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False

        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.prev_generation != self.curr_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        grid = []
        with open(filename) as f:
            for line in f:
                line = line.rstrip("\n")
                if "0" in line or "1" in line:
                    grid.append([int(n) for n in list(line)])

        game = GameOfLife((len(grid), len(grid[0])), False)
        game.curr_generation = grid

        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        lines_str = ["".join([str(c) for c in line]) for line in self.curr_generation]
        grid_str = "\n".join(lines_str)
        with open(filename, "w") as f:
            f.write(grid_str)
