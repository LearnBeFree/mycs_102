"""
That is a GUI for my game
"""

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    """Main GUI class"""

    def __init__(self, life: GameOfLife, cell_size: int = 20, speed: int = 5) -> None:
        super().__init__(life)
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.cell_size = cell_size

        # Создание нового окна
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def _draw_rect(self, x: int, y: int, creature: int) -> None:
        color = "green" if creature else "white"
        s = self.cell_size
        pygame.draw.rect(self.screen, pygame.Color(color), (x * s, self.height - y * s - s, s, s))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y, line in enumerate(self.life.curr_generation):
            for x, creature in enumerate(line):
                self._draw_rect(x, y, creature)

    def _reverse_state(self, pos: tuple[int, int]) -> None:
        """Kill a creature if exists, delete a creature if does not"""
        x_screen, y_screen = pos
        x = x_screen // self.cell_size
        y = self.life.rows - y_screen // self.cell_size - 1
        creature = int(not self.life.curr_generation[y][x])
        self._draw_rect(x, y, creature)
        self.life.curr_generation[y][x] = creature

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        paused = False

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                elif event.type == pygame.MOUSEBUTTONDOWN and paused:
                    pos = event.pos
                    self._reverse_state(pos)

            self.draw_grid()
            self.draw_lines()

            if not paused:
                self.life.step()
                running = self.life.is_changing and not self.life.is_max_generations_exceeded
            else:
                running = running and not self.life.is_max_generations_exceeded

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


if __name__ == "__main__":
    life_instance = GameOfLife((10, 10), max_generations=50)
    ui = GUI(life_instance)
    ui.run()
