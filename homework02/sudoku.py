"""
Sudoku solving program.
"""

import pathlib
import typing as tp
from random import randint

T = tp.TypeVar("T")


def read_sudoku(path: str | pathlib.Path) -> list[list[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> list[list[str]]:
    """
    Create grid function
    """
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: list[list[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print("".join(grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)))
        if str(row) in "25":
            print(line)
    print()


def group(values: list[T], n: int) -> list[list[T]]:
    """Group values into groups of n"""

    length = len(values)
    newls: list[list[T]] = [[el for i, el in enumerate(values) if i // n == group_i] 
                            for group_i in range(length // n)]

    return newls


def get_row(grid: list[list[str]], pos: tuple[int, int]) -> list[str]:
    """Возвращает все значения для номера строки, указанной в pos"""

    return grid[pos[0]]


def get_col(grid: list[list[str]], pos: tuple[int, int]) -> list[str]:
    """Возвращает все значения для номера столбца, указанного в pos"""

    return [grid[i][pos[1]] for i in range(len(grid))]



def get_block(grid: list[list[str]], pos: tuple[int, int]) -> list[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos"""
    blocky = pos[0] // 3
    blockx = pos[1] // 3
    newls = []

    for y, line in enumerate(grid):
        for x, i in enumerate(line):
            if y // 3 == blocky and x // 3 == blockx:
                newls.append(i)

    return newls


def find_empty_positions(grid: list[list[str]]) -> tuple[int, int] | None:
    """Найти первую свободную позицию в пазле"""
    for y, line in enumerate(grid):
        for x, i in enumerate(line):
            if i == ".":
                return (y, x)

    return None


def find_possible_values(grid: list[list[str]], pos: tuple[int, int]) -> set[str]:
    """Вернуть множество возможных значения для указанной позиции"""
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)
    newset = set()

    for n in "123456789":
        if n not in row + col + block:
            newset.add(n)

    return newset


def solve(grid: list[list[str]]) -> list[list[str]] | None:
    """Решение пазла, заданного в grid"""
    pos = find_empty_positions(grid)
    if not pos:
        return grid

    values = find_possible_values(grid, pos)
    if not values:
        return None

    y, x = pos
    for n in values:
        grid[y][x] = n
        solved_grid = solve(grid)

        if not solved_grid:
            grid[y][x] = "."
            continue
        else:
            return solved_grid

    return None


def check_solution(solution: list[list[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    for y, line in enumerate(solution):
        for x, n in enumerate(line):
            if n == ".":
                return False

            pos = (y, x)
            row = get_row(solution, pos)
            col = get_col(solution, pos)
            block = get_block(solution, pos)

            if not(row.count(n) == col.count(n) == block.count(n) == 1):
                return False

    return True


def generate_sudoku(N: int) -> list[list[str]]:
    """Генерация судоку заполненного на N элементов"""
    grid = [["." for _ in range(9)] for _ in range(9)]

    # Заполнить центральный квадрат случайным образом
    numbers: list[int] = []
    while len(numbers) != 9:
        n = randint(1, 9)
        if n not in numbers:
            numbers.append(n)

    for y, line in enumerate(grid):
        for x, item in enumerate(grid):
            if y // 3 == x // 3 == 1:
                grid[y][x] = str(numbers[-1])
                numbers.pop()

    # Решить судоку уже имеющимся алгоритмом
    # (We need tp.cast because the solve() function can return None)
    grid = tp.cast(list[list[str]], solve(grid))

    # Случайно вычеркнуть 81-N элементов
    toremove = 81 - N
    removed = []
    pos = (randint(0, 8), randint(0, 8))

    for _ in range(toremove):
        while pos in removed:
            pos = (randint(0, 8), randint(0, 8))

        y, x = pos
        grid[y][x] = "."
        removed.append(pos)

    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
