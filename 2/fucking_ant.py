import numpy as np
import time
import tkinter as tk

from PIL import Image, ImageDraw, ImageTk
# 0 - white, 1 - black


f = 0
HEIGHT = 500   # of window
WIDTH = 500
size = [0, 0]   # cell, of field
x = 0
y = 0
step = 1
direction = 3    # 0 - North, 1 - East, 2 - South, 3 - West


class UnexpectedError(Exception):
    def __init__(self, value):
        self.value = value


def data():   # First window, get size of image, ant's coordinates
    global f, HEIGHT, WIDTH, size, way, x, y, arrray
    global ent_h, ent_w, ent_y, ent_x, ent_dir, var, root1

    root1 = tk.Tk()
    root1.geometry('+500+400')
    var = tk.StringVar(root1)
    var.set("Field at the beginning")
    opt = tk.OptionMenu(root1, var, "White field", "My own field")
    lb1 = tk.Label(root1, text="    size of window:", font="arial 12")
    lb_h = tk.Label(root1, text="height", font="arial 12")
    lb_w = tk.Label(root1, text="width", font="arial 12")
    ent_h = tk.Entry(root1)
    ent_w = tk.Entry(root1)
    lb2 = tk.Label(root1, text="Original ant's coordinates:", font="arial 12")
    lb_x = tk.Label(root1, text="x", font="arial 12")
    lb_y = tk.Label(root1, text="y", font="arial 12")
    ent_x = tk.Entry(root1)
    ent_y = tk.Entry(root1)
    bt = tk.Button(root1, text="done", command=ok, font="arial 14")

    lb1.grid(row=1, column=1)
    lb_h.grid(row=2, column=1)
    lb_w.grid(row=3, column=1)
    ent_h.grid(row=2, column=2)
    ent_w.grid(row=3, column=2)
    lb2.grid(row=4, column=1)
    lb_x.grid(row=5, column=1)
    lb_y.grid(row=6, column=1)
    ent_x.grid(row=5, column=2)
    ent_y.grid(row=6, column=2)
    opt.grid(row=7, column=1)
    bt.grid(row=7, column=2)

    root1.mainloop()


def ok():  # Second window, get size of field or way
    global f, HEIGHT, WIDTH, x, y, direction
    global root2, ent_size0, ent_size1

    HEIGHT = int(ent_h.get())
    WIDTH = int(ent_w.get())
    x = int(ent_x.get())
    y = int(ent_y.get())
    f = var.get()
    root1.destroy()
    if f == "White field":
        root2 = tk.Tk()
        root2.geometry("+500+400")
        lb3 = tk.Label(root2, text="Size of field in cells:", font="arial 12")
        lb_size0 = tk.Label(root2, text="height", font="arial 12")
        lb_size1 = tk.Label(root2, text="width", font="arial 12")
        ent_size0 = tk.Entry(root2)
        ent_size1 = tk.Entry(root2)
        bt2 = tk.Button(root2, text="done",
                        command=get_value, font="arial 14")

        lb3.grid(row=1, column=1)
        lb_size0.grid(row=2, column=1)
        lb_size1.grid(row=3, column=1)
        ent_size0.grid(row=2, column=2)
        ent_size1.grid(row=3, column=2)
        bt2.grid(row=4, column=2)

        root2.mainloop()

    elif f == "My own field":
        root2 = tk.Tk()
        root2.geometry("+500+400")
        lb_way = tk.Label(root2, text="Way to file")
        ent_way = tk.Entry(root2)
        bt2 = tk.Button(root2, text="done",
                        command=get_value, font="arial 14")

        lb_way.grid(row=1, column=1)
        ent_way.grid(row=1, column=2)
        bt2.grid(row=2, column=2)

        root2.mainloop()

    elif f == "Field at the beginning":
        data()


def get_value():
    global array, size

    if f == "White field":
        size[0] = int(ent_size0.get()) - 1
        size[1] = int(ent_size1.get()) - 1
        array = np.zeros((size[0]+1, size[1]+1), dtype=int)
    else:
        array = np.loadtxt(way)
        size = array.shape

    root2.destroy()


def image_():  # generate image with ant's way
    if (step % 100) == 0:  # maybe, it'll be faster without print
        print(step, "step")
    im = Image.new("RGBA", (WIDTH+1, HEIGHT+1), (256, 256, 256, 256))
    draw = ImageDraw.Draw(im)
    step1 = HEIGHT / (size[0]+1)
    step2 = WIDTH / (size[1]+1)
    """  If you want to see cells
    for k in range(size[0]+2):
        draw.line((0, k*step1, WIDTH, k*step1), fill="black")    # ------
    for k in range(size[1]+2):
        draw.line((k*step2, 0, k*step2, HEIGHT), fill="black")    # |
    """
    for st in range(size[0]+1):
        for c in range(size[1]+1):
            if st == x and c == y:
                draw.rectangle((c*step2, st*step1, (c+1)*step2, (st+1)*step1),
                               fill="red",
                               outline="red")
            elif array[st][c]:
                draw.rectangle((c*step2, st*step1, (c+1)*step2, (st+1)*step1),
                               fill="black",
                               outline="black")
    return im


def show_():   # update image on root
    global label
    """ update image on root
    """
    label.destroy()
    photo = ImageTk.PhotoImage(image_())
    label = tk.Label(image=photo)
    label.image = photo
    label.grid(row=1, column=1)

    # ??????
    button = tk.Button(root, text="ok", width=5, height=1,
                       font="arial 20", command=root.destroy)
    # WHY? If i delete this button, program will crash

    label.after(2, main)


# LOGIC FUNCTIONS
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

    show_()
    if (array[x][y] == 0) or (array[x][y] == 1):
        turn(int(not(array[x][y])))
        array[x][y] = int(not(array[x][y]))
        step_()
    else:
        raise(UnexpectedError("Something goes wrong!"))
    step += 1


if __name__ == "__main__":
    data()
    root = tk.Tk()
    label = tk.Label()
    label.after_idle(main)
    root.mainloop()
