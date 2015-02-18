import numpy as np
import time
from PIL import Image, ImageDraw


while 1:
    try:
        way = input()
        array1 = np.loadtxt(way, dtype=int)
    except IOError:
        print("No such file or directory: {}\ntry again".format(way))
    else:
        break
size = array1.shape
generation = 1
HEIGHT = 320   # size of image
WIDTH = 320


class UnexpectedError(Exception):
    def __init__(self, value):
        self.value = value


def neighbours(i, j):
    """ return numbers of alive neighbours of cell
        array1[i][j] - current cell
    """
    if i == 0:
        k1 = size[0] - 1   # last string
    else:
        k1 = i-1
    if j == 0:
        k2 = size[1] - 1   # last column
    else:
        k2 = j-1

    if i+1 == size[0]:     # last string
        k3 = 0
    else:
        k3 = i+1
    if j+1 == size[1]:     # last column
        k4 = 0
    else:
        k4 = j+1

    _array = np.array((array1[k1, k2],
                       array1[k1, j],
                       array1[k1, k4],
                       array1[i, k2],
                       array1[i, k4],
                       array1[k3, k2],
                       array1[k3, j],
                       array1[k3, k4]),  # all neighbours
                      dtype=int)
    return np.count_nonzero(_array)


def show_(g):
    print(g,"generation")
    im = Image.new("RGBA", (WIDTH+1,HEIGHT+1), (256,256,256,256))
    draw = ImageDraw.Draw(im)
    step1 = HEIGHT / size[0]
    step2 = WIDTH / size[1]
    for k in range(size[0]+1):
        draw.line((0,k*step1, WIDTH,k*step1), fill="black")    # ------
    for k in range(size[1]+1):
        draw.line((k*step2,0, k*step2, HEIGHT), fill="black")    # |
    for st in range(size[0]):
        for col in range(size[1]):
            if array1[st][col]:
                draw.rectangle((col*step2,st*step1,(col+1)*step2,(st+1)*step1),
                               fill="black",
                               outline="black")
    return im
                

if __name__ == "__main__":
    f = input("Choose mode (1 - showing, 2 - generate x generation)  ")
    if f == "2":
        n = float(input("x  "))
    else:
        n = float("inf")
    while array1.any() and generation < n:   # while anybody lives
        if f == "1":
            show_(generation).show()
        array = np.zeros(size, dtype=int)

        for st in range(size[0]):   # strings
            for col in range(size[1]):   # columns
                if array1[st][col] == 0:
                    if neighbours(st, col) == 3:
                        array[st][col] = 1
                    else:
                        array[st][col] = 0

                elif array1[st][col] == 1:
                    if 1 < neighbours(st, col) < 4:
                        array[st][col] = 1
                    else:
                        array[st][col] = 0

                else:
                    er = "Wrong data at {} string, {} column".format(st+1, col+1)
                    raise(UnexpectedError(er))

        array1 = array
        generation += 1
        # time.sleep(1.5)
    if f == "2":
        show_(generation).save("After {} generation.gif".format(generation))
    elif not(array1.any()):
        raise(UnexpectedError("Dead after {} generation".format(generation)))
