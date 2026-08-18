local_array = [[0, 0], [1, 0]]

x_span: set = set()
y_span: set = set()

for y_index, row in enumerate(local_array):
    for x_index, col in enumerate(row):
        if col == 1:
            x_span.add(x_index)
            y_span.add(y_index)

print(max(x_span) - min(x_span), max(y_span) - min(y_span))


array1 = [[0, 0], [1, 0]]
array2 = [[0, 0], [0, 1]]


for row in range(len(array2)):
    for col in range(len(array2[row])):
        if array2[row][col] == 1 and array1[row][col] == 1:
            print("collision")
            break
