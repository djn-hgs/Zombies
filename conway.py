import copy
import time
import pygame

# Get things up and running

pygame.init()

# Create a window where stuff can happen

my_screen = pygame.display.set_mode((800, 600), 5)

# Our grid's width and height

grid_width = 100
grid_height = 50

# The position and size of the boxes used to display the grid

box_width = 8
box_height = 12

grid_x = 0
grid_y = 0

# Colour of the boxes on the grid

dead_color = (100, 100, 100)  # Colour for Dead
alive_color = (0, 50, 0)  # Colour for Alive

# Create a specific pattern. This is a "glider".

grid = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 1]
]

# This bit makes sure that our grid is the right size

if len(grid) > grid_height:
    grid_height = len(grid)
for row in grid:
    if len(row) > grid_width:
        grid_width = len(row)

if len(grid) < grid_height:
    grid += [[] for i in range(grid_height - len(grid))]

for row in grid:
    if len(row) < grid_width:
        row += [0 for i in range(grid_width - len(row))]

# How to find the neighbours of a cell...

neighbor_list = []

for j in [-1, 0, 1]:
    for i in [-1, 0, 1]:
        if not (i == 0 and j == 0):
            neighbor_list.append((i, j))

# This creates a loop that only ends when you close the window

still_looping = True

while still_looping:

    # This looks to see whether the close button has been pressed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still_looping = False

    # Clear the screen

    my_screen.fill((100, 100, 150))

    # Create a working copy of our grid so that we can iterate

    ref_grid = copy.deepcopy(grid)

    # Now let's iterate

    for y in range(grid_height):
        for x in range(grid_width):

            # Start by displaying the current state

            my_cell = grid[y][x]

            if my_cell == 0:
                my_color = dead_color
            if my_cell == 1:
                my_color = alive_color

            pygame.draw.rect(my_screen, my_color,
                             (grid_x + box_width * x, grid_y + box_height * y, box_width, box_height), 0)

            # Counter for neighbours

            neighbor_count = 0

            # Work through neighbours

            for (i, j) in neighbor_list:
                neighbor_x = x + i
                neighbor_y = y + j

                # As long as they are on the grid!

                if neighbor_x >= 0 and neighbor_y >= 0 and neighbor_x < grid_width and neighbor_y < grid_height:

                    # If so then count whether they are alive...
                    if ref_grid[neighbor_y][neighbor_x] > 0:
                        neighbor_count = neighbor_count + 1

            # Get the current cell value

            cell_val = ref_grid[y][x]

            # Then iterate according to Conway's rules

            # If dead with three neighbours then come to life

            if cell_val == 0 and neighbor_count == 3:
                cell_val = 1

            # If alive...

            if cell_val == 1:

                # ...with fewer than two neighbours then die

                if neighbor_count < 2:
                    cell_val = 0

                # ...with two or three neighbours then stay alive

                if neighbor_count == 2 or neighbor_count == 3:
                    cell_val = 1

                # ...with  more than three neighbours then die

                if neighbor_count > 3:
                    cell_val = 0

            # Update the grid

            grid[y][x] = cell_val

    # Show off our handiwork

    pygame.display.update()

    # Take a breath to see what is going on

    # time.sleep( 0.5 )

# Finish things off
pygame.quit()
