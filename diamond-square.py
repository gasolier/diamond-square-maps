import random
import numpy as np
import cv2


# these two functions are just for greater ease when using the program
# they make it so that I don't have to rewrite code to check indexes in
# the main functions
def return_wrap_values(y, x, grid):
    if y < 0:
        y = 0
    elif y >= len(grid):
        y = len(grid) - 1
    if x < 0:
        x = 0
    elif x >= len(grid):
        x = len(grid) - 1

    return grid[y][x]

def set_values(y, x, value, grid):
    if y < 0:
        y = 0
    elif y >= len(grid):
        y = len(grid) - 1
    if x < 0:
        x = 0
    elif x >= len(grid):
        x = len(grid) - 1

    grid[y][x] = value

    return grid

# this function just loops through the grid and calls the "steps" at different positions
def diamond_square(step_size, scale, grid):
    half_step = step_size // 2

    for y in range(half_step, len(hmap) + half_step, step_size):
        for x in range(half_step, len(hmap) + half_step, step_size):
            grid = square_step(y, x, step_size, random.uniform(-1, 1) * scale, grid)

    for y in range(0, len(hmap), step_size):
        for x in range(0, len(hmap), step_size):
            grid = diamond_step(y, x + half_step, step_size, random.uniform(-1, 1) * scale, grid)
            grid = diamond_step(y + half_step, x, step_size, random.uniform(-1, 1) * scale, grid)

    return grid

def diamond_step(y, x, size, value, grid):
    half_step = size // 2

    a = return_wrap_values(y, x - half_step, grid)
    b = return_wrap_values(y, x + half_step, grid)
    c = return_wrap_values(y - half_step, x, grid)
    d = return_wrap_values(y + half_step, x, grid)

    grid = set_values(y, x, ((a + b + c + d) / 4.0) + value, grid)

    return grid

def square_step(y, x, size, value, grid):
    half_step = size // 2

    a = return_wrap_values(y - half_step, x - half_step, grid)
    b = return_wrap_values(y + half_step, x - half_step, grid)
    c = return_wrap_values(y - half_step, x + half_step, grid)
    d = return_wrap_values(y + half_step, x + half_step, grid)

    grid = set_values(y, x, ((a + b + c + d) / 4.0) + value, grid)

    return grid

# create the heightmap, the size must be able to be represented as 2^n + 1
size = (2 ** int(input("Size (gives 2^n + 1): "))) + 1
sample_size = int(input("Feature size (powers of 2 seem to work the best): "))
scale = float(input("Starting scale (higher for more landmasses, lower for more sea): "))
hmap = np.zeros((size, size))

for y in range(size):
    for x in range(size):
        hmap[y][x] = random.uniform(-1, 1)

# main program loop
while sample_size > 1:
    hmap = diamond_square(sample_size, scale, hmap)
    sample_size //= 2
    scale /= 2

img_grid = np.empty((size, size, 3), int)
print(hmap)

# loop through the heightmap and add the colour values to the image
# the colours are given as BGR arrays, ie [255, 0, 0] creates a blue pixel
for y in range(size):
    for x in range(size):
        if hmap[y, x] < 0:
            img_grid[y, x] = [200, (60 + hmap[y, x] * 100), (60 + hmap[y, x] * 100)]
        elif hmap[y, x] < 0.7:
            img_grid[y, x] = [(hmap[y, x] * 100), 200, (hmap[y, x] * 100)]
        elif hmap[y, x] < 1.2:
            img_grid[y, x] = [(hmap[y, x] * 150), (hmap[y, x] * 150), (hmap[y, x] * 150)]
        else:
            img_grid[y, x] = [255, 255, 255]

cv2.imwrite("diamond_map.png", img_grid)
