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
        self.land_tiles_amount: int = int(math.floor(pow(self.DIMENSION_XY, 2) * percent))
        self.land_tiers: dict = self.set_land_tiers(percent)
        self.land_tile_distribution: list = self.distribute_tiles(self.land_tiles_amount, self.land_tiers)
        self.tilemap_array: list[list] = [[0 for x in range(self.DIMENSION_XY)] for y in range(self.DIMENSION_XY)]

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


init_count = 0


def init_generator():

    # NOTE: Seed implementation for debugging
    # seed = random.randint(0, 2**32 - 1)
    # random.seed(2705548230)
    # print("#########################")
    # print("SEED: ", seed)

    try:
        tile_map_segment = TileMapSegment(0.3)
        test_array = process_land_tile_distribution(tile_map_segment)
        # NOTE: testing to verifiy correct number of land tiles present in processed array
        count = sum(row.count(1) for row in test_array)
        print(f"FINAL CHECK {tile_map_segment.land_tiles_amount}: ", count)

        # TODO: add tilemap rotation function before display out happens

        # global init_count
        # init_count += 1
        # if init_count <= 200:
        #     init_generator()
        # else:
        #     exit()

        # exit()

        display_out(test_array)
    except KeyboardInterrupt:
        print("exit.")


def process_land_tile_distribution(segment: TileMapSegment) -> list[list]:
    max_index: int = segment.DIMENSION_XY - 1

    for item in segment.land_tile_distribution:
        reserved: int = random.randint(int(math.floor(item * -0.1)), int(math.floor(item * 0.1)))
        tile_amount = item - reserved

        while True:
            local_array: list[list] = [[0 for x in range(segment.DIMENSION_XY)] for y in range(segment.DIMENSION_XY)]

            item_render_range: int = set_render_range(tile_amount)
            rnd_index_x: int = get_random_index(max_index, item_render_range)
            rnd_index_y: int = get_random_index(max_index, item_render_range)

            # NOTE: Dev overwrite
            # rnd_index_x = 2
            # rnd_index_y = 20

            start_x: int = rnd_index_x

            try:
                for _ in range(tile_amount):
                    local_array[rnd_index_y][rnd_index_x] = 1

                    if rnd_index_x == max_index or rnd_index_x == (start_x + item_render_range):
                        rnd_index_y += 1
                        rnd_index_x -= item_render_range

                    else:
                        rnd_index_x += 1

                modified_array: list[list] = add_edge_erosion(local_array, item_render_range, reserved)

                return modified_array

            except IndexError as e:
                print(e)
                winsound.Beep(250, 200)
                continue

            except ValueError as e:
                print(e)
                print(local_array)
                winsound.Beep(450, 200)
                continue


def set_render_range(tile_amount: int) -> int:
    min_range: int = int(math.floor(math.sqrt(tile_amount) * 0.8))
    max_range: int = int(math.floor(math.sqrt(tile_amount) * 1.2))
    return random.randint(min_range, max_range)


def get_random_index(max_index: int, item_render_range: int) -> int:
    return random.randint(2, max_index - item_render_range)


def add_edge_erosion(array: list[list], item_render_range: int, reserved: int) -> list[list]:
    local_array: list[list] = array.copy()
    erosion_max: int = int(math.floor(item_render_range * 0.1))
    erosion_checksum: int = 0

    row_index_list: list = []

    for row_index, row in enumerate(local_array):
        if any(row):
            erosion_start: int = random.randint((erosion_max * -2), erosion_max)
            erosion_end: int = random.randint((erosion_max * -2), erosion_max)
            start: int = row.index(1)
            end: int = (len(row) - 1) - row[::-1].index(1)

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

            if any(row):
                row_index_list.append(row_index)

    erosion_checksum -= reserved
    # NOTE: Dev overwrite
    # erosion_checksum = 50

    if erosion_checksum != 0:
        new_local_array: list[list] = handle_checksum_imbalance(
            local_array, erosion_checksum, row_index_list[0], row_index_list[-1]
        )

        return new_local_array

    else:
        return local_array


def handle_checksum_imbalance(array: list[list], erosion_checksum: int, y_start: int, y_end: int):
    local_array: list[list] = array.copy()
    distribution: list = set_distribution(erosion_checksum)
    top_blocked: bool = y_start - math.ceil(len(distribution) / 2) < 0
    bottom_blocked: bool = y_end + math.ceil(len(distribution) / 2) > TileMapSegment.DIMENSION_XY - 1

    if erosion_checksum < 0:
        if bottom_blocked and not top_blocked:
            local_array = handle_underflow_top(local_array, distribution, y_start)

        elif top_blocked and not bottom_blocked:
            local_array = handle_underflow_bottom(local_array, distribution, y_end)

        else:
            dist_top: list = distribution[::2]
            dist_bottom: list = distribution[1::2]
            local_array = handle_underflow_top(local_array, dist_top, y_start)
            local_array = handle_underflow_bottom(local_array, dist_bottom, y_end)

    else:
        dist_top: list = distribution[::2]
        dist_bottom: list = distribution[1::2]

        x_start_top: int = local_array[y_start].index(1)
        x_end_top: int = len(local_array[y_start]) - 1 - local_array[y_start][::-1].index(1)
        x_center_top: int = x_start_top + ((x_end_top - x_start_top) // 2)
        y_start += len(dist_top) - 1

        for value in dist_top:
            index = x_center_top
            for n in range(value):
                local_array[y_start][index] = 0
                if n + 1 == value:
                    x_center_top -= 1
                else:
                    index += 1

            y_start -= 1

        x_start_bottom: int = local_array[y_end].index(1)
        x_end_bottom: int = len(local_array[y_end]) - 1 - local_array[y_end][::-1].index(1)
        x_center_bottom: int = x_start_bottom + ((x_end_bottom - x_start_bottom) // 2)
        y_end -= len(dist_bottom) - 1

        for value in dist_bottom:
            index = x_center_bottom
            for n in range(value):
                local_array[y_end][index] = 0
                if n + 1 == value:
                    x_center_bottom -= 1
                else:
                    index += 1

            y_end += 1

    return local_array


def handle_underflow_top(array: list[list], distribution: list, y_start: int) -> list[list]:
    local_array: list[list] = array.copy()
    x_start: int = local_array[y_start].index(1)
    x_end: int = len(local_array[y_start]) - 1 - local_array[y_start][::-1].index(1)
    x_center: int = x_start + ((x_end - x_start) // 2)
    y_start -= len(distribution)

    for value in distribution:
        index = x_center
        for n in range(value):
            local_array[y_start][index] = 1
            if n + 1 == value:
                x_center -= 1
            else:
                index += 1

        y_start += 1
    return local_array


def handle_underflow_bottom(array: list[list], distribution: list, y_end: int) -> list[list]:
    local_array: list[list] = array.copy()
    # NOTE: had index bug in x_start for index of 1
    x_start: int = local_array[y_end].index(1)
    x_end: int = len(local_array[y_end]) - 1 - local_array[y_end][::-1].index(1)
    x_center: int = x_start + ((x_end - x_start) // 2)
    y_end += len(distribution)

    for value in distribution:
        index = x_center
        for n in range(value):
            local_array[y_end][index] = 1
            if n + 1 == value:
                x_center -= 1
            else:
                index += 1

        y_end -= 1
    return local_array


def set_distribution(value: int):
    row_size: int = random.randint(0, 2)
    rows: list = []

    if value < 0:
        value = value * (-1)

    loop_count: int = 1
    while value > 0:

        amount = min(row_size, value)
        rows.append(amount)
        value -= amount
        row_size += random.randint(0, min(loop_count, value // 2))
        loop_count += 1

    return sorted(rows)


def display_out(grid: list[list]):
    grid = np.array(grid)
    cmap_rgba = ListedColormap([(0, 0, 0.8, 1), (0, 1, 0, 1)])
    plt.imshow(grid, cmap=cmap_rgba)
    plt.show()


def main():
    init_generator()


if __name__ == "__main__":
    main()
