import random
import typing as tp

import pygame
from pygame.locals import *

# TODO why is cell a tuple and not an int? 
# I guess for storing the amount of neighbors.. 
# but why are the type checks below (where cell is just an int) valid?
CellCord = tp.Tuple[int, int]
Creatures = tp.List[int]
Grid = tp.List[Creatures]

class GameOfLife:
    def __init__(
        self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10
    ) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_grid()
            self.draw_lines()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """ Создание списка клеток """
        if randomize:
            return [[random.choice((0, 1)) for _ in range(self.cell_width)] for _ in range(self.cell_height)]
        else:
            return [[0 for _ in range(self.cell_width)] for _ in range(self.cell_height)]


    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y, line in enumerate(self.grid):
            for x, creature in enumerate(line):
                color = 'green' if creature else 'white'
                s = self.cell_size
                pygame.draw.rect(
                    self.screen, 
                    pygame.Color(color), 
                    (x * s, self.height - y*s - s, s, s)
                )

    def get_neighbours(self, cell: CellCord) -> Creatures:
        """
        Вернуть список соседних клеток для клетки `cell`.
        """
        x, y = cell
        assumed_neighbors = [
            # Linter will break my beautiful code:
            # (x-1, y+1), (x, y+1), (x+1, y+1),
            # (x-1, y),             (x+1, y),
            # (x-1, y-1), (x, y-1), (x+1, y-1)
            (x-1, y+1), (x, y+1), (x+1, y+1),
            (x-1, y),             (x+1, y),
            (x-1, y-1), (x, y-1), (x+1, y-1)
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


if __name__ == '__main__':
    """
    game = GameOfLife(320, 240, 20)
    game.run()
    """
