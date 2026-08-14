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
        user_menu_select(2)
    except KeyboardInterrupt:
        print("exit.")


def user_menu_select(n: int):
    # NOTE: dev only for testing. calls specific int to bypass user select
    if not n:
        print("MENU OPTIONS:")
        print("(1) default random out OLD")
        print("(2) default random out")
        print("\n")
        user_input: int = int(input("select: "))

    else:
        user_input = n

    while True:
        if user_input == 1:
            output_random_old()
            break
        if user_input == 2:
            output_random_tile()
            break
        else:
            print("invalid input.")
            continue


def output_random_tile():
    grid = np.array(get_tiles_grid())
    cmap_rgba = ListedColormap([(0, 0, 0.8, 1), (0, 1, 0, 1)])
    display_out(grid, cmap_rgba)


# TODO: entities should come out of a constructor as payload
# TODO: also dimension and percent should come out of constructor
# TODO: keep in mind in constructor to also have a relation for m, s and later big
# dimension should be % 0 devided by area_amount/2
def get_tiles_grid(
    dimension: int = 10, percent: int = 20, entities: dict = {"m": 1, "s": 2, "sum": 3}
):
    new_array: list = []
    land_tiles_total: int = int(math.floor(pow(dimension, 2) * (percent / 100)))
    area_amount: int = get_area_amount(entities)
    print(land_tiles_total, area_amount)
    area_data: list[tuple] = get_area_data(area_amount, entities, land_tiles_total)

    print(area_data)
    exit()

    # set area data
    # get area size tile amount
    # set area sum to area_amount in relation and fill difference with empty area


def get_area_data(area_amount: int, entities: dict, land_tiles_total: int):
    full_entity_list: list[str] = get_full_entity_list(area_amount, entities)
    entity_type_amount: int = get_entity_type_amount(entities)
    entity_list_with_amounts: list[tuple] = get_entity_list_with_amounts(
        full_entity_list, entity_type_amount, land_tiles_total, entities
    )
    # maybe map here for entity list with amounts?
    print(full_entity_list)

    exit()


def get_entity_list_with_amounts(
    full_entity_list: list[str],
    entity_type_amount: int,
    land_tiles_total: int,
    entities: dict,
):
    results: list[tuple] = []

    tiles: int = land_tiles_total
    last_entity = None
    for e in full_entity_list:
        if e == "e":
            tiles = 0

        if e == last_entity:
            for _ in e:
                results.append((e, tiles))

        else:
            for _ in e:
                tiles = tiles / 2
                results.append((e, tiles))

        last_entity = e

    print(results)


def get_entity_type_amount(entities: dict):
    amount: int = 0
    for e in entities:
        if e == "sum":
            continue
        else:
            amount += 1
    return amount


def get_full_entity_list(area_amount: int, entities: dict) -> list[str]:
    entity_list: list = []
    for _ in range(area_amount):
        for e in entities:
            # ignore sum key
            if e == "sum":
                continue

            if entities[e] != 0:
                entities[e] -= 1
                entity_list.append(e)

    # add empty slots to match area_amount
    while True:
        if len(entity_list) < area_amount:
            entity_list.append("e")
        else:
            break

    return entity_list


def get_area_amount(entities: dict) -> int:
    amount: int = 0
    if entities["sum"] == 1:
        # NOTE: sqrt of 1 ceiled is still 1 pow of 1 cant be greater 1 so default smallest value is 4
        amount = 4
    else:
        amount = int(pow(math.ceil(math.sqrt(entities["sum"])), 2))

    return amount


def display_out(grid, cmap_rgba):
    plt.imshow(grid, cmap=cmap_rgba)
    plt.show()


# NOTE: version 1.0 with random sample generation without further controll params
def output_random_old():
    grid = np.array(sample_random_tiles_old())
    cmap_rgba = ListedColormap([(0, 0, 0.8, 1), (0, 1, 0, 1)])
    display_out(grid, cmap_rgba)


def sample_random_tiles_old(cols_rows: int = 10, percent: int = 30) -> list:
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
