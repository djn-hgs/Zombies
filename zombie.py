import copy, time, pygame, sys, random

# Get things up and running

pygame.init()

# Create a window where stuff can happen

my_screen = pygame.display.set_mode((800, 600), 5)

# Load a font so that we can write something

# my_font = pygame.font.SysFont( 'monospace' , 36 )

# Our grid's width and height

w = 100
h = 50

# The position and size of the boxes used to display the grid

b_width = 8
b_height = 12

g_x = 0
g_y = 0

# Colour of the boxes on the grid

r_col = (10, 10, 10)  # Colour for Removed
s_col = (0, 0, 200)  # Colour for Susceptible
i_col = (200, 0, 100)  # Colour for Infectious
w_col = (100, 100, 100)  # Colour for Wall

# 1/Beta, 1/gamma and mu are R, the infectious period and recovery rate of our disease

# A cold due to renewed susceptibility

beta = 0.2
gamma = 0.2
mu = 0.018

# Initialize grid

grid = []

# This bit makes sure that our grid is the right size

if len(grid) > h:
    h = len(grid)
for row in grid:
    if len(row) > w:
        w = len(row)

if len(grid) < h:
    grid += [[] for i in range(h - len(grid))]

for row in grid:
    if len(row) < w:
        row += [1 for i in range(w - len(row))]

# Create a firewall

f_x = int(w / 3)

for row in grid:
    row[f_x] = 3

# Now leave some holes

porosity = 0.03
num_holes = int(h * porosity)
hole_count = 0

while hole_count < num_holes:
    hole_y = random.randint(0, h - 1)
    if grid[hole_y][f_x] == 3:
        grid[hole_y][f_x] = 1
        hole_count += 1

# Infect a few random people

to_infect = 10

for i in range(to_infect):
    cell_available = False
    while not cell_available:
        x = random.randint(int(w / 2), w - 1)
        y = random.randint(int(h / 2), h - 1)
        cell_available = (grid[y][x] == 1)
    grid[y][x] = 2

# How to find the neighbours of a cell...

n_list = []

for j in [-1, 0, 1]:
    for i in [-1, 0, 1]:
        if not (i == 0 and j == 0):
            n_list.append((i, j))

# This creates a loop that only ends when you close the window

still_looping = True

while still_looping:

    # This looks to see whether the close button has been pressed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still_looping = False

    # Clean the board before we start!!

    my_screen.fill((100, 100, 150))

    # Reset counters for the state of the system

    S = 0
    I = 0
    R = 0

    # Create a working copy of our grid so that we can iterate

    ref_grid = copy.deepcopy(grid)

    # Now let's iterate

    for y in range(h):
        for x in range(w):

            # Start by displaying the current state

            cell_val = ref_grid[y][x]

            if cell_val == 0:
                my_col = r_col
            if cell_val == 1:
                my_col = s_col
            if cell_val == 2:
                my_col = i_col
            if cell_val == 3:
                my_col = w_col

            pygame.draw.rect(my_screen, my_col, (g_x + b_width * x, g_y + b_height * y, b_width, b_height), 0)

            # Counter for neighbours

            n_count = 0

            # Work through neighbours

            for (i, j) in n_list:
                n_x = x + i
                n_y = y + j

                # As long as they are on the grid!

                if n_x >= 0 and n_y >= 0 and n_x < w and n_y < h:

                    # If so then count whether they are infected
                    if ref_grid[n_y][n_x] == 2:
                        n_count = n_count + 1

            # Then iterate according to our rules

            # If dead/removed then we should roll a die to come to life

            if cell_val == 0:
                R += 1
                if random.random() < mu:
                    cell_val = 1

            # If alive with an infected neighbour then roll a die to infect

            if cell_val == 1 and n_count > 0:
                S += 1
                if random.random() < beta:
                    cell_val = 2

            # If infected then roll a die to die

            if cell_val == 2:
                I += 1
                if random.random() < gamma:
                    cell_val = 0

            # Update the grid

            grid[y][x] = cell_val

    # Show off our handiwork

    pygame.display.update()

    # Remind us of the values of the parameters and the current state

    # print('\n\n beta = ', beta, '\t\t S = ', S)
    # print('gamma = ', gamma, '\t\t I = ', I)
    # print('   mu = ', mu, '\t\tR = ', R, '\n\n')

# Finish things off
pygame.quit()
sys.exit()
