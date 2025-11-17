from random import choice, randint

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> list[list[str | int]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: list[list[str | int]], coord: tuple[int, int]) -> list[list[str | int]]:
    y, x = coord
    y_remove, x_remove = y, x
    cols = len(grid[0])

    decision = choice(("up", "right"))
    if decision == "up" and 0 <= y - 2:
        y_remove, x_remove = y - 1, x
    else:
        decision = "right"

    if decision == "right" and x + 2 < cols - 1:
        y_remove, x_remove = y, x + 1
    elif 0 <= y - 2 and x < cols - 1:
        y_remove, x_remove = y - 1, x

    grid[y_remove][x_remove] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> list[list[str | int]]:
    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for cell in empty_cells:
        grid = remove_wall(grid, cell)

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: list[list[str | int]]) -> list[tuple[int, int]]:
    """Find a couple of positions with X, NOTE: the test expects coordinates like (y, x)"""
    exits = []
    for y, row in enumerate(grid):
        for x, s in enumerate(row):
            if s == "X":
                exits.append((y, x))
    return exits


def make_step(grid: list[list[str | int]], k: int) -> list[list[str | int]]:
    """Find the first cell that contains k, fill empty cells around it with k+1"""
    rows = len(grid)
    cols = len(grid[0])
    for y, row in enumerate(grid):
        for x, s in enumerate(row):
            if s == k:
                k += 1
                for fill_x, fill_y in [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]:
                    if fill_x in range(0, cols) and fill_y in range(0, rows):
                        if grid[fill_y][fill_x] == 0:
                            grid[fill_y][fill_x] = k
                k -= 1

    return grid


def shortest_path(
    grid: list[list[str | int]], exit_coord: tuple[int, int]
) -> tuple[int, int] | list[tuple[int, int]] | None:
    """Once the numbers have been filled in, find the shortest path"""
    rows = len(grid)
    cols = len(grid[0])

    y, x = exit_coord
    k = int(grid[y][x])
    path = [(y, x)]
    while grid[y][x] != 1:
        for check_x, check_y in [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]:
            if check_x in range(0, cols) and check_y in range(0, rows):
                if grid[check_y][check_x] == k - 1:
                    path.append((check_y, check_x))
                    k -= 1
                    x, y = check_x, check_y
                    break

    return path


def encircled_exit(grid: list[list[str | int]], coord: tuple[int, int]) -> bool:
    """NOTE: the coordinates are passed in incorrect format (y, x)"""
    rows = len(grid)
    cols = len(grid[0])
    y, x = coord

    # In a corner
    if (x, y) in [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]:
        return True

    # Blocked: up, right, down, left
    if (
        (y == 0 and grid[y + 1][x] != " ")
        or (x == cols - 1 and grid[y][x - 1] != " ")
        or (y == rows - 1 and grid[y - 1][x] != " ")
        or (x == 0 and grid[y][x + 1] != " ")
    ):
        return True

    return False


def solve_maze(
    grid: list[list[str | int]],
) -> tuple[list[list[str | int]], tuple[int, int] | list[tuple[int, int]] | None]:
    """Main function for solving a maze"""
    exits = get_exits(grid)

    if len(set(exits)) == 1:
        return grid, exits[0]

    for exit_pos in exits:
        if encircled_exit(grid, exit_pos):
            return grid, None

    # NOTE I have to invert the coordinates because of the test
    (y_in, x_in), (y_out, x_out) = exits

    grid[y_in][x_in] = 1
    grid[y_out][x_out] = 0

    for y, row in enumerate(grid):
        for x, s in enumerate(row):
            if s == " ":
                grid[y][x] = 0

    k = 0
    while grid[y_out][x_out] == 0:
        k += 1
        grid = make_step(grid, k)

    path = shortest_path(grid, (y_out, x_out))
    return grid, path


def add_path_to_grid(
    grid: list[list[str | int]], path: tuple[int, int] | list[tuple[int, int]] | None
) -> list[list[str | int]]:
    if path:
        for y, row in enumerate(grid):
            for x, _ in enumerate(row):
                if (y, x) in path:
                    grid[y][x] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
