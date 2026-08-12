# procedural terrain generation
# regarind first calculations for 1440p resolution
# to have buffers arround the player we need at least 15x27 16pixel tiles

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import random
import math

# random.seed(10)

counter: int = 0


def random_segment(cols_rows: int = 10, land_percentage: int = 30) -> list:
    new_segment: list = [
        [
            random_int_land_tile_percent(cols_rows, land_percentage)
            for _ in range(cols_rows)
        ]
        for _ in range(cols_rows)
    ]
    return new_segment


# issue here is that it could happen that the limit is reached to early
# rest of the segment is all water no clear overall distribution
# somehow use sample maybe to return each line with a sample
# maybe define a specific position where to populate an island
def random_int_land_tile_percent(factor: int, percent: int) -> int:
    global counter
    limit: int = math.floor(((factor * factor) / 100) * percent)
    if counter < limit:
        print(counter)
        rand_int: int = random.randint(0, 1)
        if rand_int == 1:
            counter += 1
            return 1
        else:
            return 0
    else:
        return 0


grid = np.array(random_segment())
cmap_rgba = ListedColormap([(0, 0, 0.8, 1), (0, 1, 0, 1)])

plt.imshow(grid, cmap=cmap_rgba)

plt.show()


def main():
    print("Hello from procedural-generation!")


if __name__ == "__main__":
    main()
