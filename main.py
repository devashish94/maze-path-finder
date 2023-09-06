import sys
import time
import pygame as pg
import tkinter as tk

game_start = False

# ---------------------------------------------------------------------- #
root = tk.Tk()
root.geometry('500x500')
root.title("Radio Button Example")

values = ['3x3', '10x10', '25x25', '50x50', '100x100']
var = tk.StringVar()
res_var = tk.StringVar(root)
res_var.set(values[0])  # Set the default value

WIDTH, HEIGHT = 800, 800
GRID_SIZE = 10

starting_row, starting_col = 0, 0
ending_row, ending_col = 0, 0


def selection_changed(event):
    global GRID_SIZE
    selected_value = res_var.get().split('x')[0]
    print(selected_value)
    GRID_SIZE = WIDTH // int(selected_value)


def handle_on_value():
    global starting_row, starting_col, ending_row, ending_col
    global game_start
    game_start = True
    starting_row, starting_col = [int(i) for i in entry1.get().split(',')]
    ending_row, ending_col = [int(i) for i in entry2.get().split(',')]
    root.destroy()


dropdown = tk.OptionMenu(root, res_var, *values, command=selection_changed)
radio_button1 = tk.Radiobutton(root, text="DFS", variable=var, value="d")
radio_button2 = tk.Radiobutton(root, text="BFS", variable=var, value="b")
show_button = tk.Button(root, text="Start Visualizer", command=handle_on_value)
label1 = tk.Label(root, text="Enter starting point")
entry1 = tk.Entry(root)
label2 = tk.Label(root, text="Enter ending point")
entry2 = tk.Entry(root)

radio_button1.pack()
radio_button2.pack()
dropdown.pack()
label1.pack()
label2.pack()
entry1.pack()
entry2.pack()
show_button.pack()

root.mainloop()
# ---------------------------------------------------------------------- #

sys.setrecursionlimit(5000)

print(f'Resolution: {WIDTH // GRID_SIZE} x {HEIGHT // GRID_SIZE}')

if game_start:
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))

pg.display.set_caption('Visualizer')

starting_color = pg.Color('purple')
ending_color = pg.Color('violet')
point_color = pg.Color('green')

start_point = 'S'
target_point = 'T'
set_point = 'O'
visited_point = 'V'

grid = [['X' for _ in range(WIDTH // GRID_SIZE)] for _ in range(HEIGHT // GRID_SIZE)]

running = True
done = False


def draw_cell(grid):
    for x in range(0, WIDTH, GRID_SIZE):
        pg.draw.line(screen, pg.Color('black'), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pg.draw.line(screen, pg.Color('black'), (0, y), (WIDTH, y))


def color_cell(grid):
    for row in range(len(grid)):
        for col in range(len(grid[row])):

            if grid[row][col] == 'S':
                colored_cell = pg.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pg.draw.rect(screen, pg.Color('violet'), colored_cell)

            if grid[row][col] == 'T':
                colored_cell = pg.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pg.draw.rect(screen, pg.Color('purple'), colored_cell)

            if grid[row][col] == 'O':
                colored_cell = pg.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pg.draw.rect(screen, pg.Color('green'), colored_cell)

            if grid[row][col] == 'V':
                colored_cell = pg.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pg.draw.rect(screen, pg.Color('pink'), colored_cell)

            if grid[row][col] == 'D':
                colored_cell = pg.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pg.draw.rect(screen, pg.Color('blue'), colored_cell)

            if grid[row][col] == 'B':
                colored_cell = pg.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                pg.draw.rect(screen, pg.Color('purple'), colored_cell)


# starting_row, starting_col = [int(i) for i in input('Enter starting: ').split()]
# ending_row, ending_col = [int(i) for i in input('Enter ending: ').split()]

grid[starting_row][starting_col] = start_point
grid[ending_row][ending_col] = target_point

# mode = input('Enter the type of search between BFS and DFS (b/d): ')

start = False


def get_values(arr, type):
    for i in range(len(arr)):
        for j in range(len(arr[i])):
            if arr[i][j] == type:
                return [i, j]
    return [0, 0]


visited = []


def f(arr, row, col, target, path, save: list[list[int]]):
    # time.sleep(1000 / 1000)
    global start

    if arr[row][col] == target:
        print('FOUND', row, col)
        start = False
        return

    columns = len(arr[row])
    up = (row - 1) * columns + col
    down = (row + 1) * columns + col
    left = row * columns + (col - 1)
    right = row * columns + (col + 1)

    if start:
        print('Coordinates:', row, col, '<=', len(arr[row]))
        arr[row][col] = 'D'
        color_cell(arr)
        draw_cell(arr)
        pg.display.flip()
        if col + 1 < len(arr[row]) and arr[row][col + 1] != 'O' and right not in visited:
            visited.append(right)
            arr[row][col] = 'V'
            f(arr, row, col + 1, target, path + [[row, col]], save)
            arr[row][col] = 'B'

        if row + 1 < len(arr) and arr[row + 1][col] != 'O' and down not in visited:
            visited.append(down)
            arr[row][col] = 'V'
            f(arr, row + 1, col, target, path + [[row, col]], save)
            arr[row][col] = 'B'

        if col - 1 >= 0 and arr[row][col - 1] != 'O' and left not in visited:
            visited.append(left)
            arr[row][col] = 'V'
            f(arr, row, col - 1, target, path + [[row, col]], save)
            arr[row][col] = 'B'

        if row - 1 >= 0 and arr[row - 1][col] != 'O' and up not in visited:
            visited.append(up)
            arr[row][col] = 'V'
            f(arr, row - 1, col, target, path + [[row, col]], save)
            arr[row][col] = 'B'


def bfs(arr):
    row, col = get_values(grid, start_point)
    fx, fy = get_values(grid, target_point)
    target = 'T'
    columns: int = len(arr[row])

    q: list[int] = [row * columns + col]
    v: list[int] = []

    while len(q) != 0:
        # time.sleep(20 / 1000)
        value: int = q.pop(0)
        x, y = value // columns, value % columns

        arr[x][y] = 'D'
        color_cell(grid)
        draw_cell(grid)
        pg.display.flip()

        if x == fx and y == fy:
            print(f'Found {target} at ({x}, {y})')
            global start
            start = False
            draw_cell(grid)
            return

        arr[x][y] = 'V'

        if value in v:
            continue

        v.append(value)

        up = (x - 1) * columns + y
        down = (x + 1) * columns + y
        left = x * columns + (y - 1)
        right = x * columns + (y + 1)

        if x - 1 >= 0 and up not in v and arr[x - 1][y] != 'O':
            q.append(up)
        if x + 1 < len(arr) and down not in v and arr[x + 1][y] != 'O':
            q.append(down)
        if y - 1 >= 0 and left not in v and arr[x][y - 1] != 'O':
            q.append(left)
        if y + 1 < len(arr[x]) and right not in v and arr[x][y + 1] != 'O':
            q.append(right)
        # arr[row][col] = 'D'

    draw_cell(grid)
    start = False


def dfs(arr):
    global start
    start_x, start_y = get_values(grid, start_point)
    save: list[list] = []

    print('starting path finding...')
    f(arr, start_x, start_y, target_point, [], save)
    print('done...')

    for path in save:
        print(path)

    start = False


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if pg.mouse.get_pressed()[2]:
            x, y = pg.mouse.get_pos()
            grid[y // GRID_SIZE][x // GRID_SIZE] = set_point
            print(y // GRID_SIZE, x // GRID_SIZE)
        if pg.mouse.get_pressed()[1]:
            print('pressed')
            start = True

    if start:
        x = var.get()
        # if mode == 'b':
        #     bfs(grid)
        # elif mode == 'd':
        #     dfs(grid)
        if x == 'b':
            bfs(grid)
        elif x == 'd':
            dfs(grid)
        grid[starting_row][starting_col] = start_point
        grid[ending_row][ending_col] = target_point

    screen.fill(pg.Color('white'))

    color_cell(grid)
    draw_cell(grid)

    pg.display.flip()

pg.quit()
sys.exit()
