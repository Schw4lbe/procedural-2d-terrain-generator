# procedural terrain generation

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import numpy as np

grid = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
grid2 = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 1]])

cmap_rgba = ListedColormap([(0, 0, 0.5, 1), (0, 1, 0, 1)])
cmap_rgba2 = ListedColormap([(0, 0, 0, 0), (1, 0, 0, 1)])

plt.imshow(grid, cmap=cmap_rgba)
plt.imshow(grid2, cmap=cmap_rgba2)

plt.show()


def main():
    print("Hello from procedural-generation!")


if __name__ == "__main__":
    main()
