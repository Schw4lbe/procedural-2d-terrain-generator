# procedural terrain generation
# regarind first calculations for 1440p resolution
# to have buffers arround the player we need at least 15x27 16pixel tiles

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import random
import math

# random.seed(10)

# maybe define a specific position where to populate an island
# maybe set fixed number of populations

# idea for multi layer random generation
# assume 10 x 10 tiles and 20 percent land ergo 20 tiles
# set a limit of own entities per total pixels
# a entity is for the start describes a big, medium or small tileset
# base idea is to have gib tile sets beeing doulbe the size as med, beeing double as small ones
# lets say on 20 tiles results in 3 tile packages 1 big(10) 2 small(5)
# separate full 10 x 10 tiles evenly into 4 5x5 areas -> 1 area will be free
# another example would be having 5 tile packages 1 big(20) 2 med(10) 4 small(2-3)
# in total 7 areas needed separate 12 x 12 tiles into 9 evenly split 4 x 4 areas
# keep in mind cols_rows have to be divideable wihtout rest by number of total areas
# every area gets its own random origin point to start draw land tiles
# to have maximum randomness later make every area it its self rotate 0 - 270 deg at random
# put it all together in one segment and add to world tile set
# have to find out if area separation is actually doable with indexing or by constructing own lists
# area rotation could be tricky with one big array


def init_generator():
    try:
        grid = np.array(sample_random_tiles())
        cmap_rgba = ListedColormap([(0, 0, 0.8, 1), (0, 1, 0, 1)])
        plt.imshow(grid, cmap=cmap_rgba)
        plt.show()
    except KeyboardInterrupt:
        print("exit.")


def sample_random_tiles(cols_rows: int = 10, percent: int = 30):
    new_segment: list = []
    for n in range(cols_rows):
        if n == cols_rows:
            break

        else:
            n -= -1
            new_row: list = [0] * cols_rows
            el_per_row: int = int(math.ceil((percent / 100) * cols_rows))
            sample: list = random.sample(range(cols_rows), el_per_row)
            for index in sample:
                new_row[index] = 1

            new_segment.append(new_row)
    return new_segment


def main():
    init_generator()


if __name__ == "__main__":
    main()
