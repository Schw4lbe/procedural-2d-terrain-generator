import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np
import random
import math
import winsound
import traceback

### DEVLOG REFACTORING ###
# NOTE: I want all percentages to run properly from 0 - 100
# NOTE: making a clean cut on 80 percent land seems reasonable
# NOTE: One of the main issues is the edge erosion tolerance
# NOTE: also the returning only a int for render range and no actuall range is kind a limiting
# NOTE: render range static could cause issues
# NOTE: check if reappearing code is present


class TileMapSegment:
    DIMENSION_XY: int = 36

    def __init__(self, percent: float):
        self.percent = percent
        self.land_tiles_amount: int = int(math.floor(pow(self.DIMENSION_XY, 2) * percent))
        self.land_tiers: dict = self.set_land_tiers(percent)
        self.land_tile_distribution: list = self.distribute_tiles(self.land_tiles_amount, self.land_tiers)
        self.tilemap_array: list[list] = [[0 for x in range(self.DIMENSION_XY)] for y in range(self.DIMENSION_XY)]

        # NOTE: for refactoring Only
        # print(self.land_tiles_amount)
        # print(self.land_tiers)
        # print(self.land_tile_distribution)

    def set_land_tiers(self, percent: int) -> dict:
        if percent >= 0.8:
            return {"b": 1, "m": 0, "s": 0}

        else:
            land_tiers: dict = {
                "b": random.randint(1, 2),
                "m": random.randint(0, 4),
                "s": random.randint(0, 16),
            }
            return land_tiers

    def distribute_tiles(self, amount: int, tiers: dict) -> list:
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
    seed = random.randint(0, 2**32 - 1)
    random.seed(4028074726)
    # random.seed(seed)
    # print("#########################")
    print("SEED: ", seed)

    try:
        tile_map_segment = TileMapSegment(0.8)
        array = process_land_tile_distribution(tile_map_segment)

        """NOTE: dev overwrite for loop
        global init_count
        init_count += 1
        if init_count <= 100:
            init_generator()
        else:
            exit()"""

        print(tile_map_segment.land_tiles_amount)
        print(sum(row.count(1) for row in array))
        print(f"checksum", tile_map_segment.land_tiles_amount == sum(row.count(1) for row in array))
        print(array)
        # TODO: have to evaluate where difference comes from
        display_out(array)

    except KeyboardInterrupt:
        exit()

    except ValueError as e:
        print(e)
        winsound.Beep(450, 200)


def process_land_tile_distribution(segment: TileMapSegment) -> list[list]:
    max_index: int = segment.DIMENSION_XY - 1

    for item in segment.land_tile_distribution:
        reserved: int = int(math.floor(item * 0.2))
        tile_amount_to_use = item - reserved
        item_render_range: int = int(math.floor(math.sqrt(tile_amount_to_use)))

        print("initial check on item: ", reserved + tile_amount_to_use == item)

        while True:
            local_array: list[list] = [[0 for x in range(segment.DIMENSION_XY)] for y in range(segment.DIMENSION_XY)]
            rnd_index: tuple = get_random_index_xy(max_index, item_render_range, segment.tilemap_array)

            rnd_index_x: int = rnd_index[0]
            rnd_index_y: int = rnd_index[1]
            start_x: int = rnd_index_x

            try:
                # NOTE: output a square to start with
                for _ in range(tile_amount_to_use):
                    local_array[rnd_index_y][rnd_index_x] = 1

                    if rnd_index_x == max_index or rnd_index_x == (start_x + item_render_range):
                        rnd_index_y += 1
                        rnd_index_x -= item_render_range

                    else:
                        rnd_index_x += 1

                # NOTE: I think here might be an issue with land_tiles_amount -> it is not later used and there is a difference regarding the reservation
                local_array = add_edge_erosion(
                    local_array, item_render_range, reserved, segment.land_tiles_amount, max_index
                )

                return local_array

                tile_difference: int = sum(row.count(1) for row in local_array) - segment.land_tiles_amount
                if tile_difference > 0:
                    local_array = cleanup_tile_difference(local_array, tile_difference)
                local_array = add_rotation_and_mirroring(local_array)

                # NOTE: try add to result
                is_successfull: bool = attach_tiles_to_segment(segment, local_array)

                if is_successfull:
                    print(f"{item} tiles successfully added to segment.")
                    break
                else:
                    print(f"{item} failed")
                    break

            except IndexError as e:
                print("ERR: ", e)
                traceback.print_exc()
                continue

            except ValueError as e:
                print("ERR: ", e)
                # print(local_array)
                traceback.print_exc()

                winsound.Beep(450, 200)
                continue

            except AttributeError as e:
                print("ERR: ", e)
                # print(local_array)
                traceback.print_exc()

                winsound.Beep(650, 200)
                continue

    return segment.tilemap_array


def get_random_index_xy(max_index: int, item_render_range: int, tilemap_array: list[list]) -> tuple:
    while True:
        # NOTE: if here is buffer 2 to min, and buffer 2 to max i cant fit in 80 percent of land tiles any more
        # NOTE: there should be a distinction how many percent is even wanted to set a propper buffer
        # NOTE: hardcoding 2 tiles is bullshit
        # NOTE: set to 0 for testing and establishing a propper ersion method
        index_x: int = random.randint(0, max_index - item_render_range)
        index_y: int = random.randint(0, max_index - item_render_range)
        # NOTE: checks upfront if x and y render range are even possible in given space as square
        if index_x + item_render_range > max_index or index_y + item_render_range > max_index:
            continue
        # NOTE: checks upfront if point is allready populated
        if tilemap_array[index_y][index_x] == 1:
            continue
        else:
            return (index_x, index_y)


def attach_tiles_to_segment(segment: TileMapSegment, array: list[list]) -> bool:
    local_array: list[list] = array.copy()
    render_pos: tuple = (0, 0)

    def check_collision(array1: list[list], array2: list[list]) -> bool:
        for row in range(len(array2)):
            for col in range(len(array2[row])):
                if array2[row][col] == 1 and array1[row][col] == 1:
                    return True
                else:
                    continue

        return False

    is_colliding: bool = check_collision(segment.tilemap_array, local_array)

    if is_colliding:
        render_pos: tuple = get_free_render_position(segment, local_array)
        add_tiles_to_segment(segment.tilemap_array, local_array, render_pos)

    else:
        add_tiles_to_segment(segment.tilemap_array, local_array, render_pos)
        return True


def add_tiles_to_segment(segment_array: list[list], local_array: list[list], render_pos: tuple) -> None:
    start_x: int = render_pos[0]
    start_y: int = render_pos[1]

    for y in range(len(local_array)):
        for x in range(len(local_array[y])):
            if local_array[y][x] == 1:
                segment_array[start_y + y][start_x + x] = 1


def get_free_render_position(segment: TileMapSegment, local_array: list[list]) -> tuple:
    while True:
        render_dimension: tuple = get_render_dimension(local_array)
        max_index: int = len(segment.tilemap_array[0]) - 1
        x_start: int = random.randint(0, max_index - render_dimension[0])
        y_start: int = random.randint(0, max_index - render_dimension[1])

        is_free: bool = True

        for row in range(render_dimension[1]):
            for col in range(render_dimension[0]):
                if segment.tilemap_array[y_start + row][x_start + col] == 1:
                    is_free = False
                    break

            if not is_free:
                break

        if is_free:
            return (x_start, y_start)


def get_render_dimension(local_array: list[list]) -> tuple:
    x_span: set = set()
    y_span: set = set()

    for y_index, row in enumerate(local_array):
        for x_index, col in enumerate(row):
            if col == 1:
                x_span.add(x_index)
                y_span.add(y_index)

    return (max(x_span) - min(x_span), max(y_span) - min(y_span))


def add_rotation_and_mirroring(array: list[list]):
    local_array: list[list] = array.copy()
    rotation: str = random.choice([0, 90, 180, 270])
    mirror: str = random.choice(["hori", "vert", "none"])

    if rotation == 90:
        local_array = [list(row) for row in zip(*local_array[::-1])]
    elif rotation == 180:
        local_array = [row[::-1] for row in local_array[::-1]]
    elif rotation == 270:
        local_array = [list(row) for row in zip(*local_array)][::-1]

    if mirror == "hori":
        local_array = [row[::-1] for row in local_array]
    elif mirror == "vert":
        local_array = local_array[::-1]

    return local_array


def cleanup_tile_difference(array: list[list], tile_difference: int) -> list[list]:
    local_array: list[list] = array.copy()

    for row in local_array:
        for index, n in enumerate(row):
            if tile_difference == 0:
                return local_array

            if n == 1:
                row[index] = 0
                tile_difference -= 1

    return local_array


def add_edge_erosion(
    array: list[list], item_render_range: int, reserved: int, land_tiles_amount: int, max_index: int
) -> list[list]:
    erosion: int = int(math.floor(item_render_range * 0.1))
    # TODO: does this effect the checksum through floor? check!
    erosion_checksum: int = 0

    for row in array:
        if 1 in row:
            start_index: int = row.index(1)
            end_index: int = (len(row) - 1) - row[::-1].index(1)

            if start_index <= 1:
                erosion_amount_start: int = random.randint(-erosion, start_index)
            else:
                erosion_amount_start: int = random.randint(-erosion, erosion)

            if end_index >= 34:
                erosion_amount_end: int = random.randint(-erosion, max_index - end_index)
            else:
                erosion_amount_end: int = random.randint(-erosion, erosion)

            if erosion_amount_start > 0:
                index = start_index - erosion_amount_start
                for _ in row:
                    if erosion_amount_start == 0:
                        break
                    else:
                        row[index] = 1
                        erosion_checksum += 1
                        index += 1
                        erosion_amount_start -= 1

            elif erosion_amount_start < 0:
                index = start_index
                for _ in row:
                    if erosion_amount_start == 0:
                        break
                    else:
                        row[index] = 0
                        erosion_checksum -= 1
                        index += 1
                        erosion_amount_start += 1

            if erosion_amount_end > 0:
                index = end_index + erosion_amount_end
                for _ in row:
                    if erosion_amount_end == 0:
                        break
                    else:
                        row[index] = 1
                        erosion_checksum += 1
                        index -= 1
                        erosion_amount_end -= 1

            elif erosion_amount_end < 0:
                index = end_index
                for _ in row:
                    if erosion_amount_end == 0:
                        break
                    else:
                        row[index] = 0
                        erosion_checksum -= 1
                        index -= 1
                        erosion_amount_end += 1

    erosion_checksum -= reserved
    print(
        "second check in add edge erosion: ",
        land_tiles_amount + (erosion_checksum - sum(row.count(1) for row in array)),
    )

    if erosion_checksum != 0:
        array = handle_checksum_imbalance(array, erosion_checksum, max_index)
        return array
    else:
        return array


def handle_checksum_imbalance(array: list[list], erosion_checksum: int, max_index: int) -> list[list]:
    y_start = next(i for i, row in enumerate(array) if 1 in row)
    y_end = next(i for i, row in reversed(list(enumerate(array))) if 1 in row)
    distribution: list = set_distribution(erosion_checksum)
    top_blocked: bool = y_start == 0 or y_start - len(distribution) < 0
    bottom_blocked: bool = y_end == max_index or y_end + len(distribution) > max_index

    # TODO: why even deside like this and not put the bottom and top available rows inside the distribution?

    if erosion_checksum < 0:
        if bottom_blocked and not top_blocked:
            array = handle_underflow_top(array, distribution, y_start)

        elif top_blocked and not bottom_blocked:
            array = handle_underflow_bottom(array, distribution, y_end)

        else:
            dist_top: list = distribution[::2]
            dist_bottom: list = distribution[1::2]
            array = handle_underflow_top(array, dist_top, y_start)
            array = handle_underflow_bottom(array, dist_bottom, y_end)

    elif erosion_checksum > 0:
        dist_top: list = distribution[::2]
        dist_bottom: list = distribution[1::2]

        x_start_top: int = array[y_start].index(1)
        x_end_top: int = len(array[y_start]) - 1 - array[y_start][::-1].index(1)
        x_center_top: int = x_start_top + ((x_end_top - x_start_top) // 2)
        y_start += len(dist_top) - 1

        for value in dist_top:
            index = x_center_top
            for n in range(value):
                array[y_start][index] = 0
                if n + 1 == value:
                    x_center_top -= 1
                else:
                    index += 1

            y_start -= 1

        if len(dist_bottom) > 0:
            x_start_bottom: int = array[y_end].index(1)
            x_end_bottom: int = len(array[y_end]) - 1 - array[y_end][::-1].index(1)
            x_center_bottom: int = x_start_bottom + ((x_end_bottom - x_start_bottom) // 2)
            y_end -= len(dist_bottom) - 1

            for value in dist_bottom:
                index = x_center_bottom
                for n in range(value):
                    array[y_end][index] = 0
                    if n + 1 == value:
                        x_center_bottom -= 1
                    else:
                        index += 1

                y_end += 1

    else:
        return array

    return array


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
    # TODO: when bottom and top in distribution, always this function desides -> single point of entry
    # TODO: currently set distribution could lead to a length overflowing index range on higher percent
    # TODO: need to evaluate another propper way to distribute land tiles cleaner in lower len

    # TODO: also consider further not having a second cleanup later on -> function: cleanup_tile_difference
    # TODO: watch for propper loop or recursion entry point to work checksum difference into array
    # TODO: might keep the check at the end but refference to this function again rather then creating a new one (cleanup_tile_difference)

    row_size: int = random.randint(1, 2)
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

    # NOTE: this is the base for propper full world generation
    # grid = np.block(grid)
    # grid = np.block([[grid, grid, grid], [grid, grid, grid], [grid, grid, grid]])
    # cmap_rgba = ListedColormap([(0, 0, 0.8, 1), (0, 1, 0, 1)])
    # plt.imshow(grid, cmap=cmap_rgba)
    # plt.show()


def main():
    init_generator()


if __name__ == "__main__":
    main()
