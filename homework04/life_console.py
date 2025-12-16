import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.CELL_WIDTH = 3
        self.CELL_HEIGHT = 2

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        grid_ch_width = self.life.cols * self.CELL_WIDTH + 2
        grid_ch_height = self.life.rows * self.CELL_HEIGHT + 2
        top_bottom_row_str = (grid_ch_width) * " "
        color_pair = curses.color_pair(3)
        for ch_y in (0, grid_ch_height - 1):
            screen.addstr(ch_y, 0, top_bottom_row_str, color_pair)

        for ch_y in range(1, grid_ch_height - 1):
            for ch_x in (0, grid_ch_width - 1):
                screen.addstr(ch_y, ch_x, " ", color_pair)

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        for cell_y, line in enumerate(self.life.curr_generation):
            for cell_x, creature in enumerate(line):
                color_pair = curses.color_pair(2) if creature == 1 else curses.color_pair(1)
                ch_x = 1 + cell_x * self.CELL_WIDTH
                for cell_row_n in range(self.CELL_HEIGHT):
                    ch_y = 1 + cell_y * self.CELL_HEIGHT + cell_row_n
                    row_str = " " * self.CELL_WIDTH
                    screen.addstr(ch_y, ch_x, row_str, color_pair)

    def want_to_quit(self, screen) -> bool:
        try:
            ch = screen.getch()
            answer = True if ch == ord("q") else False
        except curses.error:
            answer = False

        return answer

    def run(self) -> None:
        screen = curses.initscr()
        screen.timeout(100)  # screen.getch() will not block the code. Instead, it will wait for 100 ms

        curses.curs_set(0)  # make the cursor invisible
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_YELLOW)

        maxy, maxx = screen.getmaxyx()
        max_rows = maxy // self.CELL_HEIGHT - 2
        max_cols = maxx // self.CELL_WIDTH - 2
        if self.life.rows > max_rows or self.life.cols > max_cols:
            curses.endwin()
            print("Your terminal window is too small for specified game size")
        else:
            self.draw_grid(screen)
            self.draw_borders(screen)
            time.sleep(1)
            while self.life.is_changing and not self.life.is_max_generations_exceeded and not self.want_to_quit(screen):
                self.life.step()
                screen.erase()
                self.draw_grid(screen)
                self.draw_borders(screen)
                time.sleep(1)

            curses.endwin()
            print("It's time to stop playing games!")


if __name__ == "__main__":
    life = GameOfLife((10, 10), max_generations=50)
    ui = Console(life)
    ui.run()
