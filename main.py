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


class TileMapSegment:
    DIMENSION_XY: int = 36

    def __init__(self, percent: float):
        self.percent = percent
        self.land_tiles_amount: int = int(
            math.floor(pow(self.DIMENSION_XY, 2) * percent)
        )
        self.land_tiers: dict = self.set_land_tiers(percent)
        self.land_tile_distribution: list = self.distribute_tiles_per_tier(
            self.land_tiles_amount, self.land_tiers
        )
        self.tilemap_array: list[list] = [
            [0 for x in range(self.DIMENSION_XY)] for y in range(self.DIMENSION_XY)
        ]

    def set_land_tiers(self, percent: int) -> dict:
        if percent == 100:
            return {"b": 1, "m": 0, "s": 0}

        else:
            land_tiers: dict = {
                "b": random.randint(1, 2),
                "m": random.randint(0, 4),
                "s": random.randint(0, 8),
            }
            return land_tiers

    def distribute_tiles_per_tier(self, amount: int, tiers: dict) -> list:
        # NOTE: dev overwrite local for testing
        # tiers = {"b": 2, "m": 1, "s": 0}

        # TODO: currently linear distribution, might consider more randomness
        # this would involve float factors on amount for partila_amount variables
        # also would involve having random range per iteration on tiers entry
        # is complicated because there will be a value overflow that has to be caught and processed

        results: list = []
        if tiers["m"] == 0 and tiers["s"] == 0:
            partial_amount: int = int(math.floor(amount / tiers["b"]))
            for _ in range(tiers["b"]):
                results.append(partial_amount)

        elif tiers["m"] == 0 and tiers["s"] != 0:
            partial_amount_big: int = int(math.floor(amount * 0.80 / tiers["b"]))
            partial_amount_small: int = int(math.floor(amount * 0.20 / tiers["s"]))
            for _ in range(tiers["b"]):
                results.append(partial_amount_big)

            for _ in range(tiers["s"]):
                results.append(partial_amount_small)

        elif tiers["m"] != 0 and tiers["s"] == 0:
            partial_amount_big: int = int(math.floor(amount * 0.70 / tiers["b"]))
            partial_amount_medium: int = int(math.floor(amount * 0.30 / tiers["m"]))
            for _ in range(tiers["b"]):
                results.append(partial_amount_big)

            for _ in range(tiers["m"]):
                results.append(partial_amount_medium)

        else:
            partial_amount_big: int = int(math.floor(amount * 0.60 / tiers["b"]))
            partial_amount_medium: int = int(math.floor(amount * 0.30 / tiers["m"]))
            partial_amount_small: int = int(math.floor(amount * 0.10 / tiers["s"]))
            for _ in range(tiers["b"]):
                results.append(partial_amount_big)

            for _ in range(tiers["m"]):
                results.append(partial_amount_medium)

            for _ in range(tiers["s"]):
                results.append(partial_amount_small)

        return results


def init_generator():
    tile_map_segment = TileMapSegment(0.2)
    print(tile_map_segment.land_tiers)
    print(tile_map_segment.land_tiles_amount)
    print(tile_map_segment.land_tile_distribution)

    exit()
    display_out(tile_map_segment.tilemap_array)


def display_out(grid: list[list]):
    grid = np.array(grid)
    cmap_rgba = ListedColormap([(0, 0, 0.8, 1), (0, 1, 0, 1)])
    plt.imshow(grid, cmap=cmap_rgba)
    plt.show()


def get_grid():
    pass


def main():
    init_generator()


if __name__ == "__main__":
    main()
