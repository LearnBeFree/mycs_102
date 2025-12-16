import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 20, speed: int = 10) -> None:
        super().__init__(life)
        self.width = self.life.cols * cell_size
        self.height = self.life.rows * cell_size
        self.cell_size = cell_size

        # Создание нового окна
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for y, line in enumerate(self.life.curr_generation):
            for x, creature in enumerate(line):
                color = 'green' if creature else 'white'
                s = self.cell_size
                pygame.draw.rect(
                    self.screen, 
                    pygame.Color(color), 
                    (x * s, self.height - y*s - s, s, s)
                )

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        paused = False

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused


            self.draw_grid()
            self.draw_lines()
            
            if not paused:
                self.life.step()
                running = self.life.is_changing and not self.life.is_max_generations_exceeded
            else:
                # keep running unless stopped by user or other condition
                running = running and not self.life.is_max_generations_exceeded

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

if __name__ == '__main__':
    life = GameOfLife((10, 10), max_generations=50)
    ui = GUI(life)
    ui.run()

