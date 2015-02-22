import numpy as np
import time
# 0 - white, 1 - black


f = 0
HEIGHT = 0
WIDTH = 0
way = ""
size = ()
x = 0
y = 0
step = 1
direction = 3    # 0 - North, 1 - East, 2 - South, 3 - West


class UnexpectedError(Exception):
    def __init__(self, value):
        self.value = value


def data():
    global f, HEIGHT, WIDTH, size, way, direction, x, y, arrray
    while not(f):
        f = input("Beginning (1 - white field, 2 - your field): ")

    global array
    if f == "1":
        while not(HEIGHT) or not(WIDTH):
            print("Size of field in cells: ")
            HEIGHT = int(input("height ")) - 1
            WIDTH = int(input("width ")) - 1
        size = (HEIGHT, WIDTH)
        array = np.zeros((HEIGHT+1, WIDTH+1), dtype=int)
    elif f == "2":
        while not(way):
            try:
                way = input("Way to field: ")
                array = np.loadtxt(way, dtype=int)
            except IOError:
                print("No such file or directory: {}\ntry again".format(way))
        size = array.shape
        HEIGHT = size[0]
        WIDTH = size[1]

    while not(x) or not(y):
        print("Original ant's coorinates:")
        x = int(input("x "))
        y = int(input("y "))


def output():
    print(step)
    for row in array:
        for col in row:
            print(col, end="")
        print()
    print()


def turn(move):   # on white - clockwise; on black - counterclockwise
    global direction
    if move == 1:   # move == 1 NESW;       move == 0
        direction = (direction + 1) % 4
    elif move == 0:
        direction = (direction - 1) % 4


def step_():
    global direction, x, y, size
    if direction == 0:
        if x != 0:
            x = x - 1
        else:
            x = size[0]
    elif direction == 1:
        if y != size[1]:
            y += 1
        else:
            y = 0
    elif direction == 2:
        if x != size[0]:
            x += 1
        else:
            x = 0
    elif direction == 3:
        if y != 0:
            y -= 1
        else:
            y = size[1]


def main():
    global step
    while 1:
        if (array[x][y] == 0) or (array[x][y] == 1):
            turn(int(not(array[x][y])))
            array[x][y] = int(not(array[x][y]))
            step_()
        else:
            raise(UnexpectedError("Something goes wrong!"))
        step += 1
        output()
        time.sleep(1)


if __name__ == "__main__":
    data()
    output()
    main()
