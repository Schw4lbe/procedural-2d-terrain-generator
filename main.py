import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import random
import math
import winsound

# make every partial generation at itself rotate 0 - 270 deg at random
# put it all together in one world tile set


class TileMapSegment:
    DIMENSION_XY: int = 36

    def __init__(self, percent: float):
        self.percent = percent
        self.land_tiles_amount: int = int(
            math.floor(pow(self.DIMENSION_XY, 2) * percent)
        )
        self.land_tiers: dict = self.set_land_tiers(percent)
        self.land_tile_distribution: list = self.distribute_tiles(
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

    def distribute_tiles(self, amount: int, tiers: dict) -> list:
        # NOTE: dev overwrite local for testing
        tiers = {"b": 1, "m": 0, "s": 0}

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
    try:
        tile_map_segment = TileMapSegment(0.1)
        print(tile_map_segment.land_tiers)
        print(tile_map_segment.land_tiles_amount)
        print(tile_map_segment.land_tile_distribution)

        test_array = process_land_tile_distribution(tile_map_segment)

        display_out(test_array)
    except KeyboardInterrupt:
        print("exit.")


# TODO: embedd some form of noise to the generation to interupt tiles but without creating lakes
# TODO: before adding noise update script to also create a set
def process_land_tile_distribution(segment: TileMapSegment) -> list[list]:
    max_index: int = segment.DIMENSION_XY - 1

    for item in segment.land_tile_distribution:

        while True:
            local_array: list[list] = [
                [0 for x in range(segment.DIMENSION_XY)]
                for y in range(segment.DIMENSION_XY)
            ]

            rnd_index_x: int = random.randint(0, max_index)
            rnd_index_y: int = random.randint(0, max_index)
            start_x: int = rnd_index_x
            item_render_range: int = set_render_range(item)

            try:
                for _ in range(item):
                    local_array[rnd_index_y][rnd_index_x] = 1
                    print("y/x: ", rnd_index_y, rnd_index_x)

                    if rnd_index_x == max_index or rnd_index_x == (
                        start_x + item_render_range
                    ):
                        rnd_index_y += 1
                        rnd_index_x -= item_render_range

                    else:

                        rnd_index_x += 1

                modified_array: list[list] = add_edge_erosion(
                    local_array, item_render_range
                )
                return modified_array

            except IndexError as e:
                print(e)
                winsound.Beep(1000, 200)
                continue


# TODO: create a set from the local_array
# TODO: manipulate the set rather then the array it self
# TODO: add same logic as below after update loop set into array
def add_edge_erosion(local_array: list[list], item_render_range: int) -> list[list]:
    # 0 - 20% floored from render range
    erosion_max_range: int = int(math.floor(item_render_range * 0.2))

    # keep track of all deleted and added items
    # after last iteration counter for difference must be 0
    erosion_checksum: int = 0

    # NOTE: not worth the effort its to complicated
    # NOTE: redo with first filtering the array into a set
    # for row in local_array:
    #     if any(row):
    #         # on each row decide weather to add or delete tiles at START and END
    #         is_delete: bool = random.choice([True, False])
    #         erosion_front: int = random.randint(0, erosion_max_range)
    #         erosion_back: int = random.randint(0, erosion_max_range)
    #         for index, tile in enumerate(row):
    #             if tile == 1 and erosion_front > 0:
    #                 if is_delete:
    #                     tile[index] == 0
    #                     erosion_checksum -= 1
    #                     erosion_front -= 1
    #                 if not is_delete:
    #                     tile[index + erosion_front] == 1
    #                     erosion_checksum += 1
    #                     erosion_front -= 1


def set_render_range(item: int) -> int:
    min_range: int = int(math.floor(math.sqrt(item) * 0.5))
    max_range: int = int(math.floor(math.sqrt(item) * 1.5))
    return random.randint(min_range, max_range)


def display_out(grid: list[list]):
    grid = np.array(grid)
    cmap_rgba = ListedColormap([(0, 0, 0.8, 1), (0, 1, 0, 1)])
    plt.imshow(grid, cmap=cmap_rgba)
    plt.show()


def main():
    init_generator()


if __name__ == "__main__":
    main()
