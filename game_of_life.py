import numpy as np
import tkinter as tk
import sys     # sys.exit()

from PIL import Image, ImageDraw, ImageTk


class UnexpectedError(Exception):
    def __init__(self, value):
        self.value = value


def neighbours(i, j):
    """ return numbers of alive neighbours of cell
        array1[i][j] - current cell
    """
    # the left and right edges of the field are stitched together,
    # and the top and bottom edges also
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

    _array = np.array((array1[k1, k2],    # i-1, j-1
                       array1[k1, j],     # i-1, j
                       array1[k1, k4],    # i-1, j+1
                       array1[i, k2],     # i, j-1
                       array1[i, k4],     # i, j+1
                       array1[k3, k2],    # i+1, j-1
                       array1[k3, j],     # i+1, j
                       array1[k3, k4]),   # i+1, j+1
                      dtype=int)          # all neighbours
    return np.count_nonzero(_array)    # numbers of nonzero (alive) neighbours


def image_(g):
    """ generate image of g generation;
    """
    if f == 'show life':
        print(g, "generation")
    im = Image.new("RGBA", (WIDTH+1, HEIGHT+1), (256, 256, 256, 256))
    draw = ImageDraw.Draw(im)
    step1 = HEIGHT / size[0]
    step2 = WIDTH / size[1]
    for k in range(size[0]+1):
        draw.line((0, k*step1, WIDTH, k*step1), fill="black")    # ------
    for k in range(size[1]+1):
        draw.line((k*step2, 0, k*step2, HEIGHT), fill="black")    # |
    for st in range(size[0]):
        for c in range(size[1]):
            if array1[st][c]:
                draw.rectangle((c*step2, st*step1, (c+1)*step2, (st+1)*step1),
                               fill="black",
                               outline="black")
    return im


def show_():
    """ update image on root
    """
    photo = ImageTk.PhotoImage(image_(generation))
    label = tk.Label(image=photo)
    label.image = photo
    label.grid(row=1, column=1)
    button = tk.Button(root, text="ok", width=5, height=1,
                       font="arial 20", command=root.destroy)
    button.grid(row=2, column=1)
    if f == "show life":  # if we're watching, main()
        label.after(1000, main)


def main():
    """ life
    """
    global array1, generation, change, f
    if not(array1.any()):   # if all cells are dead
        raise(UnexpectedError("Dead after {} generation".format(generation)))
    change = 0
    if f == "show life":  # if we're watching, how they're living
        show_()   # show current generation
    array = np.zeros(size, dtype=int)
    for st in range(size[0]):   # strings
        for col in range(size[1]):   # columns
            if array1[st][col] == 0:   # if cell is dead
                if neighbours(st, col) == 3:   # and it has 3 alive neighbours
                    array[st][col] = 1    # it become alive
                    change = 1
                else:
                    array[st][col] = 0    # else it's still dead

            elif array1[st][col] == 1:  # if cell is alive and has 2
                if 1 < neighbours(st, col) < 4:   # or 3 alive neighbours
                    array[st][col] = 1   # it's still alive
                else:
                    array[st][col] = 0   # else cell dies
                    change = 1

            else:  # if cell not alive, nor dead
                er = "Wrong data at {} string, {} column".format(st+1, col+1)
                root.destroy()
                sys.exit(er)

    array1 = array
    if not(change) and f == "show":
        # so, we lived some generation, and then figure become static
        er = "Figure become static after {} generation".format(generation)
        root.destroy()
        raise(UnexpectedError(er))
        sys.exit()
    generation += 1


def get_value():
    global n
    n = int(ent_value.get())
    root2.destroy()


def ok():
    global way, f
    way = ent_way.get()
    f = var.get()
    root1.destroy()
    if f == "generate x generation":
        root2 = tk.Tk()
        root2.geometry('+550+400')
        lb3 = tk.Label(root2, text="x:", font="arial 12")
        ent_value = tk.Entry(root2)
        bt1 = tk.Button(root2, text="done", command=get_value,
                        font="arial 14")
        lb3.grid(row=1, column=1)
        ent_value.grid(row=1, column=2)
        bt1.grid(row=2, column=1)
        global ent_value, root2
        root2.mainloop()


def get_data():
    global ent_way, var, root1
    root1 = tk.Tk()
    root1.geometry('+550+400')
    lb2 = tk.Label(root1, text="way to file: ", font="arial 12")
    ent_way = tk.Entry(root1)   # way to file
    bt = tk.Button(root1, text="done", command=ok, font="arial 14")
    var = tk.StringVar(root1)
    var.set("Mode")
    opt = tk.OptionMenu(root1, var, "show life", "generate x generation")
    
    lb2.grid(row=1, column=1)
    ent_way.grid(row=1, column=2)
    opt.grid(row=2, column=1)
    bt.grid(row=2, column=2)

    root1.mainloop()


if __name__ == "__main__":
    way = ""
    generation = 1
    change = 0  # 1 if was some changes in figure, else 0
    HEIGHT = 500
    WIDTH = 500
    
    get_data()
    while 1:
        while f == "Mode":
            get_data()
        
        try:
            array1 = np.loadtxt(way, dtype=int)
        except IOError:
            if not(way):
                sys.exit()
            print("No such file or directory: {}\ntry again".format(way))
            get_data()
        else:
            break

    size = array1.shape
    
    if f == "generate x generation":
        # if you want save image as png-image
        # image_(generation).save("After {} generation.png".format(generation))
        for i in range(1, n):
            main()
        root = tk.Tk()
        show_()
        root.mainloop()

    elif f == "show life":
        root = tk.Tk()
        label = tk.Label()
        label.after_idle(main)  # root goes in loop and then main()
        root.mainloop()
