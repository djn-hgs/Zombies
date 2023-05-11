import pygame
import time
import copy
import random

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

# Declare our grid

grid = []

# Work across the rows one after another

for y in range(grid_height - len(grid)):
    grid.append([])

for row in grid:
    for x in range(grid_width - len(row)):
        row.append(0)

# This creates a loop that only ends when you close the window

still_looping = True

while still_looping:

    # This looks to see whether the close button has been pressed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still_looping = False

    # Clear the screen

    my_screen.fill((100, 100, 150))

    # Work across the rows, one after another

    for y in range(grid_height):
        for x in range(grid_width):

            # Displaying a grid of random colours

            my_color = alive_color

            if grid[y][x] == 0:
                my_color = dead_color
            if random.random() > 0.9:
                grid[y][x] = 1 - grid[y][x]

            pygame.draw.rect(my_screen, my_color,
                             (grid_x + box_width * x, grid_y + box_height * y, box_width, box_height), 0)

    # Show off our handiwork

    pygame.display.update()

    # Take a breath to see what is going on

    time.sleep(0.5)

# Finish things off
pygame.quit()