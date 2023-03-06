import copy
import math
import numpy as np
import warnings
warnings.filterwarnings("ignore")


class Cell:
    def __init__(self, value, adj_neighbors, others, obstacle=False):
        self.others = others
        self.adj_neighbors = adj_neighbors
        self.value = value
        self.obstacle = obstacle

        self.neighbors = []
        self.corners = []


cum_prob = 0.9


def initiate(grid):
    n = grid.shape[0]
    m = grid.shape[1]
    for i in range(n):
        for j in range(m):
            cell_counts_update(i, j,grid)
            # else :
            #     print(i,j,"obstacle")


def find_cell_prob(i, j,grid,grid1):
    n = grid.shape[0]
    m = grid.shape[1]

    sum = 0
    for adj in grid[i, j].neighbors:
        cell = grid[adj[0], adj[1]]
        sum += cell.value * (cum_prob / cell.adj_neighbors)


    sum += grid[i, j].value * (1 - cum_prob) / grid[i, j].others
    for corner in grid[i, j].corners:
        cell = grid[corner[0], corner[1]]
        if cell.adj_neighbors == 0:
            sum += cell.value * (1 / cell.others)
        else :
            sum += cell.value * ((1 - cum_prob) / cell.others)
        # print(corner[0], corner[1], cell.others)
    grid1[i, j].value = sum


def cell_counts_update(i, j, grid):
    # if grid[i, j].obstacle:
    #     return
    n = grid.shape[0]
    m = grid.shape[1]
    adj_neighbor = 4
    others = 5
    if grid[i, j].obstacle:
        others = 4
    for x in [-1, 1]:
        if i + x < 0 or i + x > n - 1 or grid[i + x, j].value == 0:
            adj_neighbor -= 1
        else:
            grid[i, j].neighbors.append([i + x, j])
        if j + x < 0 or j + x > m - 1 or grid[i, j + x].value == 0:
            adj_neighbor -= 1
        else:
            grid[i, j].neighbors.append([i, j + x])
        for y in [-1, 1]:
            if i + x < 0 or i + x > n - 1 or j + y < 0 or j + y > m - 1 or grid[i + x, j + y].value == 0:
                others -= 1
            else:
                grid[i, j].corners.append([i + x, j + y])
    grid[i, j].adj_neighbors = adj_neighbor
    grid[i, j].others = others


def normalize(grid):
    n = grid.shape[0]
    m = grid.shape[1]
    sum = 0
    for i in range(n):
        for j in range(m):
            if not grid[i, j].obstacle:
                sum += grid[i, j].value
    for i in range(n):
        for j in range(m):
            if not grid[i, j].obstacle:
                grid[i, j].value /= sum


def increase_prob(u, v, b, grid):
    grid1 = copy.deepcopy(grid)
    n = grid.shape[0]
    m = grid.shape[1]
    for i in range(n):
        for j in range(m):
            if not grid[i, j].obstacle:
                find_cell_prob(i, j, grid,grid1)
    grid = grid1

    # print("Partial Belief:")
    # print_grid(grid)

    if b == 1:
        for i in range(n):
            for j in range(m):
                grid[i, j].value *= 0.15
        grid[u, v].value *= 0.85 / 0.15
        for n in grid[u, v].neighbors:
            neighbor = grid[n[0], n[1]]
            neighbor.value *= 0.85 / 0.15
        for c in grid[u, v].corners:
            corner = grid[c[0], c[1]]
            corner.value *= 0.85 / 0.15
    elif b == 0:
        for i in range(n):
            for j in range(m):
                grid[i, j].value *= 0.85
        grid[u, v].value *= 0.15 / 0.85
        for n in grid[u, v].neighbors:
            neighbor = grid[n[0], n[1]]
            neighbor.value *= 0.15 / 0.85
        for c in grid[u, v].corners:
            corner = grid[c[0], c[1]]
            corner.value *= 0.15 / 0.85

    # print("Evidence :")
    # print_grid(grid)

    normalize(grid)

    # print("Normalized :")
    # print_grid(grid)
    return grid


def print_grid(grid):
    n = grid.shape[0]
    m = grid.shape[1]
    print(end='\t')
    for x in range(m):
        print(x, end='\t\t\t')
    print()
    for i in range(n):
        print(i, end='\t')
        for j in range(m):
            x = grid[i, j].value*100.0
            print("%.7f" % x, end='\t')
        print()



f = open("input.txt", "r")
line1 = f.readline().split(" ")
n, m, k = int(line1[0]), int(line1[1]), int(line1[2])
grid = np.empty([n, m], dtype=np.object)
grid1 = np.empty([n, m], dtype=np.object)

for i in range(0, n):
    for j in range(0, m):
        grid[i, j] = Cell(1 / (n * m - k), 0, 0)
for i in range(0, k):
    line = f.readline().split(" ")
    grid[int(line[0]), int(line[1])] = Cell(0, 0, 0, True)
print_grid(grid)
print("="*80)
initiate(grid)
grid1 = copy.deepcopy(grid)
time = 0
lines = f.readlines()
for line in lines:
    # print(line)
    line = line.rstrip()
    parts = line.split(" ")
    if parts[0] == "R":
        time+=1
        u = parts[1]
        v = parts[2]
        b = parts[3]
        grid = increase_prob(int(u), int(v), int(b), grid)
        print("Time ",time)
        print_grid(grid)
        print("="*80)
    elif line == "C":
        max = -math.inf
        maxi,maxj = 0,0
        for i in range(0, n):
            for j in range(0, m):
                if grid[i, j].value > max:
                    max = grid[i,j].value
                    maxi = i
                    maxj = j
        print("Casper is probably at",maxi,maxj)
        print("=" * 80)
    elif line == "Q":
        print("Bye Casper!")
        exit()
