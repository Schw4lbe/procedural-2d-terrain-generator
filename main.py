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
        tile_map_segment = TileMapSegment(0.2)
        # print(tile_map_segment.land_tiers)
        # print(tile_map_segment.land_tiles_amount)
        # print(tile_map_segment.land_tile_distribution)

        test_array = process_land_tile_distribution(tile_map_segment)

        display_out(test_array)
    except KeyboardInterrupt:
        print("exit.")


def process_land_tile_distribution(segment: TileMapSegment) -> list[list]:
    max_index: int = segment.DIMENSION_XY - 1

    for item in segment.land_tile_distribution:

        while True:
            local_array: list[list] = [
                [0 for x in range(segment.DIMENSION_XY)]
                for y in range(segment.DIMENSION_XY)
            ]

            item_render_range: int = set_render_range(item)
            rnd_index_x: int = get_random_index(max_index, item_render_range)
            rnd_index_y: int = get_random_index(max_index, item_render_range)
            start_x: int = rnd_index_x

            print("Startin POINT for Rendering: ", rnd_index_y, rnd_index_x)

            try:
                for _ in range(item):
                    local_array[rnd_index_y][rnd_index_x] = 1

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
                # TODO: add some rotation here next before returning anything

                return modified_array

            except IndexError as e:
                print(e)
                winsound.Beep(1000, 200)
                continue


def get_random_index(max_index: int, item_render_range: int) -> int:
    return random.randint(0, max_index - item_render_range)


# TODO: add gap mechanic for start or ending
def add_edge_erosion(array: list[list], item_render_range: int) -> list[list]:
    local_array: list[list] = array.copy()
    erosion_max: int = int(math.floor(item_render_range * 0.2))
    erosion_checksum: int = 0
    row_idex_list: list = []

    for row_index, row in enumerate(local_array):
        if any(row):
            row_idex_list.append(row_index)
            erosion_start: int = random.randint((erosion_max * -1), erosion_max)
            erosion_end: int = random.randint((erosion_max * -1), erosion_max)
            start: int = row.index(1)
            end: int = (len(row) - 1) - row[::-1].index(1)
            # print("erosions: ", erosion_start, erosion_end)
            # print("start/end: ", start, end)

            if erosion_start > 0:
                index = start - erosion_start

                for _ in row:
                    if row[index] == 1:
                        break
                    else:
                        row[index] = 1
                        erosion_checksum += 1
                        index += 1

            elif erosion_start < 0:
                index = start

                for _ in row:
                    if erosion_start == 0:
                        break
                    else:
                        row[index] = 0
                        erosion_checksum -= 1
                        index += 1
                        erosion_start += 1

            if erosion_end > 0:
                index = end + 1

                for _ in row:
                    if index == erosion_end + end + 1:
                        break
                    else:
                        row[index] = 1
                        erosion_checksum += 1
                        index += 1

            elif erosion_end < 0:
                index = end + erosion_end + 1

                for _ in row:
                    if row[index] == 0:
                        break
                    else:
                        row[index] = 0
                        erosion_checksum -= 1
                        index += 1

    if erosion_checksum != 0:
        local_array: list[list] = apply_overflow(
            local_array, erosion_checksum, row_idex_list[0], row_idex_list[-1]
        )
        return local_array

    else:
        return local_array


def apply_overflow(array: list[list], erosion_checksum: int, y_start: int, y_end: int):
    local_array: list[list] = array.copy()
    on_top: bool = True
    distribution: list = set_overflow_distribution(erosion_checksum)

    # NOTE: local overwrite for testing:
    distribution = [1, 3, 4]
    erosion_checksum = 8

    if erosion_checksum > 0:
        # guards to prevent index errors
        if y_start - len(distribution) < 0:
            on_top = False
        if y_end + len(distribution) > TileMapSegment.DIMENSION_XY - 1:
            on_top = True

        if on_top:
            x_start: int = local_array[y_start].index(1)
            x_end: int = (
                len(local_array[y_start]) - 1 - local_array[y_start][::-1].index(1)
            )

            x_new_start: int = x_start + ((x_end - x_start) // 2)
            print("X NEW START: ", x_new_start)
            print(distribution)

            y_start -= len(distribution)

            for value in distribution:
                index = x_new_start
                for n in range(value):
                    local_array[y_start][index] = 1
                    print("tile set: ", y_start, index)
                    if n + 1 == value:
                        x_new_start -= 1
                    else:
                        index += 1

                y_start += 1

    return local_array


# NOTE: currently increase per row hardcode as int 2
def set_overflow_distribution(value: int):
    row_size: int = 1
    rows: list = []

    if value < 0:
        value = value * (-1)

    while value > 0:
        amount = min(row_size, value)
        rows.append(amount)

        value -= amount
        row_size += 2

    return rows


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
